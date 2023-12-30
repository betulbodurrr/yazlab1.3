import tkinter as tk
import time
from PIL import Image,ImageTk


class Arayuz:
    print("")
class Musteri():
    def __init__(self, musteri_id):
        self.musteri_id = musteri_id

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
        musteriler.append(Musteri(i))

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
        kapidakiMusteriler.append(Musteri(_))

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


for i in range(7):

    k=2**(i+1)
    print(f"k değeri: {k}")
    masaOlustur(int(musteriSayisi/k))

    if (int(len(masalar) == 0)):
        masaOlustur(1)

    garsonOlustur(int(len(masalar)/k))

    if (int(len(masalar) / k) == 0):
        garsonOlustur(1)

    asciOlustur(int(len(garsonlar)/k))

    if (int(len(garsonlar) / k) == 0):
        asciOlustur(1)

    """print(f"masa sayısı: {int(musteriSayisi/k)}--garson sayısı: {int(len(masalar)/k)}--asçı sayısı: {int(len(garsonlar)/k)}")
    maliyet=musteriSayisi-(int(musteriSayisi/k)+int(len(masalar)/k)+int(len(garsonlar)/k))"""
    maliyet = musteriSayisi - int(len(masalar)) - int(len(garsonlar)) - int(len(ascilar))
    print(f"verim: {maliyet}--masa sayısı: {len(masalar)}--garson sayısı: {len(garsonlar)}--asçı sayısı: {len(ascilar)}")
    
    for t in range(time):

        if(t % musteriGelmeSikligi):
            kapiyaMusteriGetir()

        masayaOtur()
        masayaGarsonGonder()
        asciyaGotur()
        t += 2 #2 saniye yemek yediler
        masaTemizle()

        if(t % 20 == 0):
            kapiyaMusteriGetir()


