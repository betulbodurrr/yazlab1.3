import threading
import time
import tkinter as tk
from Arayuz import Arayuz

class Masa(threading.Thread):
    def __init__(self, adi, semaphore, musteri):
        threading.Thread.__init__(self)
        self.adi = adi
        self.semaphore = semaphore
        self.musteriID = musteri

    def run(self):
        while True:
            self.semaphore.acquire()  # müşteri geldiğinde masa dolu olduğunda semaphoreı al

            print(f"{self.adi} masaya " + f"{self.musteriID} oturdu")
            time.sleep(10)
            self.semaphore.release()  # Müşteri gittiğinde semaphoreı serbest bırak
            print(f"{self.adi} masa boş.")


class Musteri(threading.Thread):
    def __init__(self, musteriID, semaphore):
        threading.Thread.__init__(self)
        self.musteriID = musteriID
        self.semaphore = semaphore

    def run(self):
        while True:
            self.semaphore.acquire()  # Müşteri geldiğinde bir masa serbest bırak
            for masa in masalar:
                if masa.musteriID == "":
                    masa.musteriID = self.musteriID
                    break
            self.semaphore.release()
            print(f"{self.musteriID}  geldi.")
            time.sleep(3)
            self.semaphore.acquire()
            for masa in masalar:
                if masa.musteriID == self.musteriID:
                    masa.musteriID = ""
                    break
            self.semaphore.release()
            self.semaphore.release()  # Müşteri geldiğinde bir masa serbest bırak
            print(f"{self.musteriID}  ayrıldı.")


class Garson(threading.Thread):
    def __init__(self, adi):
        threading.Thread.__init__(self)
        self.adi = adi

    def run(self):
        while True:
            print(f"{self.adi} yemeği servis ediyor.")
            time.sleep(3)


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


if __name__ == "__main__":
    arayuz = Arayuz()
    #arayuz.baslat()
    
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

    threads = []

    for musteriId in Totaliste:  # müşterileri tek tek dönecek
        yeni_musteri = Musteri(musteriId, semaphore)
        threads.append(yeni_musteri)
        yeni_musteri.start()  # Her müşteri geldiğinde yeni thread başlattık
        
    for i in range(masa_sayisi):
        masa = Masa(f"Masa {i + 1}", semaphore, "")
        masalar.append(masa)
        masa.start()  # Her masa için bir thread başlat

    for thread in threads:
        thread.join()
