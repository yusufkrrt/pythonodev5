import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import hashlib

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metin Karşılaştırma Uygulaması")

        self.conn = sqlite3.connect('kullanıcılar.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS kullanıcılar (
            kullanıcı_adı TEXT PRIMARY KEY,
            şifre TEXT
        )
        ''')

        self.kullanıcı_adı = None
        self.giriş_ekranı()

    def giriş_ekranı(self):
        self.geometry("300x200")
        kullanıcı_adı_label = tk.Label(self, text="Kullanıcı Adı:")
        kullanıcı_adı_label.pack()
        self.kullanıcı_adı_entry = tk.Entry(self)
        self.kullanıcı_adı_entry.pack()
        şifre_label = tk.Label(self, text="Şifre:")
        self.şifre_entry = tk.Entry(self, show="*")
        şifre_label.pack()
        self.şifre_entry.pack()
        giriş_butonu = tk.Button(self, text="Giriş Yap", command=self.giriş_yap)
        giriş_butonu.pack()
        kaydol_butonu = tk.Button(self, text="Kaydol", command=self.kaydol)
        kaydol_butonu.pack()

    def kaydol(self):
        kullanıcı_adı = self.kullanıcı_adı_entry.get()
        şifre = self.şifre_entry.get()
        if not kullanıcı_adı or not şifre:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz.")
            return
        şifre_hash = hashlib.sha256(şifre.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM kullanıcılar WHERE kullanıcı_adı = ?", (kullanıcı_adı,))
        user = self.cursor.fetchone()
        if user:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten var.")
        else:
            self.cursor.execute("INSERT INTO kullanıcılar (kullanıcı_adı, şifre) VALUES (?, ?)", (kullanıcı_adı, şifre_hash))
            self.conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarılı! Artık giriş yapabilirsiniz.")

    def giriş_yap(self):
        kullanıcı_adı = self.kullanıcı_adı_entry.get()
        şifre = self.şifre_entry.get()
        if not kullanıcı_adı or not şifre:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz.")
            return
        şifre_hash = hashlib.sha256(şifre.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM kullanıcılar WHERE kullanıcı_adı = ? AND şifre = ?", (kullanıcı_adı, şifre_hash))
        user = self.cursor.fetchone()
        if user:
            messagebox.showinfo("Başarılı", "Giriş Başarılı!")
            self.kullanıcı_adı = kullanıcı_adı
            self.menü_ekranı()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")

    def menü_ekranı(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("300x200")
        karşılaştır_butonu = tk.Button(self, text="Karşılaştır", command=self.karşılaştır_menüsü)
        karşılaştır_butonu.pack()
        işlemler_butonu = tk.Button(self, text="İşlemler", command=self.işlemler_menüsü)
        işlemler_butonu.pack()
        çıkış_butonu = tk.Button(self, text="Çıkış", command=self.quit)
        çıkış_butonu.pack()

    def karşılaştır_menüsü(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("400x200")
        tk.Button(self, text="Kelime bazında Karşılaştır", command=lambda: self.karşılaştır_penceresi(self.kelime_benzerligi)).pack()
        tk.Button(self, text="Karakter bazında Karşılaştır", command=lambda: self.karşılaştır_penceresi(self.karakter_benzerligi)).pack()
        tk.Button(self, text="Geri", command=self.menü_ekranı).pack()

    def işlemler_menüsü(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("300x200")
        şifre_değiştir_butonu = tk.Button(self, text="Şifre Değiştir", command=self.şifre_değiştir_penceresi)
        şifre_değiştir_butonu.pack()
        geri_butonu = tk.Button(self, text="Geri", command=self.menü_ekranı)
        geri_butonu.pack()

    def şifre_değiştir_penceresi(self):
        if self.kullanıcı_adı is None:
            messagebox.showerror("Hata", "Şifre değiştirmek için giriş yapmalısınız.")
            return
        yeni_pencere = tk.Toplevel(self)
        yeni_pencere.title("Şifre Değiştir")
        yeni_şifre_label = tk.Label(yeni_pencere, text="Yeni Şifre:")
        yeni_şifre_entry = tk.Entry(yeni_pencere, show="*")
        yeni_şifre_label.pack()
        yeni_şifre_entry.pack()
        def değiştir():
            yeni_şifre = yeni_şifre_entry.get()
            if not yeni_şifre:
                messagebox.showerror("Hata", "Şifre boş olamaz.")
                return
            yeni_şifre_hash = hashlib.sha256(yeni_şifre.encode()).hexdigest()
            self.cursor.execute("UPDATE kullanıcılar SET şifre = ? WHERE kullanıcı_adı = ?", (yeni_şifre_hash, self.kullanıcı_adı))
            self.conn.commit()
            messagebox.showinfo("Başarılı", "Şifre başarıyla değiştirildi.")
            yeni_pencere.destroy()
        değiştir_butonu = tk.Button(yeni_pencere, text="Değiştir", command=değiştir)
        değiştir_butonu.pack()

    def karşılaştır_penceresi(self, karşılaştırma_fonksiyonu):
        yeni_pencere = tk.Toplevel(self)
        yeni_pencere.title("Metin Karşılaştır")
        tk.Label(yeni_pencere, text="Metin 1:").pack()
        metin1_entry = tk.Entry(yeni_pencere, width=50)
        metin1_entry.pack()
        tk.Label(yeni_pencere, text="Metin 2:").pack()
        metin2_entry = tk.Entry(yeni_pencere, width=50)
        metin2_entry.pack()

        tk.Button(yeni_pencere, text="Dosya Seç ve Kaydet (Metin 1)", command=lambda: self.dosya_seç_ve_kaydet(metin1_entry)).pack()
        tk.Button(yeni_pencere, text="Dosya Seç ve Kaydet (Metin 2)", command=lambda: self.dosya_seç_ve_kaydet(metin2_entry)).pack()
        tk.Button(yeni_pencere, text="Karşılaştır", command=lambda: self.karşılaştır_ve_göster(karşılaştırma_fonksiyonu, metin1_entry.get(), metin2_entry.get())).pack()

    def dosya_seç_ve_kaydet(self, entry):
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if dosya_yolu:  # Dosya yolu seçildiyse
            with open(dosya_yolu, 'w', encoding='utf-8') as file:
                metin = entry.get()
                file.write(metin)
            entry.delete(0, tk.END)
            entry.insert(0, dosya_yolu)

    def karşılaştır_ve_göster(self, karşılaştırma_fonksiyonu, metin1_yolu, metin2_yolu):
        try:
            with open(metin1_yolu, 'r', encoding='utf-8') as file1:
                metin1 = file1.read()
            with open(metin2_yolu, 'r', encoding='utf-8') as file2:
                metin2 = file2.read()

            sonuç, kesisim, birlesim = karşılaştırma_fonksiyonu(metin1, metin2)
            sonuç_mesajı = f"Benzerlik Oranı: {sonuç:.2f}\nKesişim: {kesisim}\nBirleşim: {birlesim}"
            messagebox.showinfo("Karşılaştırma Sonucu", sonuç_mesajı)
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya okuma hatası: {e}")


    def kelime_benzerligi(self, metin1, metin2):
        from collections import Counter

        kelimeler1 = Counter(metin1.lower().split())
        kelimeler2 = Counter(metin2.lower().split())

        kesisim = sum((kelimeler1 & kelimeler2).values()) 
        toplam = sum((kelimeler1 | kelimeler2).values())  

        if toplam == 0:
            return 0, kesisim, toplam  

        benzerlik_oranı = kesisim / toplam
        return benzerlik_oranı, kesisim, toplam


    def karakter_benzerligi(self, metin1, metin2):
        from collections import Counter

        kume1 = Counter(metin1.lower().replace(" ", ""))
        kume2 = Counter(metin2.lower().replace(" ", ""))

        kesisim = sum((kume1 & kume2).values())  # Kesişimdeki karakter sayısını al
        toplam = sum((kume1 | kume2).values())  # Toplam benzersiz karakter sayısını al

        if toplam == 0:
            return 0, kesisim, toplam  # Eğer toplam 0 ise, bölme hatası önlemek için 0 döndür

        benzerlik_oranı = kesisim / toplam
        return benzerlik_oranı, kesisim, toplam


if __name__ == "__main__":
    app = App()
    app.mainloop()
