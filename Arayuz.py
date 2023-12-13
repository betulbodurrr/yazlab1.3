import tkinter as tk

class Arayuz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restoran Yonetim Sistemi")

        self.text_var = tk.StringVar()

        # Butonlara tıklanınca çalışacak fonksiyonları tanımlama
        def buton1_tikla():
            self.ekle_yazi("Buton 1 tıklandı!\n")

        def buton2_tikla():
            self.ekle_yazi("Buton 2 tıklandı!\n")

        def buton3_tikla():
            self.ekle_yazi("Buton 3 tıklandı!\n")

        # Butonlar oluşturma
        buton1 = tk.Button(self.root, text="Buton 1", command=buton1_tikla)
        buton1.pack(pady=10)

        buton2 = tk.Button(self.root, text="Buton 2", command=buton2_tikla)
        buton2.pack(pady=10)

        buton3 = tk.Button(self.root, text="Buton 3", command=buton3_tikla)
        buton3.pack(pady=10)

        # Etiket oluşturma (eklenen yazıları göstermek için)
        etiket = tk.Label(self.root, textvariable=self.text_var)
        etiket.pack(pady=10)

    def ekle_yazi(self, yazi):
        self.text_var.set(self.text_var.get() + yazi)

    def baslat(self):
        # Pencereyi başlatma
        self.root.mainloop()
