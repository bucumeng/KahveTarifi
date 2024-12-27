import json
import gensim
from gensim.models import Word2Vec
import numpy as np # benzerlik hesaplamasında

try:
    with open("tarifler.json", "r", encoding="utf-8") as f:
        tarifler = json.load(f) #python sözlüğü 
except FileNotFoundError:
    print("tarifler.json dosyası bulunamadı. Lütfen tarifleri ekleyin.")
    exit()


tum_malzemeler = [] # malzemeler, liste oluşturarak buraya ekledik.
for tarif in tarifler:
    tum_malzemeler.extend([m.lower() for m in tarif["ingredients"]])


model = Word2Vec([tum_malzemeler], min_count=1, vector_size=100, window=5, sg=1)


def benzerlik_hesapla(malzemeler, hedef_malzemeler):
    if not malzemeler or not hedef_malzemeler:
        return 0
    benzerlikler = []
    for malzeme in malzemeler:
        malzeme_benzerlikleri = []
        for hedef in hedef_malzemeler:
            try:
                malzeme_benzerlikleri.append(model.wv.similarity(malzeme, hedef))
            except KeyError: 
                pass
        if malzeme_benzerlikleri:
            benzerlikler.append(max(malzeme_benzerlikleri)) # Bir malzeme için en yüksek benzerliği al
    return np.mean(benzerlikler) if benzerlikler else 0 # tüm benzerliklerin ortalamasını alarak tarifin genel benzerlik oranını çıkartıyor



mevcut_malzemeler = input("Elindeki malzemeleri virgülle ayırarak girin: ").split(",")
mevcut_malzemeler = [malzeme.strip().lower() for malzeme in mevcut_malzemeler]


uygun_tarifler = []
for tarif in tarifler:
    tarif_malzemeleri = [malzeme.lower() for malzeme in tarif["ingredients"]]
    benzerlik = benzerlik_hesapla(mevcut_malzemeler, tarif_malzemeleri)
    if benzerlik > 0:  # Sadece pozitif benzerlikleri ekle
        uygun_tarifler.append((tarif, benzerlik))

uygun_tarifler.sort(key=lambda x: x[1], reverse=True)


if uygun_tarifler:
    print("Elindeki malzemelere en benzer ilk 3 kahve:")
    for i, (tarif, benzerlik) in enumerate(uygun_tarifler[:5]): 
        benzerlik_yuzde = benzerlik * 100
        print(f"\n{i+1}. {tarif['name']} (Benzerlik: {benzerlik_yuzde:.2f})")
        print(f"  Malzemeler: {', '.join(tarif['ingredients'])}")
        print(f"  Tarif: {tarif['instructions']}")
        print(f"  Süre: {tarif['duration']} dakika")
        print(f"  Zorluk: {tarif['difficulty']}")
        if i == 2: 
            break
else:
    print("Elindeki malzemelere benzer bir tarif bulunamadı.")
