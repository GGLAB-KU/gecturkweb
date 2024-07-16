from django.core.cache import cache

from seqtagmodel.text_corrector import TextCorrector


def get_text_corrector():
    text_corrector = cache.get('text_corrector')

    if text_corrector is None:
        # print("Creating a new TextCorrector instance")
        text_corrector = TextCorrector()
        cache.set('text_corrector', text_corrector)
    # else:
    # print("Using the cached TextCorrector instance")

    return text_corrector
