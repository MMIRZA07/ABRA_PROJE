import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Sunucu Çalışıyor...")

while True:
    mesaj = socket.recv_string()
    istek = json.loads(mesaj)

    with open("kutuphane.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    cevap = {}
    komut = istek["komut"]

    # Kitap Arama Kısmı
    if komut == "ara":
        ad = istek["ad"]
        bulundu = False

        for kitap in veri["kitaplar"]:
            if kitap["ad"].lower() == ad.lower():
                cevap["durum"] = "Kitap Mevcut"
                cevap["bilgi"] = (
                    f"(ID: {kitap['id']}, "
                    f"Ad: {kitap['ad']}, "
                    f"Yazar: {kitap['yazar']})"
                )
                bulundu = True
                break

        if not bulundu:
            cevap["durum"] = "Kitap Bulunamadı"

    # Kitapları Listeleme Kısmı
    elif komut == "listele":
        kitap_listesi = []

        for kitap in veri["kitaplar"]:
            kitap_listesi.append(
                f"(ID: {kitap['id']}, "
                f"Ad: {kitap['ad']}, "
                f"Yazar: {kitap['yazar']})"
            )

        cevap["kitaplar"] = kitap_listesi

    # Kitap Ekleme Kısmı
    elif komut == "ekle":
        yeni_kitap = {
            "id": istek["id"],
            "ad": istek["ad"],
            "yazar": istek["yazar"]
        }

        veri["kitaplar"].append(yeni_kitap)

        with open("kutuphane.json", "w", encoding="utf-8") as f:
            json.dump(veri, f, indent=4, ensure_ascii=False)

        cevap["durum"] = "Kitap Eklendi"

    # Kitap Silme Kısmı
    elif komut == "sil":
        id = istek["id"]
        bulundu = False

        for kitap in veri["kitaplar"]:
            if kitap["id"] == id:
                veri["kitaplar"].remove(kitap)
                bulundu = True
                break

        if bulundu:
            with open("kutuphane.json", "w", encoding="utf-8") as f:
                json.dump(veri, f, indent=4, ensure_ascii=False)
            cevap["durum"] = "Kitap Silindi"
        else:
            cevap["durum"] = "Kitap Bulunamadı"

    socket.send_string(json.dumps(cevap, ensure_ascii=False))