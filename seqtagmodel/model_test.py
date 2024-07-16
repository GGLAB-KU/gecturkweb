import time

import seqtagmodel.rule_dict_creator as rule_dict_creator
from seqtagmodel.text_corrector import TextCorrector

all_examples = rule_dict_creator.get_all_examples()
simple_examples = rule_dict_creator.get_simple_examples()
input_string = ""
for example in all_examples:
    input_string += example.get('false_form') + " "

# measure time
print(input_string)

start_time = time.time()
text_corrector = TextCorrector()
output_new = text_corrector.correct_text_enhanced(input_string)
print("time: ", time.time() - start_time)


print("input_string:               ", output_new[0])
print("final_input_string:         ", output_new[1])
print("final_output_string:        ", output_new[2])


test_string = "Seçim çalışmaları başladı.tüm partilerin        teşkilatları il       ,         ilçe ve hatta mahalle düzeyinde harekete geçti. Sonuçları herkes gibi bende merakla bekliyorum. Önümüzdeki hafta istanbul, ankara ve izmir gibi önemli illerde mitingler düzenlenecek. Tatil yapmk istiyrum fakat çalışmaya devam etmem şart. Gidip te gelmemek var, gelip te görmemek var. Sen yada o buradan gidecek. Ayşe'de geldi. Ev de hiç süt kalmamıştı. Bugün öyle çok yorulmuşki hemen yattı. Karakara düşünüyordu. İnsanlık öldümü? Bu şirkette işe başlıyacağım. Ağızı bıçak açmıyor. İçerde kimse yok. Bu yaptığının hiçbir sebepi yok. Hukuğu ayaklar altına aldı. Dansetmek istemediği için gitti. Onu hemen ortadan kayıp et. Uyuya kalmak huyun olmuş. Arkadaşı ile birlikte kahve hane açtılar. Hiç bir şey yapmadan bekledi."
print("test_string: ", test_string)
test_corrected = text_corrector.correct_text_enhanced(test_string)
print("test_corrected: ", test_corrected[2])

