from .applications import open_application
from .google_search import google_search
from .browser import open_website

tools = {
    "open_application": open_application,
    "google_search": google_search,
    "open_website": open_website
}

def arac_bul(arac_adi):
    return tools.get(arac_adi)

def arac_calistir(arac_adi, parametreler):
    if not isinstance(parametreler, dict):
        return {
            "success": False,
            "message": "Araç parametreleri geçersiz."
        }

    arac = arac_bul(arac_adi)

    if arac is None:
        return {
            "success": False,
            "message": "Bilinmeyen araç."
        }
    
    try:
        sonuc = arac(**parametreler)
        return sonuc

    except TypeError as e:
        return {
            "success": False,
            "message": f"Araç parametreleri hatalı: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Araç çalıştırılırken hata oluştu: {e}"
        }

if __name__ == "__main__":

    test = arac_calistir(
        "open_application",
        {"app": "notepad"}
    )

    print(test)
