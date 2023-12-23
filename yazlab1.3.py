from asyncio import Semaphore
from itertools import count
from operator import index
import threading
import time
import tkinter as tk
from Arayuz import Arayuz


class Musteri(threading.Thread):
    def __init__(self, musteriID, semaphore, masalar,mutex,mutex1,musteriqueue):
        threading.Thread.__init__(self)
        self.musteriID = musteriID
        self.semaphore = semaphore
        self.masalar = masalar
        self.musteriqueue=musteriqueue
    def masa_ara(self,masalar):
        for x in range(6):
            if(masalar[x].durum==0):
                return 1
            
        
    def run(self):
        index=6
        
        for table_number in range(len(masalar)):
            
            with mutex:
            # masa bloklandı....

                if masalar[table_number].durum==0:
                    masalar[table_number].musteriID = self.musteriID
                    masalar[table_number].durum = 1  # masa dolu olunca 1
                    print(
                        f"{masalar[table_number].masaID}"
                        + " kilitlendi."
                        + f"{masalar[table_number].musteriID}"
                        + " geldi."
                        + f"{table_number}"
                    )
                    break

        else:
            print(f"No available tables for customer {self.musteriID}")    #bekleyen müşteriler
                
         


                



class Garson(threading.Thread):
    def __init__(self, adi, masalar, mutex):
        threading.Thread.__init__(self)
        self.adi = adi
        self.masalar = masalar
        self.mutex = mutex


    def run(self):
    
        while True:
            with mutex:
                unattended_tables = [table_number for table_number, table in enumerate(masalar) if masalar[table_number].durum == 1]
                #print(f"{unattended_tables} bu masalarda müşteri var garson yok")

                if unattended_tables:
                    table_number = unattended_tables[0]
                    masalar[table_number].durum = 2  
                    print(f"{self.adi} yemeği {masalar[table_number].musteriID} 'e servis ediyor masaID: {masalar[table_number].masaID}")
                    time.sleep(1)
                else:
                    print(f"{self.adi} müşteri bekliyor ")
            time.sleep(1)
       


class Asci(threading.Thread):
    def __init__(self, adi, masalar, mutex):
        threading.Thread.__init__(self)
        self.adi = adi
        self.masalar = masalar
        self.mutex = mutex

    def run(self):
        time.sleep(3)
        while True:
            with mutex:
                unattended_tables = [table_number for table_number, table in enumerate(masalar) if masalar[table_number].durum == 2]

                if unattended_tables:
                    table_number = unattended_tables[0]
                    masalar[table_number].durum = 3 
                    print(f"{self.adi} yemek yapıyor.{masalar[table_number].musteriID} masaID: {masalar[table_number].masaID}")
                    time.sleep(1)
                #else:
                    #print(f"{self.adi} müşteri bekliyor ")
            time.sleep(1)

class Kasa(threading.Thread):
    def __init__(self, adi, masalar, mutex):
        threading.Thread.__init__(self)
        self.adi = adi
        self.masalar = masalar
        self.mutex = mutex

    def run(self):
        time.sleep(5)
        
        while True:
            with mutex:
                unattended_tables = [table_number for table_number, table in enumerate(masalar) if masalar[table_number].durum == 3]

                if unattended_tables:
                    table_number = unattended_tables[0]
                    masalar[table_number].durum =0
                    print(f"{self.adi} ücret ödendi.{masalar[table_number].musteriID} masaID: {masalar[table_number].masaID} masanın yeni durumu {masalar[table_number].durum}")
                    time.sleep(1)
                #else:
                    #print(f"{self.adi} müşteri gelmedi")
            time.sleep(1)
   


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
    global tables
    tables=None
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
    ascilar=[]
    threads = []
    ParaKasası=[]
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
    for i in range(1):
        kasa = Kasa(f"Kasa", masalar, mutex) 
        ParaKasası.append(kasa)

    for i in range(2):
        asci = Asci(f"Asci{i}", masalar, mutex) 
        ascilar.append(asci)
        
    for i in range(3):
        garson = Garson(f"Garson{i}", masalar, mutex)  # Assign a waiter to each table
        garsonlar.append(garson)    
        
    for musteriId in Totaliste:  # müşterileri tek tek dönecek
        yeni_musteri = Musteri(musteriId, semaphore, masalar,mutex,mutex1,musteriqueue)
        threads.append(yeni_musteri)
        #print(musteriId + "'in thread oluşturuldu")
        #yeni_musteri.start()  # Her müşteri geldiğinde yeni thread başlattık
     
    for garson in garsonlar+threads+ascilar+ParaKasası:
        garson.start()
       
    for thread in threads+garsonlar+ascilar+ParaKasası:
        thread.join()