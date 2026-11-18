import time
import wave
from collections import deque

import sounddevice as sd
import numpy as np

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    http_options={"api_version": "v1beta"}
)


def mikrofon_sec():
    cihazlar = sd.query_devices()
    mikrofonlar = []

    print("\nKullanılabilir mikrofonlar:")

    for index, cihaz in enumerate(cihazlar):
        if cihaz["max_input_channels"] > 0:
            mikrofonlar.append(index)
            print(f"{len(mikrofonlar)}. {cihaz['name']}")

    if not mikrofonlar:
        print("Mikrofon bulunamadı!")
        return None

    try:
        secim = int(input("\nMikrofon numarasını seç: "))

        if secim < 1 or secim > len(mikrofonlar):
            print("Geçersiz mikrofon numarası!")
            return None

        return mikrofonlar[secim - 1]

    except ValueError:
        print("Lütfen geçerli bir sayı gir!")
        return None


def mikrofon_kaydi(
    secilen_mikrofon,
    dosya_yolu="ses_test.wav",
    sessizlik_suresi=1.2,
    max_sure=20,
    ses_esigi=300
):
    cihaz = sd.query_devices(secilen_mikrofon)

    ornekleme_hizi = int(cihaz["default_samplerate"])
    kanal = 1

    blok_suresi = 0.1
    blok_boyutu = int(ornekleme_hizi * blok_suresi)

    onceki_sesler = deque(maxlen=4)
    kayit = []

    konusma_basladi = False
    son_ses_zamani = None

    baslangic_zamani = time.monotonic()

    print("\nDinliyorum... Konuşabilirsin.")

    try:
        with sd.InputStream(
            samplerate=ornekleme_hizi,
            channels=kanal,
            dtype="int16",
            device=secilen_mikrofon,
            blocksize=blok_boyutu
        ) as stream:

            while time.monotonic() - baslangic_zamani < max_sure:

                blok, tasma = stream.read(blok_boyutu)

                blok = np.asarray(blok, dtype=np.int16)

                ses_seviyesi = float(
                    np.sqrt(np.mean(blok.astype(np.float32) ** 2))
                )

                simdiki_zaman = time.monotonic()

                if not konusma_basladi:

                    onceki_sesler.append(blok.copy())

                    if ses_seviyesi >= ses_esigi:

                        konusma_basladi = True
                        kayit.extend(onceki_sesler)

                        son_ses_zamani = simdiki_zaman

                        print("Konuşma algılandı...")

                else:

                    kayit.append(blok.copy())

                    if ses_seviyesi >= ses_esigi:
                        son_ses_zamani = simdiki_zaman

                    elif simdiki_zaman - son_ses_zamani >= sessizlik_suresi:
                        print("Konuşma bitti.")
                        break

        if not konusma_basladi:
            print("Konuşma algılanamadı!")
            return None

        ses_verisi = np.concatenate(kayit, axis=0)

        with wave.open(dosya_yolu, "wb") as dosya:
            dosya.setnchannels(kanal)
            dosya.setsampwidth(2)
            dosya.setframerate(ornekleme_hizi)
            dosya.writeframes(ses_verisi.tobytes())

        print("Ses kaydı tamamlandı!")

        return dosya_yolu

    except Exception as e:
        print(f"Mikrofon kayıt hatası: {e}")
        return None


def sesi_metne_cevir(dosya_yolu="ses_test.wav"):

    try:
        print("Ses Google'a gönderiliyor...")

        audio_file = client.files.upload(
            file=dosya_yolu
        )

        print("Konuşma metne dönüştürülüyor...")

        interaction = client.interactions.create(
            model="gemini-3.5-transcribe",
            input=[
                {
                    "type": "audio",
                    "uri": audio_file.uri,
                    "mime_type": audio_file.mime_type
                }
            ]
        )

        metin = interaction.output_text

        if not metin or not metin.strip():
            print("Konuşma algılanamadı!")
            return None

        print(f"\nAlgılanan konuşma: {metin}")

        return metin

    except FileNotFoundError:
        print("Ses dosyası bulunamadı!")
        return None

    except Exception as e:
        print(f"Transkripsiyon hatası: {e}")
        return None


def konusmayi_dinle(secilen_mikrofon):

    dosya_yolu = mikrofon_kaydi(secilen_mikrofon)

    if dosya_yolu is None:
        return None

    return sesi_metne_cevir(dosya_yolu)


# Dosya doğrudan çalıştırılırsa mikrofon testi yap.
# Başka bir dosyadan import edilirse otomatik kayıt başlamaz.

if __name__ == "__main__":

    mikrofon = mikrofon_sec()

    if mikrofon is not None:

        while True:

            metin = konusmayi_dinle(mikrofon)

            if metin:
                if metin.lower().strip() == "testi bitir":
                    print("Mikrofon testi tamamlandı.")
                    break
