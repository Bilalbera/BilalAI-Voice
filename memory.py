import json

try:
    with open("hafiza.json", "r", encoding="utf-8") as readfile:
        konusmalistesi = json.load(readfile)
except FileNotFoundError:
    konusmalistesi = []

def mesaj_ekle(role, content):
    mesaj = {
        "role": role,
        "content": content
    }

    konusmalistesi.append(mesaj)

def hafizayi_kaydet():
    with open("hafiza.json", "w", encoding="utf-8") as writefile:
        json.dump(konusmalistesi, writefile, ensure_ascii=False, indent=4)

def gecmisi_getir():
    return konusmalistesi