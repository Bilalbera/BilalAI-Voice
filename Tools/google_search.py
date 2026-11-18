from urllib.parse import quote_plus
from Tools.browser import open_website


def google_search(sorgu):

    # Arama sorgusunu kontrol et
    if not isinstance(sorgu, str) or not sorgu.strip():
        return {
            "success": False,
            "message": "Arama sorgusu boş olamaz. Lütfen aramak istediğin konuyu belirt."
        }

    # Arama metnini URL için kodla
    aranacak_metin = quote_plus(sorgu.strip())

    # Google arama adresini oluştur
    google_adresi = f"https://www.google.com/search?q={aranacak_metin}"

    # Browser aracını çalıştır
    sonuc = open_website(google_adresi)

    # İşlem sonucunu geri döndür
    return sonuc


if __name__ == "__main__":
    test = google_search("Python eğitimi")
    print(test)
