import time
from brain import cevap_uret
from memory import mesaj_ekle, hafizayi_kaydet
from speech_to_text import mikrofon_sec, konusmayi_dinle
from text_to_speech import seslendir

def sesli_mesaj_al(kullanici_adi, secilen_mikrofon):

    if secilen_mikrofon is None:
        print("Mikrofon kullanılamıyor!")
        return

    print("\nMikrofon dinlemeye başladı...")

    metin = konusmayi_dinle(secilen_mikrofon)

    if not metin:
        print("Konuşma algılanamadı!")
        return

    print("\nSen: " + metin)
    print("Düşünüyorum...")

    cevap = cevap_uret(metin, kullanici_adi)

    print("\nBilalAI: " + cevap)
    seslendir(cevap)

    # Hafızaya kaydet
    mesaj_ekle("user", metin)
    mesaj_ekle("assistant", cevap)

    hafizayi_kaydet()

    if secilen_mikrofon is None:
        print("Mikrofon seçilemedi. Sesli mod kapatılıyor.")
        return

baslangicmesaj = "Merhaba! Ben BilalAI Voice. Yani Sesli Asistanınım."
print(baslangicmesaj)

time.sleep(1)
print("Sistem başlatılıyor...")

time.sleep(4)
print("BilalAI Voice başarıyla hazırlandı!")

time.sleep(2)
baslangicmesajii = input("Lütfen adınızı girin: ")

with open("veri.txt", "w", encoding="utf-8") as writefile:
    writefile.write(baslangicmesajii)

with open("veri.txt", "r", encoding="utf-8") as readfile:
    baslangicmesajii = readfile.read()
time.sleep(1)

komut = input("Merhaba, " + baslangicmesajii + "! Bugün ne yapmak istersiniz? ")

while True:
    if komut.lower().strip() == "çıkış":
        print("Görüşürüz, " + baslangicmesajii + "!")
        break

    elif komut.lower().strip() == "sesli konuşma":
        sesli_mesaj_al(baslangicmesajii)

    else:
        print("Düşünüyor...")

        cevap = cevap_uret(komut, baslangicmesajii)

        print("\nBilalAI: " + cevap)

        mesaj_ekle("user", komut)
        mesaj_ekle("assistant", cevap)

        hafizayi_kaydet()

    komut = input("\nBaşka bir isteğiniz var mı? ")
