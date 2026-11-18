import asyncio
import edge_tts
import pygame

SES = "tr-TR-AhmetNeural"
DOSYA = "bilalai_cevap.mp3"


# Metni ses dosyasına dönüştür
async def ses_dosyasi_olustur(metin):

    konusmaci = edge_tts.Communicate(
        text=metin,
        voice=SES
    )
    await konusmaci.save(DOSYA)


# Oluşturulan sesi çal
def seslendir(metin):
    if not metin or not metin.strip():
        return
    try:
        print("\nBilalAI konuşuyor...")

        asyncio.run(ses_dosyasi_olustur(metin))

        if pygame.mixer.get_init() is None:
            pygame.mixer.init()

        pygame.mixer.music.load(DOSYA)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()

    except Exception as e:
        print(f"Seslendirme hatası: {e}")

# Dosya doğrudan çalıştırıldığında test et
if __name__ == "__main__":
    seslendir("Merhaba! Ben BilalAi Voice. Artık seninle konuşabiliyorum.")
