import subprocess

def open_application(app):

    if not isinstance(app, str) or not app.strip():
        return {
            "success": False,
            "message": "Geçerli bir uygulama adı belirtilmedi."
        }

    app = app.strip().lower()

    uygulamalar = {
        "notepad": ["notepad.exe"],
        "calculator": ["calc.exe"]
    }

    if app not in uygulamalar:
        return {
            "success": False,
            "message": "Bu uygulamaya izin verilmiyor."
        }

    try:
        subprocess.Popen(uygulamalar[app])
        return {
            "success": True,
            "message": f"{app} başarıyla başlatıldı."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "message": f"'{app}' uygulaması bilgisayarda bulunamadı."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Uygulama açılırken bir hata oluştu: {e}"
        }

if __name__ == "__main__":
    print(open_application("notepad"))
