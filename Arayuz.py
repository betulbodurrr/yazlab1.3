import random
import tkinter as tk
import time
from PIL import Image,ImageTk


class Arayuz:
    print("")
class Musteri():
    def __init__(self, musteri_id,zaman):
        self.musteri_id = musteri_id
        self.zaman=zaman

class Masa():
    def __init__(self, durum, musteriID, masaID): #0 boş 1 dolu
        self.durum = durum
        self.musteriID = musteriID
        self.masaID = masaID

class Garson():
    def __init__(self, durum, masaID):
        self.durum = durum
        self.masaID = masaID

class Asci():
    def __init__(self, durum, masaID):
        self.durum = durum
        self.masaID = masaID

global kapıdakiMusteriler
kapidakiMusteriler = []

global oturanMusteriler
oturanMusteriler = []

global musteriler
musteriler = []

global masalar
masalar = []

global garsonlar
garsonlar = []

global ascilar
ascilar = []

global gidenMusteri
gidenMusteri = 0

global maliyet
maliyet=0

"""
#musteriSayisi = 100
musteriGelmeSikligi = 5
masaSayisi = 20
garsonSayisi = 10
asciSayisi = 5
time = 180 #simulasyon 180 saniye olacak
"""

time=int(input("toplam süre :"))
musteriGelmeSikligi=int(input("periyot"))
musterino=int(input("müşteri sayısı"))
musteriSayisi=int((time/musteriGelmeSikligi)*musterino)


def musteriOlustur(musteriSayisi):
    for i in range(musteriSayisi):
        musteriler.append(Musteri(i,0))

musteriOlustur(musteriSayisi)
def masaOlustur(masaSayisi):
    masalar.clear()
    for i in range(masaSayisi):
        masalar.append(Masa(0, -1, i))

def garsonOlustur(garsonSayisi):
    garsonlar.clear()
    for i in range(garsonSayisi):
        garsonlar.append(Garson(0, -1))

def asciOlustur(asciSayisi):
    ascilar.clear()
    for i in range(asciSayisi):
        ascilar.append(Asci(0, -1))

def kapiyaMusteriGetir():
    kapidakiMusteriler.clear()
    for _ in range(int(musteriSayisi/musteriGelmeSikligi)):
        kapidakiMusteriler.append(Musteri(_,0))
        #print(f"_ degğeri:{_}   musteri sayıı: {len(musteriler)}  kapıdaki musteriler {len(kapidakiMusteriler)}")        


def masayaOtur():
    for musteri in kapidakiMusteriler:
        for masa in masalar:
            if(masa.durum == 0):
                masa.durum = 1
                masa.musteriID = musteri.musteri_id
                #print(len(kapidakiMusteriler))
                kapidakiMusteriler.remove(musteri)
                break

def masayaGarsonGonder():
    for masa in masalar:
        for garson in garsonlar:
            if(garson.durum == 0 and masa.durum == 1):
                garson.durum = 1
                garson.masaID = masa.masaID
                break
def asciyaGotur():
    for garson in garsonlar:
        for asci in ascilar:
            if(asci.durum == 0 and garson.durum == 1):
                asci.durum = 1
                garson.durum = 0
                break

def masaTemizle():
    for masa in masalar:
        if masa.durum == 1:
            masa.durum = 0
            masa.musteriID = -1

global sayac
sayac=0
data = []
print("Hesaplanıyor...")
for i in range(1000):

    k=2**(i+1)
    #print(f"k değeri: {k}")
    masaOlustur(int(musteriSayisi/k))
    """
    if (int(len(masalar) == 0)):
        masaOlustur(1)
    """
    
    garsonOlustur(random.randint(1,int(len(masalar))+1))#k değerlerini iptal edip random bir şekilde bakıyorum
    """
    if (int(len(masalar) / k) == 0):
        garsonOlustur(1)
    """
    asciOlustur(random.randint(1,int(len(garsonlar)+1)))
    """
    if (int(len(garsonlar) / k) == 0):
        asciOlustur(1)
    """

    """print(f"masa sayısı: {int(musteriSayisi/k)}--garson sayısı: {int(len(masalar)/k)}--asçı sayısı: {int(len(garsonlar)/k)}")
    maliyet=musteriSayisi-(int(musteriSayisi/k)+int(len(masalar)/k)+int(len(garsonlar)/k))"""
    maliyet = musteriSayisi - int(len(masalar)) - int(len(garsonlar)) - int(len(ascilar)-int(sayac))
    

       
    #print(f"verim: {maliyet}--masa sayısı: {len(masalar)}--garson sayısı: {len(garsonlar)}--asçı sayısı: {len(ascilar)}--bekleyen müşteriler{musteriSayisi}--giden müşteri {sayac}")
    
    
    data.append({"verim":maliyet,"masa sayısı": len(masalar),"garson sayısı": len(garsonlar),"asçı sayısı": len(ascilar),"bekleyen müşteriler":musteriSayisi,"giden müşteri": sayac})
    """
    with open("veriler.txt", "a") as dosya:
        dosya.write(f"verim:{maliyet}-masa sayısı:{len(masalar)}-garson sayısı:{len(garsonlar)}-asçı sayısı:{len(ascilar)}-bekleyen müşteriler:{musteriSayisi}-giden müşteri{sayac}\n")
    """
    for t in range(time):

        if(t % musteriGelmeSikligi):
            kapiyaMusteriGetir()

        masayaOtur()
        masayaGarsonGonder()
        asciyaGotur()
        t += 2 #2 saniye yemek yediler
        masaTemizle()
        
        if(t<len(musteriler)):
            musteriler[t].zaman+=9
            if(musteriler[t].zaman>=20):
                musteriler.pop(t)
                sayac+=1
        #print(f"{sayac} gitti")  
#dosyaya verileri dictionaye uygun bir şekilde kayıt ediyor.
#dosyadan verileri okuyup her bir özelliğini dictionary olarak kayıt edip
#süre,periyot,müşteri sayısı eşit olanları aşşağıdaki gibi düzenlenebilir.
"""
# Dosyadan okuma işlemi
with open("veriler.txt", "r") as dosya:
    satirlar = dosya.readlines()

# Verileri işleme
for satir in satirlar:
    # "-" karakterine göre split
    parcalanmis_veri = satir.split("-")
    
    # ":" karakterine göre split ve temizleme
    for parca in parcalanmis_veri:
        if ":" in parca:
            anahtar, deger = parca.split(":")
            anahtar = anahtar.strip()
            deger = deger.strip()
            print(f"{anahtar}: {deger}")
"""

min_giden_musteri = min(data, key=lambda x: x["giden müşteri"])["giden müşteri"]

musteri_az_giden_veriler = [veri for veri in data if veri["giden müşteri"] == min_giden_musteri]

max_verim_en_az_giden = max(musteri_az_giden_veriler, key=lambda x: x["verim"])

print(f"\nEn az giden müşteri verileri ({min_giden_musteri} müşteri):")
for veri in musteri_az_giden_veriler:
    print(veri)

print("\nEn yüksek verime sahip veriler:")    
print(max_verim_en_az_giden)
print("\n------------------------------------------------------------------------------------------------------------")

    #print(f"Verim: {data[-1]['verim']}, Masa Sayısı: {data[-1]['masa sayısı']}, Garson Sayısı: {data[-1]['garson sayısı']}, Asçı Sayısı: {data[-1]['asçı sayısı']}, Bekleyen Müşteriler: {data[-1]['bekleyen müşteriler']}, Giden Müşteri: {data[-1]['giden müşteri']}")

