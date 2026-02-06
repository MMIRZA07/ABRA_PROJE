import zmq 
import json 

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("sunucu Çalışıyor ...")

while True : 
    mesaj = socket.recv_string()
    istek =json.loads(mesaj)

    with open("kutuphane.json" , "r" , encoding="utf-8") as f : 
        data = json.load(f) 

    cevap = {}
    komut = istek["komut"]

    if komut == "ara":
  
        aranan_ad = istek["ad"].strip().lower()
        bulundu = False 

        for kitap in data["kitaplar"]:
            mevcut_kitap_adi = kitap["ad"].strip().lower()
            
            if mevcut_kitap_adi == aranan_ad: 
                cevap["durum"] = "kitap mevcut" 
                cevap["bilgi"] = f"ID: {kitap['id']}, Ad: {kitap['ad']}, Yazar: {kitap['yazar']}"
                bulundu = True
                print(f"Kitap bulundu: {kitap['ad']}")
                break 
                
        if not bulundu: 
            print("Kitap listede yok.")
            cevap["durum"] = "Kitap Mevcut değil"
    elif komut == "liste" : 
        kitap_liste = []

        for kitap in data["kitaplar"] : 
            kitap_liste.append(f"ID: {kitap['id']}, Ad: {kitap['ad']}, Yazar: {kitap['yazar']}")

        cevap["kitaplar"] = kitap_liste


    # Kitap Ekleme Kısmı
    elif komut == "ekle":
        yeni_kitap = {
            "id": istek["id"],
            "ad": istek["ad"],
            "yazar": istek["yazar"]
        }

        data["kitaplar"].append(yeni_kitap)

        with open("kutuphane.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        cevap["durum"] = "Kitap Eklendi"

    elif komut == "sil" : 
        id = istek["id"] 
        bul = False 

        for kitap in data["kitaplar"] : 
            if id == kitap["id"] : 
                data["kitaplar"].remove(kitap)
                bul = True
                break
        
        if bul is True : 
            with open("kutuphane.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            cevap["durum"] = "Kitap Silindi"
        else : cevap["durum"] = "kitap bulunamadı"

    socket.send_string(json.dumps(cevap ,ensure_ascii=False))         

