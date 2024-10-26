import tkinter as  tk
from tkinter import ttk
from decimal import Decimal
from tkinter import messagebox
from tkinter import *
import xlsxwriter
import os
import re

class nivo():
    labels = ['Nokta No', 'Ara Uzaklıklar', 'Geri Okuma', 'Orta Okuma', 'İleri Okuma',
              'Yükseklik Farkı', 'Gözleme Düzlemi Kotu', 'Nokta Yükseklikleri']
    valueOfTemp = 0

    def __init__(self, valueOfTemp):
        self.valueOfTemp = int(valueOfTemp)
    def main(self):
        self.NOKTA_NO_INDEX = 0
        self.ARA_UZAKLIK_INDEX = 1
        self.GERİ_OKUMA_INDEX = 2
        self.ORTA_OKUMA_INDEX = 3
        self.İLERİ_OKUMA_INDEX = 4
        self.YÜKSEKLİK_FARKI = 5
        self.GDK = 6
        self.NOKTA_YÜKSEKLİKLERİ = 7

        self.win = tk.Tk()
        self.win.title('Açık Nivelman Hesabı')
        self.win.geometry("1162x300")
        self.win.resizable(0, 0)
        self.h_known = 1
        self.nokta_sayısı = self.valueOfTemp
        self.frame = Frame(self.win, width=1138, height=300, background='#EBEBEB')
        self.frame.grid()
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.frame, height=290, width=1138, background='#EBEBEB')
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#EBEBEB")
        self.canvas.create_window(0, 0, window=self.scrollable_frame, anchor='nw')

        self.scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scroll.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1, sticky="ns")

        self.scrollable_frame.bind("<Configure>", self.update_scrollregion)

        self.create_labels()
        self.create_table(self.nokta_sayısı, self.h_known)
        self.win.mainloop()

    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_labels(self):
        H1 = ttk.Label(self.scrollable_frame, text="Nokta Numarası/ Adı")
        H2 = ttk.Label(self.scrollable_frame, text="Ara Uzaklıklar (m)")
        H3 = ttk.Label(self.scrollable_frame, text="Geri Okuma (mm)")
        H4 = ttk.Label(self.scrollable_frame, text="Orta Okuma (mm)")
        H5 = ttk.Label(self.scrollable_frame, text="İleri Okuma (mm)")
        H6 = ttk.Label(self.scrollable_frame, text="Yükseklik Farkı (mm)")
        H7 = ttk.Label(self.scrollable_frame, text="Gözleme Düzlemi Kotu (mm)")
        H8 = ttk.Label(self.scrollable_frame, text="Nokta Yükseklikleri (m)")

        H1.grid(row=0, column=0, padx=10, pady=10)
        H2.grid(row=0, column=1, padx=10, pady=10)
        H3.grid(row=0, column=2, padx=10, pady=10)
        H4.grid(row=0, column=3, padx=10, pady=10)
        H5.grid(row=0, column=4, padx=10, pady=10)
        H6.grid(row=0, column=5, padx=10, pady=10)
        H7.grid(row=0, column=6, padx=10, pady=10)
        H8.grid(row=0, column=7, padx=10, pady=10)


    def create_table(self, nokta_sayısı, h_known):
        cols = 9
        nokta_sayısı += h_known-1
        rows = nokta_sayısı
        self.arr = [[0 for i in range(cols)] for j in range(rows)]

        for i in range(len(self.labels)):
            for j in range(h_known, nokta_sayısı + h_known):
                self.cur_entry = ttk.Entry(self.scrollable_frame , justify='center',  width = 15)
                self.arr[j - h_known][i] = self.cur_entry
                self.cur_entry.grid(row=j, column=i, sticky=tk.NSEW)

        self.calculate_button = ttk.Button(self.scrollable_frame, text="Hesapla", command=self.get_values)
        self.calculate_button.grid(row=self.nokta_sayısı + self.h_known + 3, column=1, padx=10, pady=10)

        self.reset_button = ttk.Button(self.scrollable_frame, text="Sıfırla", command=self.reset_values)
        self.reset_button.grid(row=self.nokta_sayısı + self.h_known + 3, column=3, padx=10, pady=10)

        self.export_button = ttk.Button(self.scrollable_frame, text="Kaydet (Excel)", command=self.create_excel)
        self.export_button.grid(row=self.nokta_sayısı + self.h_known + 3, column=5, padx=10, pady=10)

        self.quit_button = ttk.Button(self.scrollable_frame, text="Kapat", command=self.close_window)
        self.quit_button.grid(row=self.nokta_sayısı + self.h_known + 3, column=7, padx=10, pady=10)

        self.arr[0][self.ARA_UZAKLIK_INDEX].config(state='disabled')
        self.arr[0][self.ORTA_OKUMA_INDEX].config(state='disabled')
        self.arr[0][self.İLERİ_OKUMA_INDEX].config(state='disabled')
        self.arr[0][self.YÜKSEKLİK_FARKI].config(state='disabled')
        self.arr[rows-1][self.GERİ_OKUMA_INDEX].config(state='disabled')
        self.arr[rows-1][self.GDK].config(state='disabled')


    def close_window(self):
        self.scrollable_frame.destroy()
        self.win.destroy()

    def reset_values(self):
        self.create_table(self.nokta_sayısı, self.h_known)
        self.calculate_button.config(state = 'normal')

    def get_values(self):

        self.calculate_button.config(state = 'disabled')
        self.total_row = self.nokta_sayısı + self.h_known - 1
        self.yükseklik_farkı()
        self.kot_hesabı()
        self.GDK_hesabı()

    def contol(self):
        list = [0, self.nokta_sayısı + self.h_known - 1]
        list1 = [self.NOKTA_YÜKSEKLİKLERİ, self.NOKTA_YÜKSEKLİKLERİ]

        for k, item in enumerate(list1):

            if len(self.arr[list[k]][self.NOKTA_YÜKSEKLİKLERİ].get()) != 0:
                l = (self.arr[list[k]][self.NOKTA_YÜKSEKLİKLERİ].get())

                if not re.search("[0-9]", l):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[$#@]", l):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[A-Z]", l):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[a-z]", l):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("\s", l):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            else:
                messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
        for J in range(0, self.total_row - 1):
            if len(self.arr[J][self.GERİ_MESAFE].get()) != 0:
                c = (self.arr[J][self.GERİ_MESAFE].get())
                if not re.search("[0-9]", c):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[$#@]", c):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[A-Z]", c):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[a-z]", c):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("\s", c):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            elif len(self.arr[J][self.GERİ_OKUMA_INDEX].get()) != 0:
                b = (self.arr[J][self.GERİ_OKUMA_INDEX].get())
                if not re.search("[0-9]", b):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[$#@]", b):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[A-Z]", b):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[a-z]", b):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("\s", b):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            else:
                messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
        for i in range(1, self.total_row):
            if len(self.arr[i][self.İLERİ_MESAFE].get()) != 0:
                d = (self.arr[i][self.İLERİ_MESAFE].get())
                if not re.search("[0-9]", d):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[$#@]", d):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[A-Z]", d):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[a-z]", d):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("\s", d):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            elif len(self.arr[i][self.İLERİ_OKUMA_INDEX].get()) != 0:
                a = (self.arr[i][self.İLERİ_OKUMA_INDEX].get())
                if not re.search("[0-9]", a):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[$#@]", a):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[A-Z]", a):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("[a-z]", a):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                elif re.search("\s", a):
                    messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
            else:
                messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
    def create_excel(self):

        workbook = xlsxwriter.Workbook('açık_nivelman_çıktı.xlsx')

        worksheet = workbook.add_worksheet()
        cell_format3 = workbook.add_format({'bold': False, 'font_color': 'blue'})
        cell_format3.set_center_across()
        cell_format2 = workbook.add_format({'bold': False, 'font_color': 'black'})
        cell_format2.set_center_across()
        cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
        cell_format.set_center_across()
        worksheet.write_row(0, 1, self.labels,cell_format)
        worksheet.set_column(0, len(self.labels),17)

        nokta_numarası = []
        ara_uzaklık = []
        geri_okuma = []
        orta_okuma = []
        ileri_okuma = []
        yükseklik_farkı = []
        gdk = []
        nokta_yükseklikleri = []

        for i in range(1, self.total_row):
            ara_uzaklık.insert(i, float(self.arr[i][self.ARA_UZAKLIK_INDEX].get()))
            orta_okuma.insert(i, self.arr[i][self.ORTA_OKUMA_INDEX].get())
            ileri_okuma.insert(i, float(self.arr[i][self.İLERİ_OKUMA_INDEX].get()))
            yükseklik_farkı.insert(i, float(self.arr[i][self.YÜKSEKLİK_FARKI].get()))

        for i in range(0, self.total_row-1):
             geri_okuma.insert(i, float(self.arr[i][self.GERİ_OKUMA_INDEX].get()))
             gdk.insert(i, float(self.arr[i][self.GDK].get()))

        for i in range(0, self.total_row):
            nokta_numarası.insert(i, self.arr[i][self.NOKTA_NO_INDEX].get())
            nokta_yükseklikleri.insert(i, self.arr[i][self.NOKTA_YÜKSEKLİKLERİ].get())

        for row_num, data in enumerate(nokta_numarası):
            worksheet.write(row_num+1, 1, data,cell_format2)

        for row_num, data in enumerate(ara_uzaklık):
            worksheet.write(row_num+2, 2, data,cell_format2)
        for row_num, data in enumerate(geri_okuma):
            worksheet.write(row_num + 1, 3, data,cell_format2)
        for row_num, data in enumerate(orta_okuma):
            worksheet.write(row_num + 2, 4, data,cell_format2)
        for row_num, data in enumerate(ileri_okuma):
            worksheet.write(row_num+2, 5, data,cell_format2)
        for row_num, data in enumerate(yükseklik_farkı):
            worksheet.write(row_num + 2, 6, data,cell_format2)
        for row_num, data in enumerate(gdk):
            worksheet.write(row_num + 1, 7, data,cell_format2)
        for row_num, data in enumerate(nokta_yükseklikleri):
            worksheet.write(row_num + 1, 8, data,cell_format2)



        workbook.close()
        os.startfile('açık_nivelman_hesabı.xlsx')

    def yükseklik_farkı(self):

        for i in range(0, self.total_row-1):

            self.first_available=0
            self.second_available=0
            if len(self.arr[i][self.GERİ_OKUMA_INDEX].get())!= 0:
                self.first_available=float(self.arr[i][self.GERİ_OKUMA_INDEX].get())
            elif len(self.arr[i][self.ORTA_OKUMA_INDEX].get())!= 0:
                self.first_available = float(self.arr[i][self.ORTA_OKUMA_INDEX].get())


            if len(self.arr[i+1][self.GERİ_OKUMA_INDEX].get())!= 0:
                self.second_available=float(self.arr[i+1][self.GERİ_OKUMA_INDEX].get())
            if len(self.arr[i+1][self.ORTA_OKUMA_INDEX].get())!= 0:
                self.second_available = float(self.arr[i+1][self.ORTA_OKUMA_INDEX].get())
            if len(self.arr[i + 1][self.İLERİ_OKUMA_INDEX].get()) != 0:
                self.second_available = float(self.arr[i + 1][self.İLERİ_OKUMA_INDEX].get())

            self.diff_h=self.first_available-self.second_available
            self.arr[i + 1][self.YÜKSEKLİK_FARKI].insert(i, self.convert_number_to_float_3_digit((self.diff_h)))

    def kot_hesabı(self):
        for i in range(0, self.total_row-1):
            self.nokta_kotu = float(self.arr[i][self.NOKTA_YÜKSEKLİKLERİ].get()) + float(self.arr[i+1][self.YÜKSEKLİK_FARKI].get())/1000
            self.arr[i+1][self.NOKTA_YÜKSEKLİKLERİ].insert(i, self.convert_number_to_float_3_digit(self.nokta_kotu))

    def GDK_hesabı(self):
        for i in range(0, self.total_row-1):
            if len(self.arr[i][self.GERİ_OKUMA_INDEX].get())== 0:
                self.gdk = float(self.arr[i-1][self.GDK].get())
                self.arr[i][self.GDK].insert(i, self.convert_number_to_float_3_digit(self.gdk))
            else:
                self.gdk = float(self.arr[i][self.NOKTA_YÜKSEKLİKLERİ].get()) + float(self.arr[i][self.GERİ_OKUMA_INDEX].get())
                self.arr[i][self.GDK].insert(i, self.convert_number_to_float_3_digit(self.gdk))


    def convert_entry_to_float_3_digit(self, entry):
        return float("{0:.3f}".format(float(entry.get())))

    def convert_number_to_float_3_digit(self, entry):
        return float("{0:.3f}".format(float(entry)))

    def convert_entry_to_float_5_digit(self, entry):
        return float("{0:.5f}".format(float(entry.get())))

    def convert_number_to_float_5_digit(self, entry):
        return float("{0:.5f}".format(float(entry)))

if __name__ == '__main__':
    x = nivo()
    x.main()



