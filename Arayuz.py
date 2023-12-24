import tkinter as tk
import time


class Arayuz:
    def __init__(self):
        
        self.pencere = tk.Tk()

        self.pencere.title("Restoran Yonetim Sistemi")

        self.text_var = tk.StringVar()

        """
        etiket = tk.Label(
            pencere,
            text="Ben Bir Etiketim",
            font="Tahoma 24",
            bg="blue",
            fg="white",
            wraplength=150
        )

        etiket.pack()
        etiket1 = tk.Label(pencere, text="Etiket1")
        etiket1.place(x = 25, y = 25)
        """

        
        def buton1_tikla():
            time.sleep(1)
            
               
            

        giris = tk.Entry(self.pencere, width=50)
        giris.insert(string="Müşteri Gelme Aralığı:", index=0)
        giris.pack()
        musterigelmearaligi = giris.get()

        giris1 = tk.Entry(self.pencere, width=50)
        giris1.insert(string="Toplam Süre:", index=0)
        giris1.pack()
        totalsure = giris1.get()


        self.pencere.geometry("1000x500")

        # Butonlar oluşturma
        buton1 = tk.Button(self.pencere, text="Start", command=buton1_tikla)
        buton1.pack(pady=10)


        
        # Etiket oluşturma 
        etiket = tk.Label(self.pencere, textvariable=self.text_var)
        etiket.pack(pady=10)

    def ekle_yazi(self, yazi):
        self.text_var.set(self.text_var.get() + yazi)

    def baslat(self):
        # Pencereyi başlatma
        self.pencere.mainloop()
