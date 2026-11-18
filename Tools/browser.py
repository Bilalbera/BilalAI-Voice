import webbrowser
from urllib.parse import urlparse

def open_website(url):
    # URL kontrolü
    if not isinstance(url, str) or not url.strip():
        return {
            "success": False,
            "message": "Geçerli bir internet adresi girilmedi."
        }

    url = url.strip()
    adres = urlparse(url)

    # Yalnızca HTTP ve HTTPS adreslerine izin ver
    if adres.scheme not in ("http", "https") or not adres.netloc:
        return {
            "success": False,
            "message": "Geçersiz veya izin verilmeyen internet adresi."
        }

    try:
        # Siteyi varsayılan tarayıcıda yeni sekmede aç
        acildi = webbrowser.open(url, new=2)

        if acildi:
            return {
                "success": True,
                "message": "Tarayıcıya siteyi açma isteği gönderildi."
            }

        return {
            "success": False,
            "message": "Tarayıcı başlatılamadı."
        }

    except Exception as hata:
        return {
            "success": False,
            "message": str(hata)
        }


# Dosya doğrudan çalıştırılırsa test et
if __name__ == "__main__":
    sonuc = open_website("https://www.google.com")
    print(sonuc["message"])
