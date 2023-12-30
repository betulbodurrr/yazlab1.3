from ast import unaryop
from asyncio import Semaphore
from itertools import count
from operator import index
import threading
import time
import tkinter as tk
from Arayuz import Arayuz
import random
from PIL import Image,ImageTk

class Semaphore:
    def __init__(self, initial):
        self.signal_count = initial
        self.condition = threading.Condition() 

    def wait(self):
        with self.condition: 
            while self.signal_count <= 0:
                self.condition.wait() 
            self.signal_count -= 1 

    def signal(self):
        with self.condition:
            self.signal_count += 1 
            self.condition.notify()
    
    def signaln(self,n):
        with self.condition:
            self.signal_count+=n
            for _ in range(n):
                self.condition.notify()
            
    def value(self):
        return self.signal_count 


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
        musteriqueue.wait()# 3 müşteri gelir
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

                    renk_degistir_m(table_number)
                    butonlar[table_number].config(text=masalar[table_number].musteriID)
                    unoccupied_tables.pop(0)
                    time.sleep(2)
                    break
                else:
                    end_time = time.time() 
                    gecen_zaman=end_time-start_time
                    if(gecen_zaman>60):
                        print(f"bu kadar zaman geçti : {gecen_zaman} ancak hala masa bulamadı.  {self.musteriID} gitti")
                        #unoccupied_tables.remove(unoccupied_tables[0])# ynilemeden dolayı burada bir hata veriyor root.after() fonskiyonundan dolayı
                        if unoccupied_tables:
                        
                            unoccupied_tables.pop(0)
                        break
                    #print(f"Müşteriler için boş masa yok bu müşteriler bekliyor-> {self.musteriID} geçen zaman{gecen_zaman}")    #bekleyen müşteriler
        garsonqueue.signal()
   

class Garson(threading.Thread):
    def __init__(self, adi, masalar, mutex):
        threading.Thread.__init__(self)
        self.adi = adi
        self.masalar = masalar
        self.mutex = mutex


    def run(self):
        garsonqueue.wait()

        while True:
            with mutex:
                unattended_tables = [table_number for table_number, table in enumerate(masalar) if masalar[table_number].durum == 1]
                #print(f"{unattended_tables} bu masalarda müşteri var garson yok")

                if unattended_tables :
                    table_number = unattended_tables[0]
                    print(f"{self.adi} yemek {masalar[table_number].musteriID}'nin' siparişi alıyor masaID: {masalar[table_number].masaID}")
                    renk_degistir_g(table_number)
                    butonlar[table_number].config(text=masalar[table_number].musteriID)
                    if(table_number<3):
                        masano = tk.Label(root, text=f"Garson:{self.adi}")
                        masano.place(x=masalar[table_number].masaID*170+10,y=140)
                    else:
                        masano = tk.Label(root, text=f"Garson:{self.adi}")
                        masano.place(x=(masalar[table_number].masaID-3)*170+10,y=310)
                    time.sleep(2)
                    if(table_number<3):
                        masano = tk.Label(root, text="Garson:--------")
                        masano.place(x=masalar[table_number].masaID*170+10,y=140)
                    else:
                        masano = tk.Label(root, text="Garson:--------")
                        masano.place(x=(masalar[table_number].masaID-3)*170+10,y=310)
                    #renk_degistir_gb(table_number)
                    masalar[table_number].durum = 2  
                    print(f"{self.adi} yemek {masalar[table_number].musteriID}'nin' siparişi aldı. masaID: {masalar[table_number].masaID}")
                    unattended_tables.pop(0)
                    
                else:

                    print(f"{self.adi} müşteri bekliyor ")
                    
            time.sleep(1)
            musteriqueue.signaln(2)    
            asciqueue.signal()



class Asci(threading.Thread):
    def __init__(self, adi, masalar, mutex):
        threading.Thread.__init__(self)
        self.adi = adi
        self.masalar = masalar
        self.mutex = mutex

    def run(self):
        asciqueue.wait()

        while True:
            with mutex:
                unattended_tables = [table_number for table_number, table in enumerate(masalar) if masalar[table_number].durum == 2]
                if unattended_tables:
                    table_number = unattended_tables[0]
                    
                    print(f"{self.adi} yemek yapıyor.{masalar[table_number].musteriID} masaID: {masalar[table_number].masaID} masa no: {table_number}")
                    renk_degistir_a(table_number)
                    butonlar[table_number].config(text=masalar[table_number].musteriID)
                    renk_degistir_a(table_number)
                    butonlar[table_number].config(text=masalar[table_number].musteriID)
                    if(table_number<3):
                        masano = tk.Label(root, text=f"Aşçı:{self.adi}")
                        masano.place(x=masalar[table_number].masaID*170+10,y=120)
                    else:
                        masano = tk.Label(root, text=f"Aşçı:{self.adi}")
                        masano.place(x=(masalar[table_number].masaID-3)*170+10,y=290)    
                    time.sleep(3)
                    if(table_number<3):
                        masano = tk.Label(root, text="Aşçı:-----")
                        masano.place(x=masalar[table_number].masaID*170+10,y=120)
                    else:
                        masano = tk.Label(root, text="Aşçı:-----")
                        masano.place(x=(masalar[table_number].masaID-3)*170+10,y=290)   
                    #renk_degistir_ab(table_number)
                    masalar[table_number].durum = 3 
                    print(f"{self.adi} yemek yaptı.{masalar[table_number].musteriID} masaID: {masalar[table_number].masaID}")
                    unattended_tables.pop(0)

                #else:
                    #print(f"{self.adi} müşteri bekliyor ")
            kasaqueue.signal()
   

            time.sleep(1)

class Kasa(threading.Thread):
    def __init__(self, adi, masalar, mutex):
        threading.Thread.__init__(self)
        self.adi = adi
        self.masalar = masalar
        self.mutex = mutex

    def run(self):
        kasaqueue.wait()
        while True:
            with mutex:
                unattended_tables = [table_number for table_number, table in enumerate(masalar) if masalar[table_number].durum == 3]

                if unattended_tables:
                    table_number = unattended_tables[0]
                    masalar[table_number].durum =4
                    renk_degistir_k(table_number)
                    butonlar[table_number].config(text=masalar[table_number].musteriID)
                    
                    time.sleep(1)
                    renk_degistir_k(table_number)
                    butonlar[table_number].config(text="BOŞ")
                    masalar[table_number].durum =0
                    
                    print(f"{self.adi} ücret ödendi.{masalar[table_number].musteriID} masaID: {masalar[table_number].masaID} masanın yeni durumu {masalar[table_number].durum}")
                    unattended_tables.pop(0)
                #else:
                    #print(f"{self.adi} müşteri gelmedi")
            asciqueue.signal()
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
    
    customer_ids = [masalar[sayac].musteriID for sayac, table in enumerate(masalar) if masalar[sayac].durum ==1]
 
            
    garson_ids = [masalar[sayac].musteriID for sayac, table in enumerate(masalar) if masalar[sayac].durum ==2]
   
    asci_ids = [masalar[sayac].musteriID for sayac, table in enumerate(masalar) if masalar[sayac].durum ==3]
    

    kasa_ids = [masalar[sayac].musteriID for sayac, table in enumerate(masalar) if masalar[sayac].durum ==4]
  
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
    
    global ekransayac
    ekransayac=0
    tables=None
    baslamaDurumu=False
    oncelikli_musteri=0
    standart_musteri=0
    arayuz = Arayuz()
       # Create a Tkinter window
    root = tk.Tk()
    root.geometry("1000x500")
    root.title("Restoran Yonetim Sistemi")
  

    def renk_degistir_m(index):
        butonlar[index].config(bg="blue")  # Rengi değiştir
    def renk_degistir_g(index):
        butonlar[index].config(bg="green")  # Rengi değiştir
    def renk_degistir_a(index):
        butonlar[index].config(bg="red")  # Rengi değiştir
    def renk_degistir_k(index):
        butonlar[index].config(bg="brown")  # Rengi değiştir
    
    def renk_degistir_gb(index):
        butonlar[index].config(bg="cyan")  # Rengi değiştir
    def renk_degistir_ab(index):
        butonlar[index].config(bg="pink")  # Rengi değiştir
  

    global butonlar
    butonlar = []
    

    # Üst butonlar
    for i in range(3):
        buton = tk.Button(root, text=f"-", width=15, height=5)
        buton.place(x=i * 170 + 10, y=10)  # x ve y koordinatları
        
        masano = tk.Label(root, text=f"MasaID:{i}")
        
        masano.place(x=i*170+10,y=10)
        butonlar.append(buton)

    # Alt butonlar
    for i in range(3):
        buton = tk.Button(root, text=f"-", width=15, height=5)
        buton.place(x=i * 170 + 10, y=180)  # x ve y koordinatları
        masano = tk.Label(root, text=f"MasaID:{i+3}")
        masano.place(x=i*170+10,y=180)
        butonlar.append(buton)

    label = tk.Label(root, text="")
    label1 = tk.Label(root, text="")
    label2= tk.Label(root, text="")
    label3 = tk.Label(root, text="")
    label.place(x=500,y=50)
    label1.place(x=500,y=80)
    label2.place(x=500,y=110)
    label3.place(x=500,y=140)

#müşteri sayisinı alıp burada sıralama yapılacak
    print("1.Adım Müşeri Bilgisi")
    onceliksayisi1=int(input("Öncelikli müşteri sayısı giriniz:"))
    normalsayisi1=int(input("Standart müşteri sayısı giriniz:"))
    print("2.Adım Müşeri Bilgisi")    
    onceliksayisi2=int(input("Öncelikli müşteri sayısı giriniz:"))
    normalsayisi2=int(input("Standart müşteri sayısı giriniz:"))
    print("3.Adım Müşeri Bilgisi")    
    onceliksayisi3=int(input("Öncelikli müşteri sayısı giriniz:"))
    normalsayisi3=int(input("Standart müşteri sayısı giriniz:"))
    """
    Liste = ["a", "b", "c", "d", "e"]
    Liste2 = ["f", "g", "h", "k", "y1", "y2"]
    Liste3 = ["l", "m", "y3"]
    Totaliste = Liste + Liste2 + Liste3
    """
    masa_sayisi = 6
    garson_sayisi = 3
    asci_sayisi = 2
    def oncelikliOlanlariBasaGetir(musteriListesi):
        for i in range(len(musteriListesi)):
            for j in range(i+1,len(musteriListesi)):
                if(musteriListesi[i][0] == '0' and musteriListesi[j][0] == '1'):
                    temp = musteriListesi[i]
                    musteriListesi[i] = musteriListesi[j]
                    musteriListesi[j] = temp
    
        return musteriListesi
    def musteri_olustur(onceliksayisi1,normalsayisi1,onceliksayisi2,normalsayisi2,onceliksayisi3,normalsayisi3):
        Liste=[]
        Liste2=[]
        Liste3=[]
        Liste4=[]
        Liste5=[]
        Liste6=[]
        for i in range(onceliksayisi1):
            Liste.append(f"1Müşteri{i}1")
        for i in range(normalsayisi1):    
            Liste2.append(f"0Müşteri{i}1")
        for i in range(onceliksayisi2):
            Liste.append(f"1Müşteri{i}2")
        for i in range(normalsayisi2):    
            Liste2.append(f"0Müşteri{i}2")
        for i in range(onceliksayisi3):
            Liste.append(f"1Müşteri{i}3")
        for i in range(normalsayisi3):    
            Liste2.append(f"0Müşteri{i}3")    

        Totaliste = oncelikliOlanlariBasaGetir(Liste) + oncelikliOlanlariBasaGetir(Liste2)+oncelikliOlanlariBasaGetir(Liste3) + oncelikliOlanlariBasaGetir(Liste4)+oncelikliOlanlariBasaGetir(Liste5) + oncelikliOlanlariBasaGetir(Liste6) 
        return Totaliste
    masaGrupları = []
    Totaliste=musteri_olustur(onceliksayisi1,normalsayisi1,onceliksayisi2,normalsayisi2,onceliksayisi3,normalsayisi3)
    def otur():
        if len(Totaliste)>6:
            Totaliste[0:6] = oncelikliOlanlariBasaGetir(Totaliste[0:6])
            masaGrupları.append(Totaliste[0:6])
            Totaliste[0:6] = []
        else:
            masaGrupları.append(Totaliste[0:len(Totaliste)])  
            Totaliste[0:len(Totaliste)] = []
 
    while len(Totaliste) > 0:
        otur()

    for eleman in masaGrupları:
        Totaliste += eleman
        print(eleman)     

    print(Totaliste)

    masa_sayisi = 6
    semaphore = threading.Semaphore(masa_sayisi)  # Masa sayısı kadar semaphore oluştur

    masalar = []
    garsonlar = []
    ascilar=[]
    threads = []
    ParaKasası=[]
    timer=[]
    global musteriqueue,garsonqueue,asciqueue,kasaqueue
    musteriqueue, garsonqueue, asciqueue, kasaqueue = (
        Semaphore(6),
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
    """
    for garson in garsonlar+threads+ascilar+ParaKasası:  #bu olduğunda tüm müşterileri bekliyor sonra çıkıyorlar
            garson.join()    
 """
