from asyncio import Semaphore
from itertools import count
from operator import index
import threading
import time
import tkinter as tk
from Arayuz import Arayuz
import random


class Musteri(threading.Thread):
    def __init__(self, musteriID, semaphore, masalar,mutex,mutex1,musteriqueue,start_time):
        threading.Thread.__init__(self)
        self.musteriID = musteriID
        self.semaphore = semaphore
        self.masalar = masalar
        self.musteriqueue=musteriqueue
        self.start_time=start_time
    def masa_ara(self,masalar):
        for x in range(6):
            if(masalar[x].durum==0):
                return 1
            
        
    def run(self):

        while True:
            with mutex:
                # masa bloklandı....
                unoccupied_tables = [table_number for table_number, table in enumerate(masalar) if masalar[table_number].durum == 0]
                
                if unoccupied_tables:
                    table_number = unoccupied_tables[0]
                    masalar[table_number].musteriID = self.musteriID
                    masalar[table_number].durum = 1  # masa dolu olunca 1
                    print(
                                f"{masalar[table_number].masaID}"
                                + " kilitlendi."
                                + f"{masalar[table_number].musteriID}"
                                + " geldi."
                                + f"{table_number}"
                                
                    )
                    sayi=random.uniform(1,2)
                    time.sleep(sayi)
                    break
                else:
                    end_time = time.time() 
                    gecen_zaman=end_time-start_time
                    if(gecen_zaman>60):
                        print(f"bu kadar zaman geçti : {gecen_zaman} ancak hala masa bulamadı.  {self.musteriID} gitti")
                        unoccupied_tables.remove(unoccupied_tables[0])# ynilemeden dolayı burada bir hata veriyor root.after() fonskiyonundan dolayı
                    print(f"Müşteriler için boş masa yok bu müşteriler bekliyor-> {self.musteriID} geçen zaman{gecen_zaman}")    #bekleyen müşteriler
                
    
            time.sleep(1)
        


                



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
                time.sleep(3)
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
        time.sleep(1)
        
        while True:
            with mutex:
                unattended_tables = [table_number for table_number, table in enumerate(masalar) if masalar[table_number].durum == 3]

                if unattended_tables:
                    table_number = unattended_tables[0]
                    masalar[table_number].durum =4
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

class musteriTimer:
    def __init__(self, musteriID, timer):
        self.musteriID = musteriID
        self.timer = time
        

def update_label():
    sayac=0
    garson_ids = [masalar[sayac].musteriID for sayac, table in enumerate(masalar) if masalar[sayac].durum ==2]

    asci_ids = [masalar[sayac].musteriID for sayac, table in enumerate(masalar) if masalar[sayac].durum ==3]

    kasa_ids = [masalar[sayac].musteriID for sayac, table in enumerate(masalar) if masalar[sayac].durum ==4]

    customer_ids = [masalar[sayac].musteriID for sayac, table in enumerate(masalar) if masalar[sayac].durum ==1]

    
    label.config(text=f"Musteri ID: {', '.join(map(str, customer_ids))}")
    label1.config(text=f"Garson: {', '.join(map(str, garson_ids))}")
    label2.config(text=f"Aşçı: {', '.join(map(str, asci_ids))}")
    label3.config(text=f"Kasa: {', '.join(map(str, kasa_ids))}")
    root.after(1, update_label)  # bir süre sonra güncellemede hata veriyor
 
index = 6
if __name__ == "__main__":
    mutex = threading.Lock()
    mutex1= threading.Lock()
    mutex2 = threading.Lock()
    global tables
    tables=None
    baslamaDurumu=False
    oncelikli_musteri=0
    standart_musteri=0
    arayuz = Arayuz()
    arayuz.baslat()
       # Create a Tkinter window
    root = tk.Tk()
    root.geometry("1000x500")

    root.title("Restoran Yonetim Sistemi")

    label = tk.Label(root, text="")
    label1 = tk.Label(root, text="")
    label2= tk.Label(root, text="")
    label3 = tk.Label(root, text="")
    label.pack()
    label1.pack()
    label2.pack()
    label3.pack()

#müşteri sayisinı alıp burada sıralama yapılacak
    onceliksayisi=int(input("Öncelikli müşteri sayısı giriniz:"))
    normalsayisi=int(input("Standart müşteri sayısı giriniz:"))
    Liste = ["a", "b", "c", "d", "e"]
    Liste2 = ["f", "g", "h", "k", "y1", "y2"]
    Liste3 = ["l", "m", "y3"]
    Totaliste = Liste + Liste2 + Liste3

    masa_sayisi = 6
    garson_sayisi = 3
    asci_sayisi = 2
               
    

    masa_sayisi = 6
    semaphore = threading.Semaphore(masa_sayisi)  # Masa sayısı kadar semaphore oluştur

    masalar = []
    garsonlar = []
    ascilar=[]
    threads = []
    ParaKasası=[]
    timer=[]
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
        start_time = time.time()  # Capture the start time

        yeni_musteri = Musteri(musteriId, semaphore, masalar,mutex,mutex1,musteriqueue,start_time)
        time_musteri=musteriTimer(musteriId,0)
        timer.append(time_musteri)
        threads.append(yeni_musteri)
        #print(musteriId + "'in thread oluşturuldu")
        #yeni_musteri.start()  # Her müşteri geldiğinde yeni thread başlattık
    time.sleep(2)
    for garson in garsonlar+threads+ascilar+ParaKasası:
        garson.start()
 
    
    root.after(1, update_label)
    root.mainloop()

    for thread in threads+garsonlar+ascilar+ParaKasası:
        thread.join()