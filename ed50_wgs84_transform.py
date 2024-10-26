import tkinter as  tk
from tkinter import ttk
from decimal import Decimal
from tkinter import messagebox
from tkinter import *
import xlsxwriter
import os
import math
from pyproj import Proj,transform
import folium


class transform_ed50_wgs84():
    labels = ['Nokta No', 'X Koordinatı (WGS84)', 'Y Koordinatı (WGS84)', 'Z Koordinatı (WGS84)',
              'X Koordinatı (ED50)', 'Y Koordinatı (ED50)', 'Z Koordinatı (ED50)']
    valueOfTemp = 0

    def __init__(self, valueOfTemp):
        self.valueOfTemp = int(valueOfTemp)
    def main(self):
        self.NOKTA_ADI = 0
        self.X_KOORDİNATI_ED50 = 1
        self.Y_KOORDİNATI_ED50 = 2
        self.Z_KOORDİNATI_ED50 = 3
        self.X_KOORDİNATI_WGS84 = 4
        self.Y_KOORDİNATI_WGS84 = 5
        self.Z_KOORDİNATI_WGS84 = 6

        self.win = tk.Tk()
        self.win.title('ED50-WGS84 Datum Dönüşümü (3B Kartezyen)')
        self.win.geometry("1032x300")
        self.win.resizable(0, 0)

        self.nokta_sayısı = self.valueOfTemp

        self.frame = Frame(self.win, width=1010, height=300, background='#EBEBEB')
        self.frame.grid()
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self.frame, height=295, width=1010, background='#EBEBEB')
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#EBEBEB")
        self.canvas.create_window(0, 0, window=self.scrollable_frame, anchor='nw')

        self.scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scroll.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1, sticky="ns")

        self.scrollable_frame.bind("<Configure>", self.update_scrollregion)

        self.create_labels()
        self.create_table(self.nokta_sayısı)
        self.win.mainloop()

    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_labels(self):
        H1 = ttk.Label(self.scrollable_frame, text="Nokta Numarası/Adı")
        H2 = ttk.Label(self.scrollable_frame, text='X Koordinatı (ED50)')
        H3 = ttk.Label(self.scrollable_frame, text='Y Koordinatı (ED50)')
        H4 = ttk.Label(self.scrollable_frame, text='Z Koordinatı (ED50)')
        H5 = ttk.Label(self.scrollable_frame, text='X Koordinatı (WGS84)')
        H6 = ttk.Label(self.scrollable_frame, text='Y Koordinatı (WGS84)')
        H7 = ttk.Label(self.scrollable_frame, text='Z Koordinatı (WGS84)')

        H1.grid(row=0, column=0, padx=10, pady=10)
        H2.grid(row=0, column=1, padx=10, pady=10)
        H3.grid(row=0, column=2, padx=10, pady=10)
        H4.grid(row=0, column=3, padx=10, pady=10)
        H5.grid(row=0, column=4, padx=10, pady=10)
        H6.grid(row=0, column=5, padx=10, pady=10)
        H7.grid(row=0, column=6, padx=10, pady=10)

    def create_table(self, nokta_sayısı):
        cols = 7
        rows = nokta_sayısı+1
        self.arr = [[0 for i in range(cols)] for j in range(rows)]

        for i in range(len(self.labels)):
            for j in range(1, nokta_sayısı+1):
                self.cur_entry = ttk.Entry(self.scrollable_frame, justify='center', width=15)
                self.arr[j][i] = self.cur_entry
                self.cur_entry.grid(row=j, column=i, sticky=tk.NSEW)

        self.calculate_button = ttk.Button(self.scrollable_frame, text="Dönüştür", command=self.get_values)
        self.calculate_button.grid(row=self.nokta_sayısı + 3, column=0, padx=10, pady=10)

        self.reset_button = ttk.Button(self.scrollable_frame, text="Sıfırla", command=self.reset_values)
        self.reset_button.grid(row=self.nokta_sayısı + 3, column=2, padx=10, pady=10)
        self.map_button = ttk.Button(self.scrollable_frame, text="Nokta Göster", command=self.create_map)
        self.map_button.grid(row=self.nokta_sayısı + 3, column=3, padx=10, pady=10)

        self.export_button = ttk.Button(self.scrollable_frame, text="Kaydet (Excel)", command=self.create_excel)
        self.export_button.grid(row=self.nokta_sayısı + 3, column=4, padx=10, pady=10)

        self.quit_button = ttk.Button(self.scrollable_frame, text="Kapat", command=self.close_window)
        self.quit_button.grid(row=self.nokta_sayısı + 3, column=6, padx=10, pady=10)

    def close_window(self):
        self.scrollable_frame.destroy()
        self.win.destroy()

    def reset_values(self):
        self.create_table(self.nokta_sayısı)
        self.calculate_button.config(state = 'normal')

    def get_values(self):
        self.calculate_button.config(state='disabled')
        self.dönüştür(self.nokta_sayısı)

    def dönüştür(self, nokta_sayısı):
        #Fırat ve Lenk (2002), Ayhan ve diğ. (2002)
        self.eps_x = (-0.0183/3600)*(math.pi/360)
        self.eps_y = (0.0003/3600)*(math.pi/360)
        self.eps_z = (-0.4528/3600)*(math.pi/360)
        self.t_x = -84.831
        self.t_y = -101.656
        self.t_z = -129.463
        self.k = (0.9498/1000000)

        for i in range(1, nokta_sayısı+1):
            self.x_wgs84 = float(self.arr[i][self.X_KOORDİNATI_ED50].get()) + float(self.arr[i][self.Y_KOORDİNATI_ED50].get())*self.eps_z - float(self.arr[i][self.Z_KOORDİNATI_ED50].get())*self.eps_y + float(self.arr[i][self.X_KOORDİNATI_ED50].get())*self.k + self.t_x
            self.arr[i][self.X_KOORDİNATI_WGS84].insert(i, self.convert_number_to_float_5_digit(self.x_wgs84))

            self.y_wgs84 = -(float(self.arr[i][self.X_KOORDİNATI_ED50].get())*self.eps_z) + float(self.arr[i][self.Y_KOORDİNATI_ED50].get()) + float(self.arr[i][self.Z_KOORDİNATI_ED50].get())*self.eps_x + float(self.arr[i][self.Y_KOORDİNATI_ED50].get())*self.k + self.t_y
            self.arr[i][self.Y_KOORDİNATI_WGS84].insert(i, self.convert_number_to_float_5_digit(self.y_wgs84))

            self.z_wgs84 = float(self.arr[i][self.X_KOORDİNATI_ED50].get())*self.eps_y - float(self.arr[i][self.Y_KOORDİNATI_ED50].get())*self.eps_x + float(self.arr[i][self.Z_KOORDİNATI_ED50].get()) + float(self.arr[i][self.Z_KOORDİNATI_ED50].get())*self.k + self.t_z
            self.arr[i][self.Z_KOORDİNATI_WGS84].insert(i, self.convert_number_to_float_5_digit(self.z_wgs84))

    def create_excel(self):

        workbook = xlsxwriter.Workbook('ED50-WGS84_Dönüşüm.xlsx')

        worksheet = workbook.add_worksheet()
        cell_format3 = workbook.add_format({'bold': False, 'font_color': 'blue'})
        cell_format3.set_center_across()
        cell_format2 = workbook.add_format({'bold': False, 'font_color': 'black'})
        cell_format2.set_center_across()
        cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
        cell_format.set_center_across()
        worksheet.write_row(0, 1, self.labels,cell_format)
        worksheet.set_column(0, len(self.labels),15)

        nokta_numarası = []
        X_ED50 = []
        Y_ED50 = []
        Z_ED50 = []
        X_WGS84 = []
        Y_WGS84 = []
        Z_WGS84 = []

        for i in range(1, self.nokta_sayısı+1):
            nokta_numarası.insert(i, self.arr[i][self.NOKTA_ADI].get())
            X_ED50.insert(i, self.arr[i][self.X_KOORDİNATI_ED50].get())
            Y_ED50.insert(i, self.arr[i][self.Y_KOORDİNATI_ED50].get())
            Z_ED50.insert(i, self.arr[i][self.Z_KOORDİNATI_ED50].get())
            X_WGS84.insert(i, self.arr[i][self.X_KOORDİNATI_WGS84].get())
            Y_WGS84.insert(i, self.arr[i][self.Y_KOORDİNATI_WGS84].get())
            Z_WGS84.insert(i, self.arr[i][self.Z_KOORDİNATI_WGS84].get())

        for row_num, data in enumerate(nokta_numarası):
            worksheet.write(row_num + 1, 1, data,cell_format2)
        for row_num, data in enumerate(X_ED50):
            worksheet.write(row_num + 1, 2, data,cell_format2)
        for row_num, data in enumerate(Y_ED50):
            worksheet.write(row_num + 1, 3, data,cell_format2)
        for row_num, data in enumerate(Z_ED50):
            worksheet.write(row_num + 1, 4, data,cell_format2)
        for row_num, data in enumerate(X_WGS84):
            worksheet.write(row_num + 1, 5, data,cell_format2)
        for row_num, data in enumerate(Y_WGS84):
            worksheet.write(row_num + 1, 6, data,cell_format2)
        for row_num, data in enumerate(Z_WGS84):
            worksheet.write(row_num + 1, 7, data,cell_format2)

        workbook.close()
        os.startfile('ED50-WGS84_Dönüşüm.xlsx')
    def create_map(self):
        # Create map object

        intProj = Proj(init='epsg:5255')
        outProj = Proj(init='epsg:4326')
        x_coord = []
        x_coord2 = []
        y_coord = []
        y_coord2 = []
        # Global tooltip
        m = folium.Map(location=[39.925054, 32.836943], zoom_start=10)
        tooltip = 'Click For More Info'
        for i in range(1,self.nokta_sayısı):
            y_coord.insert(i,self.arr[i][self.Y_KOORDİNATI_WGS84].get())
            x_coord.insert(i,self.arr[i][self.X_KOORDİNATI_WGS84].get())
            temp1, temp2 = transform(intProj, outProj, y_coord[i-1], x_coord[i-1])
            y_coord2.append(temp1)
            x_coord2.append(temp2)



            folium.Marker([x_coord2[i-1], y_coord2[i-1]],
                          popup='<strong>Location {} </strong>'.format(i),
                          tooltip='<strong>Location {} </strong>'.format(i)).add_to(m),

            # Generate map
        m.save('map.html')
        os.startfile('map.html')

    def convert_entry_to_float_3_digit(self, entry):
        return float("{0:.3f}".format(float(entry.get())))

    def convert_number_to_float_3_digit(self, entry):
        return float("{0:.3f}".format(float(entry)))

    def convert_entry_to_float_5_digit(self, entry):
        return float("{0:.5f}".format(float(entry.get())))

    def convert_number_to_float_5_digit(self, entry):
        return float("{0:.5f}".format(float(entry)))

if __name__ == '__main__':
    x = transform_ed50_wgs84()
    x.main()
