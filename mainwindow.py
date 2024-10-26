import tkinter as  tk
from tkinter import ttk
from Linked_Traverse import deneme
from Kapalı_poligon import deneme2
from açık_nivelman_hesabı import nivo
from bağlı_nivelman_hesabı import nivo_bağlı
from ed50_wgs84_transform import transform_ed50_wgs84
from wgs84_ed50_transform import transform_wgs84_ed50
from show_map import map
from show_map_2 import map2
import re
from tkinter import messagebox
from tkinter import Menu
import os

class mainwindow():
    def main(self):
        self.mainwindow = tk.Tk()
        #self.mainwindow.iconbitmap('C:/Users/Sina/Desktop/DesignProject/icon/main.ico')
        self.mainwindow.geometry("100x100+10+10")
        self.mainwindow.minsize(600, 400)
        self.mainwindow.title("GeoHesap")
        self.labelTop = tk.Label(self.mainwindow,
                            text="Modüller")
        self.labelTop.place( x=275, y=100, anchor='center')


        self.comboExample = ttk.Combobox(self.mainwindow,
                                    values=[
                                        "Seçim Yapınız",
                                        "Bağlı Poligon",
                                        "Kapalı Poligon",
                                        "Açık Nivelman",
                                        "Dayalı Nivelman",
                                        "ED50-WGS84 Dönüşümü",
                                        "WGS84-ED50 Dönüşümü",
                                        "Nokta Göster(Enlem, Boylam)",
                                        "Nokta Göster(Y,X/WGS84)"], state='readonly', justify='center')

        self.comboExample.current(0)
        self.comboExample.place( x=275, y=125, anchor='center')
        self.labelMid = tk.Label(self.mainwindow, text="Nokta Sayısını Giriniz")
        self.labelMid.place( x=275, y=150, anchor='center')
        self.cur_entry = ttk.Entry(self.mainwindow, justify='center', width=23)
        self.cur_entry.place( x=275, y=175, anchor='center')
        self.calculate_button = ttk.Button(self.mainwindow, text="Çalıştır", command=self.open_current)
        self.calculate_button.place( x=275, y=210, anchor='center')
        self.quit_button = ttk.Button(self.mainwindow, text="Kapat", command=self.close_window)
        self.quit_button.place( x=275, y=250, anchor='center')
        self.menü()
        self.mainwindow.mainloop()

    def close_window(self):
        self.mainwindow.destroy()

    def open_current(self):
        if  len(self.cur_entry.get()) != 0:
            a=(self.cur_entry.get())

            if not re.search("[0-9]",a) :
                messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            elif re.search("[$#@]",a):
                messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            elif re.search("[A-Z]",a):
                messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            elif re.search("[a-z]",a):
                messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            elif re.search("\s",a):
                messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            else:
                if self.comboExample.get() == "Bağlı Poligon":
                    pol_win = deneme(self.cur_entry.get())
                    pol_win.main()
                elif self.comboExample.get() == "Açık Nivelman":
                    pol_win = nivo(self.cur_entry.get())
                    pol_win.main()
                elif self.comboExample.get() == "Dayalı Nivelman":
                    pol_win = nivo_bağlı(self.cur_entry.get())
                    pol_win.main()
                elif self.comboExample.get() == "Kapalı Poligon":
                    pol_win = deneme2(self.cur_entry.get())
                    pol_win.main()
                elif self.comboExample.get() == "ED50-WGS84 Dönüşümü":
                    pol_win = transform_ed50_wgs84(self.cur_entry.get())
                    pol_win.main()
                elif self.comboExample.get() == "WGS84-ED50 Dönüşümü":
                    pol_win = transform_wgs84_ed50(self.cur_entry.get())
                    pol_win.main()
                elif self.comboExample.get() ==  "Nokta Göster(Y,X/WGS84)":
                    pol_win = map2(self.cur_entry.get())
                    pol_win.main()
                elif self.comboExample.get() == "Nokta Göster(Enlem, Boylam)":
                    pol_win = map(self.cur_entry.get())
                    pol_win.main()
                elif self.comboExample.get() == "Seçim Yapınız":
                    messagebox.showerror("DİKKAT", "Lütfen Modül Seçiniz")
                else:
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")

        else:
            messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
    def menü(self):
        menubar = Menu(self.mainwindow)
        file = Menu(menubar, tearoff=0)
        file.add_command(label="Bağlı Poligon", command=self.bağlı)
        file.add_command(label="Kapalı Poligon", command=self.kapalı)
        file.add_command(label="Açık Nivelman")
        file.add_command(label="Bağlı Nivelman", command=self.dayalı_nivo)
        file.add_command(label="ED50-WGS84 Dönüşümü", command=self.ed50)
        file.add_command(label="WGS84-ED50 Dönüşümü", command=self.wgs84)
        file.add_command(label="Nokta Göster(Enlem, Boylam)", command=self.lat_lon)
        file.add_command(label="Nokta Göster(Y,X/WGS84)", command=self.y_x)
        file.add_separator()

        file.add_command(label="Kapat", command=self.mainwindow.quit)

        menubar.add_cascade(label="Nasıl Kullanırım? ", menu=file)
        edit = Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Biz Kimiz? ", command=self.webpage)
        help = Menu(menubar, tearoff=0)


        self.mainwindow.config(menu=menubar)
        self.mainwindow.mainloop()
    def bağlı(self):
        os.startfile('Bağlı poligon.pdf')
    def kapalı(self):
        os.startfile('Kapalı Poligon.pdf')
    def ed50(self):
        os.startfile('ED-50_WGS84 Dönüşümü.pdf')
    def wgs84(self):
        os.startfile('WGS84_ED-50 Dönüşümü.pdf')
    def lat_lon(self):
        os.startfile('nokta_göster.pdf')
    def y_x(self):
        os.startfile('nokta_göster2.pdf')
    def dayalı_nivo(self):
        os.startfile('dayalınivelman.pdf')
    def webpage(self):
        os.startfile('Sabahattin_Demir.html')
        os.startfile('index.html')


    def send_mail(self):
        print("b")
if __name__ == '__main__':
    x = mainwindow()
    x.main()
