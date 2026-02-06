import json
import time

with open("list.json" , "r") as f : 
    jsonDick = json.load(f)

A = set(jsonDick["list1"])
B = set(jsonDick["list2"])

basla = time.perf_counter()
kesisim = A.intersection(B) #A kesişim B
bitir = time.perf_counter()
Sure1 = bitir - basla 

basla = time.perf_counter()
fark = A.difference(B) #A Fark B
bitir = time.perf_counter()
Sure2 = bitir - basla 

basla = time.perf_counter()
birlesim = A.union(B) #A birleşim B
bitir = time.perf_counter()
Sure3 = bitir - basla 

sonuc_dick = {"kesisim" : list(kesisim) , 
              "birlesim": list(birlesim) , 
              "fark"    : list(fark),
              "sureler": {
                            "birlesim_suresi": Sure3,
                            "kesisim_suresi": Sure1,
                            "fark_suresi": Sure2
                         } 
            }
print(type(sonuc_dick))

with open("sonuclar.json", "w") as cikti_dosya:
        json.dump(sonuc_dick, cikti_dosya, indent=2)
