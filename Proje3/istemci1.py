import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("1- Kitap Ara")
print("2- Mevcut Kitapları Listele")
print("3- Kitap Ekle")
print("4- Kitap Sil")

secim = input("Seçiminiz: ")

# 📌 Kitap Ara
if secim == "1":
    ad = input("Kitap adı: ")
    istek = {
        "komut": "ara",
        "ad": ad
    }

# 📌 Listele
elif secim == "2":
    istek = {
        "komut": "listele"
    }

# 📌 Kitap Ekle
elif secim == "3":
    istek = {
        "komut": "ekle",
        "id": int(input("ID: ")),
        "ad": input("Kitap adı: "),
        "yazar": input("Yazar: ")
    }

# 📌 Kitap Sil
elif secim == "4":
    istek = {
        "komut": "sil",
        "id": int(input("Silinecek Kitap ID: "))
    }

else:
    print("Hatalı Seçim")
    exit()

socket.send_string(json.dumps(istek, ensure_ascii=False))
cevap = json.loads(socket.recv_string())

print()

# 📌 Ortak Çıktı
if "durum" in cevap:
    print(cevap["durum"])
    if "bilgi" in cevap:
        print(cevap["bilgi"])

if "kitaplar" in cevap:
    print("Mevcut Kitaplar:")
    for kitap in cevap["kitaplar"]:
        print(kitap)
