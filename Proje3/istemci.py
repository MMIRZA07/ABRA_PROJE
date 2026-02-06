import zmq 
import json

context =zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True :
    print("1- Kitap Ara")
    print("2- Kitap listesini Goster")
    print("3- Kitap Ekle")
    print("4- Kitap Sil")

    secim = input("seçiminiz : ") 

    if secim == '1' : 
        ad = input("kitap adi giriniz : ")
        istek = {
            "komut" : "ara" ,
            "ad" : ad 
        }

    elif secim == '2' : 
        istek = {
            "komut" : "liste" 
        }

    elif secim == '3' : 
        istek = {
            "komut" : "ekle" ,
            "id" : int(input(" id : ")),
            "ad" : input("kitap adi :"),
            "yazar" : input("Yazar : ")
        }

    elif secim == '4' : 
        istek = {
            "komut" : "sil" ,
            "id" : int(input("silinecek kitabin id si :"))
        }

    else : print("hatali secim .")


    socket.send_string(json.dumps(istek , ensure_ascii=False))
    cevap = json.loads(socket.recv_string())

    if "durum" in cevap:
        print(cevap["durum"])
        if "bilgi" in cevap: 
            print(cevap["bilgi"])

    if "kitaplar" in cevap: 
        print("Mevcut Kitaplar :")
        for kitap in cevap["kitaplar"]: 
            print(kitap)


