from asyncio import Semaphore
from operator import index
import threading
import time
import tkinter as tk
from Arayuz import Arayuz


class Musteri(threading.Thread):
    def __init__(self, musteriID, semaphore, masalar,mutex,mutex1,mutex2):
        threading.Thread.__init__(self)
        self.musteriID = musteriID
        self.semaphore = semaphore
        self.masalar = masalar

    def run(self):
        global index
        index=6
        with mutex:
            # masa bloklandı....
            if 0 <= 6 - index < len(masalar):

                masalar[6 - index].musteriID = self.musteriID
                masalar[6 - index].durum = 1  # masa dolu olunca 1
                print(
                    f"{masalar[6-index].masaID}"
                    + " kilitlendi."
                    + f"{masalar[6-index].musteriID}"
                    + " geldi."
                    + f"{index}"
                )
                time.sleep(1)

                masalar[6- index].durum = 0  # masa boş olunca 0
                print(
                    f"{masalar[6-index].masaID}"
                    + " serbest."
                    + f"{masalar[6-index].musteriID}"
                    + " gitti."
                    + f"{index}"
                )
                index-=1
                if(index==1): return  #buradan çıkartamadaım hata veriyor   
            else:
                print("Invalid index, skipping the operation.")

                



class Garson(threading.Thread):
    def __init__(self, adi, masa, mutex):
        threading.Thread.__init__(self)
        self.adi = adi
        self.masa = masa
        self.mutex = mutex

    def run(self):
        while True:
            with self.mutex:
                if self.masa.durum == 1:  
                    print(f"{self.adi} yemeği servis ediyor masaID: {self.masa.masaID}")
                    
                    time.sleep(3)
                else:
                    print(f"{self.adi} bekliyor masaID: {self.masa.masaID}")
            time.sleep(1)


class Asci(threading.Thread):
    def __init__(self, adi):
        threading.Thread.__init__(self)
        self.adi = adi

    def run(self):
        while True:
            print(f"{self.adi} yemek yapıyor.")
            time.sleep(2)


class Kasa(threading.Thread):
    def __init__(self, adi):
        threading.Thread.__init__(self)
        self.adi = adi

    def run(self):
        while True:
            print(f"{self.adi} ücret ödendi.")
            time.sleep(3)


class masa:
    def __init__(self, musteriID, durum, masaID):
        self.musteriID = musteriID
        self.durum = durum
        self.masaID = masaID


index = 6
if __name__ == "__main__":
    mutex = threading.Lock()
    mutex1= threading.Lock()
    mutex2 = threading.Lock()

    arayuz = Arayuz()
    # arayuz.baslat()
    masa_sayisi = 6
    garson_sayisi = 3
    asci_sayisi = 2
    Liste = ["a", "b", "c", "d", "e"]
    Liste2 = ["f", "g", "h", "k", "y1", "y2"]
    Liste3 = ["l", "m", "y3"]
    Totaliste = Liste + Liste2 + Liste3

    masa_sayisi = 6
    semaphore = threading.Semaphore(masa_sayisi)  # Masa sayısı kadar semaphore oluştur

    masalar = []
    garsonlar = []

    threads = []
    musteriqueue, asciqueue, asciqueue, kasaqueue = (
        Semaphore(0),
        Semaphore(0),
        Semaphore(0),
        Semaphore(0),
    )
    for i in range(6):
        masa1 = masa(0, 0, i)
        masalar.append(masa1)
        print(f"{masa1}" + " nesnesi oluşturuldu.")
        
    for i in range(3):
        garson = Garson(f"Garson{i}", masalar[i], threading.Lock())  # Assign a waiter to each table
        garsonlar.append(garson)
        
    for musteriId in Totaliste:  # müşterileri tek tek dönecek
        yeni_musteri = Musteri(musteriId, semaphore, masalar,mutex,mutex1,mutex2)
        threads.append(yeni_musteri)
        print(musteriId + "'in thread oluşturuldu")

        yeni_musteri.start()  # Her müşteri geldiğinde yeni thread başlattık
        """
    for garson in garsonlar:
        garson.start()
        """
    for thread in threads:
        thread.join()