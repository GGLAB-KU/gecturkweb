import copy
import json
import os
import re

import numpy as np
import regex
import torch
from datasets import Dataset
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoTokenizer, DataCollatorForTokenClassification, AutoModelForTokenClassification
from trnlp import TrnlpWord
from zemberek import (TurkishSentenceNormalizer, TurkishMorphology)

from seqtagmodel.correction_package.correction_rules import correction_rules


def get_prediction_words(input_sentences_tokenized, output_sentences_tokenized, predictions_tokenized):
    edits = []
    for s_idx, (input_sentence, output_sentence, predictions) in enumerate(
            zip(input_sentences_tokenized, output_sentences_tokenized, predictions_tokenized)):
        e_data = {
            'source': " ".join(input_sentence),
            'edits': []
        }
        for word_idx, (in_word, out_word, prediction) in enumerate(
                zip(input_sentence, output_sentence, predictions)):
            # Only consider words where a change has been predicted and the output is not an empty string
            if prediction != 'O' and out_word.strip():
                # Use the word index for o_start and adjust o_end if the following word is removed
                o_start = word_idx
                o_end = o_start + 2 if word_idx + 1 < len(input_sentence) and input_sentence[
                    word_idx + 1].strip() and not output_sentence[word_idx + 1].strip() else o_start + 1
                e_data['edits'].append((o_start, o_end, prediction, out_word.strip()))
        edits.append(e_data)
    return edits


def correct_whitespaces(text: str):
    # CASE 1: Remove extra spaces between words (including Unicode spaces)
    text = re.sub(r'\s+', ' ', text)

    # CASE 2: Add a space after punctuation if not present (including more punctuation marks)
    text = re.sub(r'([,.?!…;:—])(\S)', r'\1 \2', text)

    # CASE 3: Remove spaces before punctuation (including more punctuation marks)
    text = re.sub(r'\s+([,.?!…;:—])', r'\1', text)

    return text


def correct_capitalization(text):
    # Define a function to capitalize the first character of a match object
    def capitalize_first_character(match):
        return match.group(0).capitalize()

    # Correct capitalization after punctuation marks
    text = regex.sub(r'([.!?]|(\.{3}))\s*(\p{L})', lambda m: m.group(0)[:-1] + ' ' + m.group(0)[-1].upper(), text)

    # Capitalize the first character of the text
    text = regex.sub(r'^\s*(\p{L})', capitalize_first_character, text)

    return text


def correct_whitespaces_and_capitalization(text: str):
    text = correct_whitespaces(text)
    text = correct_capitalization(text)
    text = correct_whitespaces(text)
    return text


def split_text(text: str):
    words = re.findall(r'\w+\S*', text)
    return words


def merge_words_with_whitespaces(words: list):
    merged_text = ' '.join(words)
    return merged_text


def merge_sentences_with_periods(sentences: list):
    merged_text = '. '.join(sentences)
    return merged_text


class TextCorrector:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = self.dir_path + "/seqtagmodel/sequence-tagger"
        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")
        self.data_collator = DataCollatorForTokenClassification(tokenizer=self.tokenizer)
        self.rules_path = self.dir_path + "/seqtagmodel/rules.json"

        self.label_names = [
            "O",
            "B-rule_1",
            "B-rule_2",
            "B-rule_3",
            "B-rule_4",
            "B-rule_5",
            "B-rule_6",
            "B-rule_7",
            "B-rule_8",
            "B-rule_9",
            "B-rule_10",
            "B-rule_11",
            "B-rule_12",
            "B-rule_13",
            "B-rule_14",
            "B-rule_15",
            "B-rule_16",
            "B-rule_17",
            "B-rule_18",
            "B-rule_19",
            "B-rule_20",
            "B-rule_21",
            "B-rule_22",
            "B-rule_23",
            "B-rule_24",
            "B-rule_25",
        ]

        with open(self.rules_path) as f:
            self.explain_rules = json.load(f)

        self.id2label = {i: label for i, label in enumerate(self.label_names)}
        self.label2id = {v: k for k, v in self.id2label.items()}

        self.model = AutoModelForTokenClassification.from_pretrained(
            self.model_path,
            id2label=self.id2label,
            label2id=self.label2id,
        )
        # c
        self.model = self.model.to(self.device)
        self.trnlp_obj = TrnlpWord()

    def tokenize_and_align_labels(self, data):
        tokenized_inputs = self.tokenizer(data["tokens"], truncation=True, is_split_into_words=True)

        labels = []
        for i, label in enumerate(data["labels"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:  # Set the special tokens to -100.
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(-100)
                previous_word_idx = word_idx
            labels.append(label_ids)

        tokenized_inputs["labels"] = labels
        return tokenized_inputs

    def correct_text(self, test_data_str):
        test_source_sentences = test_data_str.split(".")
        test_len = len(test_source_sentences)
        test_labels = []
        test_sentences = []

        for i in range(test_len):
            sentence = test_source_sentences[i].strip().split(" ")
            sentence = [word for word in sentence if word]  # remove empty strings
            label = [0] * len(sentence)
            test_labels.append(label)
            test_sentences.append(sentence)

        test_dataset = Dataset.from_dict({"tokens": test_sentences, "labels": test_labels})
        tokenized_test_dataset = test_dataset.map(lambda data: self.tokenize_and_align_labels(data),
                                                  batched=True, remove_columns=test_dataset.column_names)

        test_dataloader = DataLoader(
            tokenized_test_dataset, collate_fn=self.data_collator, batch_size=64)
        self.model.eval()
        all_predictions = []
        all_labels = []
        for batch in tqdm(test_dataloader):
            for key, value in batch.items():
                batch[key] = batch[key].to(self.device)

            with torch.no_grad():
                outputs = self.model(**batch)

            predictions = np.argmax(outputs["logits"].cpu(), axis=2)
            labels = batch["labels"]

            # Remove ignored index (special tokens)
            true_predictions = [
                [self.label_names[p] for (p, l) in zip(prediction, label) if l != -100]
                for prediction, label in zip(predictions, labels)
            ]
            true_labels = [
                [self.label_names[l] for (p, l) in zip(prediction, label) if l != -100]
                for prediction, label in zip(predictions, labels)
            ]

            all_predictions.extend(true_predictions)
            all_labels.extend(true_labels)

        test_sentences_before_correction = copy.deepcopy(test_sentences)

        n = len(test_sentences)
        model_outputs = copy.deepcopy(all_predictions)

        for idx in range(0, n):
            for i, label in enumerate(model_outputs[idx]):
                if label == "O":
                    model_outputs[idx][i] = 0
                elif label == 0:
                    continue
                else:
                    correction_rule = correction_rules["rule_" + label.split("_")[-1]]
                    try:
                        correction_rule(test_sentences[idx], model_outputs[idx], i)
                    except Exception as e:
                        pass

        return all_predictions, test_sentences_before_correction, test_sentences

    def correct_text_enhanced(self, input_string):
        after_add1_string = correct_whitespaces_and_capitalization(input_string)
        predictions_tokenized, input_sentences_tokenized, output_sentences_tokenized = self.correct_text(
            after_add1_string)
        for i in range(len(output_sentences_tokenized)):
            for j in range(len(output_sentences_tokenized[i])):
                current_word = output_sentences_tokenized[i][j]
                current_word = current_word.strip(".,?!…;:—")
                self.trnlp_obj.setword(current_word)
                if self.trnlp_obj.get_base_type == 'özel' and current_word[0].islower():
                    output_sentences_tokenized[i][j] = output_sentences_tokenized[i][j][0].upper() + \
                                                       output_sentences_tokenized[i][j][1:]
                    predictions_tokenized[i][j] = 'B-rule_27'
        after_our_model_and_add2_sentences_with_no_dots = [" ".join(sentence) for sentence in
                                                           output_sentences_tokenized]
        after_our_model_and_add2_string = ". ".join(after_our_model_and_add2_sentences_with_no_dots)
        morphology = TurkishMorphology.create_with_defaults()
        normalizer = TurkishSentenceNormalizer(morphology)
        after_add3_temp = normalizer.normalize(after_our_model_and_add2_string)
        after_add3_string = correct_whitespaces_and_capitalization(after_add3_temp)
        new_predictions_tokenized, new_input_sentences_tokenized, new_output_sentences_tokenized = self.correct_text(
            after_add3_string)
        for i in range(len(new_output_sentences_tokenized)):
            if len(new_output_sentences_tokenized[i]) == len(output_sentences_tokenized[i]):
                for j in range(len(new_output_sentences_tokenized[i])):
                    current_word_1 = new_output_sentences_tokenized[i][j]
                    current_word_2 = output_sentences_tokenized[i][j]
                    current_word_1 = current_word_1.strip(".,?!…;:—").lower()
                    current_word_2 = current_word_2.strip(".,?!…;:—").lower()
                    if current_word_1 != current_word_2:
                        output_sentences_tokenized[i][j] = new_output_sentences_tokenized[i][j]
                        predictions_tokenized[i][j] = 'B-rule_28'

        for i in range(len(output_sentences_tokenized)):
            for j in range(len(output_sentences_tokenized[i])):
                if j == len(output_sentences_tokenized[i]) - 1:
                    if len(output_sentences_tokenized[i][j]) > 0 and output_sentences_tokenized[i][j][-1] not in [".",
                                                                                                                  ",",
                                                                                                                  "?",
                                                                                                                  "!",
                                                                                                                  "…",
                                                                                                                  ";",
                                                                                                                  ":",
                                                                                                                  "—"]:
                        output_sentences_tokenized[i][j] = output_sentences_tokenized[i][j] + "."

        for i in range(len(input_sentences_tokenized)):
            for j in range(len(input_sentences_tokenized[i])):
                if j == len(input_sentences_tokenized[i]) - 1:
                    if len(input_sentences_tokenized[i][j]) > 0 and input_sentences_tokenized[i][j][-1] not in [".",
                                                                                                                ",",
                                                                                                                "?",
                                                                                                                "!",
                                                                                                                "…",
                                                                                                                ";",
                                                                                                                ":",
                                                                                                                "—"]:
                        input_sentences_tokenized[i][j] = input_sentences_tokenized[i][j] + "."

        for i in range(len(input_sentences_tokenized)):
            if input_sentences_tokenized[i] == ['']:
                del input_sentences_tokenized[i]
                del output_sentences_tokenized[i]
                del predictions_tokenized[i]
                i = i - 1

        return input_sentences_tokenized, output_sentences_tokenized, predictions_tokenized

    def process_text(self, input_string):
        # if input string do not contain any chars return empty string
        if not any(char.isalpha() for char in input_string):
            return " ", " ", "Lütfen geçerli metin giriniz."
        lines = input_string.split("\n")
        input_sentences_tokenized, output_sentences_tokenized, predictions_tokenized = self.correct_text_enhanced(
            input_string)

        if len(lines) == 1:
            line_idx = [0] * len(input_sentences_tokenized)
        else:  # TODO fix this later, not important for now.
            line_idx = [0] * len(input_sentences_tokenized)

        final_outs = get_prediction_words(input_sentences_tokenized, output_sentences_tokenized, predictions_tokenized)

        out_lines = [[] for _ in lines]
        for l_idx, out in zip(line_idx, final_outs):
            tokens = out['source']
            if isinstance(tokens, str):
                tokens = tokens.split(' ')
            edits = out['edits']
            offset = 0
            for edit in edits:
                e_start = edit[0]
                e_end = edit[1]
                e_type = edit[2]
                e_rep = edit[3]
                errant_info = self.explain_rules[e_type]
                explanation = errant_info["exp"]
                title = errant_info["title"]
                color = errant_info["color"]
                errant_info = '<p>' + explanation + '</p>'


                msg = '<p>' + errant_info + '</p>'
                prefix = f'<span class="d-inline-block"><a tabindex="0" data-bs-html="true" role="button" ' \
                         f'data-bs-toggle="popover" data-bs-trigger="focus" ' \
                         f'data-bs-placement="top" class="edit" ' \
                         f'title="{title}" data-bs-content="{msg}" style="background-color: {color}; font-size: 16px;">'

                suffix = '</a></span>'
                e_cor = [prefix] + e_rep.split() + [suffix]
                len_cor = len(e_cor)
                tokens[e_start + offset:e_end + offset] = e_cor
                offset = offset - (e_end - e_start) + len_cor

            out = ' '.join(tokens)
            out_lines[l_idx].append(out)

        str_out = '\n'.join([' '.join(l) for l in out_lines])
        str_out = '<p>' + str_out + '</p>'

        final_input_string = ' '.join([' '.join(l) for l in input_sentences_tokenized])
        final_output_string = ' '.join([' '.join(l) for l in output_sentences_tokenized])
        return final_input_string, final_output_string, str_out
