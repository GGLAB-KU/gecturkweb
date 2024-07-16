def create_example_dict(rule_id_in: str, description_english: str,
                        true_sentence_in: str,
                        false_sentence_in: str,
                        description_turkish: str):
    return dict(rule_id=rule_id_in, description_eng=description_english,
                true_form=true_sentence_in,
                false_form=false_sentence_in,
                description_tr=description_turkish)


s2 = create_example_dict("B-rule_2", "Conjunction “-de/-da” must follow the vowel harmony.", # deda
                         "Kızı da geldi gelini de.",
                         "Kızı de geldi gelini de.",
                         "Bağlaç olan da / de büyük ünlü uyumuna uymalıdır.")

s3 = create_example_dict("B-rule_3", "Conjunction “-de/-da” does not follow phonetic assimilation rules.", #deda
                         "Gidip de gelmemek var, gelip de görmemek var.",
                         "Gidip te gelmemek var, gelip te görmemek var.",
                         "Ayrı yazılan da / de hiçbir zaman ta / te biçiminde yazılmaz.")

s4 = create_example_dict("B-rule_4", "“-de/-da” written together with the word “ya” is always written separately.", # deda
                         "Sen ya da o buradan gidecek.",
                         "Sen yada o buradan gidecek.",
                         "Ya sözüyle birlikte kullanılan da her zaman ayrı yazılır.")

s5 = create_example_dict("B-rule_5", "Conjunction “-de/-da” cannot be used with an apostrophe.", # deda
                         "Ayşe de geldi.",
                         "Ayşe'de geldi.",
                         "Da / de bağlacını kendisinden önceki kelimeden kesme ile ayırmak yanlıştır.")

s6 = create_example_dict("B-rule_6", "Suffix “-de/-da” is written adjacent.", # deda
                         "Evde hiç süt kalmamıştı.",
                         "Ev de hiç süt kalmamıştı.",
                         "Bulunma durumu eki getirildiği kelimeye bitişik yazılır.")

s7 = create_example_dict("B-rule_7", "Conjunction “-ki” is written separately.", # ki
                         "Bugün öyle çok yorulmuş ki hemen yattı.",
                         "Bugün öyle çok yorulmuşki hemen yattı.",
                         "Bağlaç olan ki her zaman ayrı yazılır.")

s8 = create_example_dict("B-rule_8",
                         "On some exceptional instances, by convention, the conjunction “-ki” is written adjacent.", # ki
                         "Oysaki ne olacağını ona söylemiştim.",
                         "Oysa ki ne olacağını ona söylemiştim.",
                         "Birkaç örnekte ki bağlacı kalıplaşmış olduğu için bitişik yazılır: belki, çünkü, hâlbuki, mademki, meğerki, oysaki, sanki.")

s9 = create_example_dict("B-rule_9",
                         "Words that start with double consonants of foreign origin are written without adding an “-i” between the letters.", # foreign
                         "Uçaktan indikten sonra trene bin.",
                         "Uçaktan indikten sonra tirene bin.",
                         "Çift ünsüz harfle başlayan Batı kökenli alıntılar, ünsüzler arasına ünlü konulmadan yazılır.")

s10 = create_example_dict("B-rule_10", "Duplicats must be written separately.", # single
                          "Kara kara düşünüyordu.",
                          "Karakara düşünüyordu.",
                          "Aynı sözcükten oluşan ikilemeler ayrı yazılır.")

s11 = create_example_dict("B-rule_11", "Mi/mı/mu/mü should be written separately.", # mi
                          "İnsanlık öldü mü?",
                          "İnsanlık öldümü?",
                          "Soru eki olan mı, mi, mu, mü ayrı yazılır.")

s12 = create_example_dict("B-rule_12", "Suffixes starting with -e/-a are written as is unlike the pronunciation.", # single
                          "Bu şirkette işe başlayacağım.",
                          "Bu şirkette işe başlıyacağım.",
                          "-A / -e, -acak / -ecek, -ayım / -eyim, -alım / -elim, -an / -en vb. eklerden önce gelen ünlü veya ekin geniş ünlüsü söyleyişe bakılmaksızın a / e ile yazılır.")

s13 = create_example_dict("B-rule_13", "Some words that has two syllables lose a vowel from the second syllable.",
                          "Ağzı bıçak açmıyor.",
                          "Ağızı bıçak açmıyor.", # bisyllabic
                          "İki heceli bazı kelimeler ünlüyle başlayan bir ek aldıklarında ikinci hecelerindeki dar ünlüler düşer.")

s14 = create_example_dict("B-rule_14", "Some words do not obey the rule_13.", # bisyllabic
                          "İçeride kimse yok.",
                          "İçerde kimse yok.",
                          "İçeri, dışarı, ileri, şura, bura, ora, yukarı, aşağı gibi sözler ek aldıklarında sonlarında bulunan ünlüler düşmez.")

s15 = create_example_dict("B-rule_15",
                          "Last consonant of the foreign words gets transformed when they get a suffix that starts with a vowel.", #foreign
                          "Bu yaptığının hiçbir sebebi yok.",
                          "Bu yaptığının hiçbir sebepi yok.",
                          "Alıntı kelimeler ünlü ile başlayan bir ek aldıklarında kelime sonlarındaki sert ünsüzler yumuşar.")

s16 = create_example_dict("B-rule_16", "Some words do not obey the rule_15.", # foreign
                          "Hukuku ayaklar altına aldı.",
                          "Hukuğu ayaklar altına aldı.",
                          "Bazı alıntı kelimelerde yumuşama olmaz: ahlak / ahlakın, cumhuriyet / cumhuriyete, evrak / evrakı, hukuk / hukuku, ittifak / ittifaka, sepet / sepeti, tank / tankı vb.") # foreign

s17 = create_example_dict("B-rule_17",
                          "Compound words made with etmek, edilmek, eylemek, olmak, olunmak, are written separately unless there is a grammatic transformation.", # light verb
                          "Dans etmek istemediği için gitti.",
                          "Dansetmek istemediği için gitti.",
                          "Etmek, edilmek, eylemek, olmak, olunmak yardımcı fiilleriyle kurulan birleşik fiiller, ilk kelimesinde herhangi bir ses düşmesi veya türemesine uğramazsa ayrı yazılır.")

s18 = create_example_dict("B-rule_18", "Compound words are written jointly when they lose a vowel.", # light verb
                          "Onu hemen ortadan kaybet.",
                          "Onu hemen ortadan kayıp et.",
                          "Özgün biçimleri tek heceli bazı Arapça kökenli kelimeler yardımcı fiilleriyle birleşirken ses düşmesine, ses değişmesine veya ses türemesine uğradıklarında bitişik yazılır.")

s19 = create_example_dict("B-rule_19",
                          "Compound words are written jointly when second the meaning of the second changes.", # compound
                          "Duvarı aslanağzı rengine boyadı.",
                          "Duvarı aslan ağzı rengine boyadı.",
                          "Kelimelerden her ikisi veya ikincisi, birleşme sırasında anlam değişmesine uğradığında bu tür birleşik kelimeler bitişik yazılır.")

s20 = create_example_dict("B-rule_20",
                          "Conjunction words created with bilmek, vermek, kalmak, durmak, gelmek and yazmak are written jointly if they have one of the following suffixes:-a, -e, -ı, -i, -u, -ü.", # compound
                          "Uyuyakalmak huyun olmuş.",
                          "Uyuya kalmak huyun olmuş.",
                          "-A, -e, -ı, -i, -u, -ü zarf-fiil ekleriyle bilmek, vermek, kalmak, durmak, gelmek ve yazmak fiilleriyle yapılan tasvirî fiiller bitişik yazılır.")

s21 = create_example_dict("B-rule_21", "Conjunction words created with hane, name and zade are written jointly.", # compound
                          "Arkadaşı ile birlikte kahvehane açtılar.",
                          "Arkadaşı ile birlikte kahve hane açtılar.",
                          "Hane, name, zade kelimeleriyle oluşturulan birleşik kelime­ler bitişik yazılır.")

s22 = create_example_dict("B-rule_22", "Conventionally, some pronounes are written jointly.", # single
                          "Hiçbir şey yapmadan bekledi.",
                          "Hiç bir şey yapmadan bekledi.",
                          "Biraz, birçok, birçoğu, birkaç, birkaçı, birtakım, herhangi, hiçbir, hiçbiri belirsizlik sıfat ve zamirleri de gelenekleşmiş olarak bitişik yazılır.")

s23 = create_example_dict("B-rule_23", "First word of a sentence must be capitalized.", # single
                          "hemen okula git.",
                          "hemen okula git.",
                          "Cümle başında bulunan kelimenin ilk harfi büyük harfle yazılır.")

s24 = create_example_dict("B-rule_24",
                          "In some of the words originating from Arabic and Persian, the letter a and u should be written with a circumflex accent (^).", # single
                          "Evde hiç kâğıt kalmamış.",
                          "Evde hiç kağıt kalmamış.",
                          "Arapça ve Farsçadan dilimize giren birtakım kelimelerle özel adlarda bulunan ince g, k ünsüzlerinden sonra gelen a ve u ünlüleri üzerine konur.")

s25 = create_example_dict("B-rule_25", "NOT DEFINED YET",
                          "NOT DEFINED YET",
                          "NOT DEFINED YET",
                          "NOT DEFINED YET")

sO = create_example_dict("O", "Correct word.",
                         "Seçim çalışmaları başladı.",
                         "Seçim çalışmaları başladı.",
                         "Doğru kelime.")

s1 = create_example_dict("B-rule_1", "Conjunction “-de/-da” is written separately.", # red
                         "Sonuçları herkes gibi ben de merakla bekliyorum.",
                         "Sonuçları herkes gibi bende merakla bekliyorum.",
                         "Bağlaç olan da / de ayrı yazılır.") # de/da

s26 = create_example_dict("B-rule_26", "Sentences with whitespaces and capitalization errors", # my1
                          "Tüm partilerin teşkilatları il, ilçe ve hatta mahalle düzeyinde harekete geçti.",
                          "tüm partilerin teşkilatları il , ilçe ve hatta mahalle düzeyinde harekete geçti.",
                          "Cümle büyük harfle başlar ve bir cümledeki kelimeler arasında boşluk bırakılmalıdır.")

s27 = create_example_dict("B-rule_27", "Special names are written with capital letters.", # my2
                          "Önümüzdeki hafta İstanbul, Ankara ve İzmir gibi önemli illerde mitingler düzenlenecek.",
                          "Önümüzdeki hafta istanbul, ankara ve izmir gibi önemli illerde mitingler düzenlenecek.",
                          "Özel isimler büyük harfle yazılır.")

s28 = create_example_dict("B-rule_28", "Typos are not allowed.", # my3
                          "Tatil yapmak istiyorum fakat çalışmaya devam etmem şart.",
                          "Tatil yapmk istiyrum fakat çalışmaya devam etmem şart.",
                          "Türkçe yazım kurallarına uyulmalıdır.")


# Create a list of dictionaries

def get_all_examples():
    return [sO, s26, s1, s27, s28, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19,
            s20, s21, s22, s23, s24, s25]


def get_simple_examples():
    return [sO, s26, s1, s27, s28]
