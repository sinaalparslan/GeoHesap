import tkinter as  tk
import re
import math
from tkinter import ttk
from matplotlib import pyplot as plt
import folium
import os
import xlsxwriter
from tkinter import messagebox
from tkinter import  Frame
import pyproj
import numpy as np
from pyproj import Proj,transform

class deneme:
    labels = ['Nokta Türü', "Nokta Adı/ Numarası", "Kırılma Açısı (Grad)", "Değişim",
              "Açıklık Açısı (Grad)", "Yatay Kenar (Metre)", "Delta Y (Metre)", "Değişim",
              "Delta X (Metre)", "Değişim", "Y Koordinatı (Metre)", "X Koordinatı (Metre)"]
    valueOfTemp = 0
    def __init__(self, valueOfTemp):
        self.valueOfTemp = int(valueOfTemp)
    def main(self):
        self.POINT_TYPE_INDEX = 0
        self.POINT_NUMBER_INDEX = 1
        self.AZIMUTH_ANGLE_INDEX = 2
        self.AZIMUTH_ANGLE_DIFFERENCE_INDEX = 3
        self.ACIKLIK_ANGLE_INDEX = 4
        self.HORIZONTAL_EDGE_INDEX = 5
        self.DELTA_Y_INDEX = 6
        self.DELTA_Y_DIFFERENCE_INDEX = 7
        self.DELTA_X_INDEX = 8
        self.DELTA_X_DIFFERENCE_INDEX = 9
        self.Y_CORDINATE_INDEX = 10
        self.X_CORDINATE_INDEX = 11
        
        self.win = tk.Tk()
        self.win.title("Bağlı Poligon Hesabı")
        self.win.geometry("1533x350")
        self.win.resizable(0,0)
        self.nirengi_count = 4
        self.point_count = self.valueOfTemp
                
        self.frame = Frame(self.win, width=1498, height=600, background='#EBEBEB')
        self.frame.grid()
        self.frame.rowconfigure(0, weight=1) 
        self.frame.columnconfigure(0, weight=1)
        
        self.canvas=tk.Canvas(self.frame, height=340, width=1508, background='#EBEBEB')
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#EBEBEB")
        self.canvas.create_window(0, 0, window=self.scrollable_frame, anchor='nw')
        
        self.scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scroll.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1, sticky="ns")
        
        self.scrollable_frame.bind("<Configure>", self.update_scrollregion)

        self.create_labels()
        self.create_table(self.point_count, self.nirengi_count)
        self.win.mainloop()
        
    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_labels(self):

        H1 = ttk.Label(self.scrollable_frame, text="Nokta Türü")
        H2 = ttk.Label(self.scrollable_frame, text="Nokta Adı/Numarası")
        H3 = ttk.Label(self.scrollable_frame, text="Kırılma Açısı (Grad)")
        H4 = ttk.Label(self.scrollable_frame, text="Değişim")
        H5 = ttk.Label(self.scrollable_frame, text="Açıklık Açısı (Grad)")
        H6 = ttk.Label(self.scrollable_frame, text="Yatay Kenar (Metre)")
        H7 = ttk.Label(self.scrollable_frame, text="Delta Y (Metre)")
        H8 = ttk.Label(self.scrollable_frame, text="Değişim")
        H9 = ttk.Label(self.scrollable_frame, text="Delta X (Metre)")
        H10 = ttk.Label(self.scrollable_frame, text="Değişim")
        H11 = ttk.Label(self.scrollable_frame, text="Y Koordinatı (Metre)")
        H12 = ttk.Label(self.scrollable_frame, text="X Koordinatı (Metre)")

        H1.grid(row=1, column=0, padx=10, pady=10)
        H2.grid(row=1, column=1, padx=10, pady=10)
        H3.grid(row=1, column=2, padx=10, pady=10)
        H4.grid(row=1, column=3, padx=10, pady=10)       
        H5.grid(row=1, column=4, padx=10, pady=10)
        H6.grid(row=1, column=5, padx=10, pady=10)
        H7.grid(row=1, column=6, padx=10, pady=10)
        H8.grid(row=1, column=7, padx=10, pady=10)
        H9.grid(row=1, column=8, padx=10, pady=10)
        H10.grid(row=1, column=9, padx=10, pady=10)
        H11.grid(row=1, column=10, padx=10, pady=10)
        H12.grid(row=1, column=11, padx=10, pady=10)

    def create_table(self, point_count, nirengi_count):
        cols = 12
        point_count += nirengi_count
        rows = point_count
        self.arr = [[0 for i in range(cols)] for j in range(rows)]

        for i in range(len(self.labels)):
            for j in range(nirengi_count, point_count + nirengi_count):
                self.cur_entry = ttk.Entry(self.scrollable_frame , justify='center',  width = 15)
                self.arr[j - nirengi_count][i] = self.cur_entry
                self.cur_entry.grid(row=j, column=i, sticky=tk.NSEW)


        self.arr[0][self.POINT_TYPE_INDEX].insert(0,'Nirengi')
        self.arr[0][self.POINT_TYPE_INDEX].config(state='disabled')
        self.arr[1][self.POINT_TYPE_INDEX].insert(0, 'Nirengi')
        self.arr[1][self.POINT_TYPE_INDEX].config(state='disabled')
        self.arr[self.point_count + self.nirengi_count - 1][self.POINT_TYPE_INDEX].insert(0, 'Nirengi')
        self.arr[self.point_count + self.nirengi_count - 1][self.POINT_TYPE_INDEX].config(state='disabled')
        self.arr[self.point_count + self.nirengi_count - 2][self.POINT_TYPE_INDEX].insert(0, 'Nirengi')
        self.arr[self.point_count + self.nirengi_count - 2][self.POINT_TYPE_INDEX].config(state='disabled')

        for i in range(2,self.point_count + self.nirengi_count - 2):
            self.arr[i][self.POINT_TYPE_INDEX].insert(0,'Poligon')
            self.arr[i][self.POINT_TYPE_INDEX].config(state='disable')

        self.total_row = self.point_count + self.nirengi_count - 2

        self.calculate_button = ttk.Button(self.scrollable_frame, text="Hesapla", command = self.get_values)
        self.calculate_button.grid(row=self.point_count + self.nirengi_count + 4, column=1, padx=10, pady=10)
        
        self.reset_button = ttk.Button(self.scrollable_frame, text="Sıfırla", command = self.reset_values)
        self.reset_button.grid(row=self.point_count + self.nirengi_count + 4, column=3, padx=10, pady=10)

        self.quit_button = ttk.Button(self.scrollable_frame, text="Kapat", command=self.close_window)
        self.quit_button.grid(row=self.point_count + self.nirengi_count + 4, column=11, padx=10, pady=10)

        self.arr[0][self.AZIMUTH_ANGLE_INDEX].config(state='disabled')
        self.arr[0][self.AZIMUTH_ANGLE_DIFFERENCE_INDEX].config(state='disabled')
        self.arr[0][self.HORIZONTAL_EDGE_INDEX].config(state='disabled')
        self.arr[self.total_row+1][self.HORIZONTAL_EDGE_INDEX].config(state='disabled')
        self.arr[self.total_row + 1][self.ACIKLIK_ANGLE_INDEX].config(state='disabled')
        self.arr[self.total_row + 1][self.AZIMUTH_ANGLE_INDEX].config(state='disabled')
        self.arr[self.total_row + 1][self.AZIMUTH_ANGLE_DIFFERENCE_INDEX].config(state='disabled')
        self.arr[self.total_row ][self.HORIZONTAL_EDGE_INDEX].config(state='disabled')
        self.arr[0][self.DELTA_X_DIFFERENCE_INDEX].config(state='disabled')
        self.arr[0][self.DELTA_X_INDEX].config(state='disabled')
        self.arr[0][self.DELTA_Y_INDEX].config(state='disabled')
        self.arr[0][self.DELTA_Y_DIFFERENCE_INDEX].config(state='disabled')
        self.arr[self.total_row+1][self.DELTA_X_DIFFERENCE_INDEX].config(state='disabled')
        self.arr[self.total_row+1][self.DELTA_X_INDEX].config(state='disabled')
        self.arr[self.total_row+1][self.DELTA_Y_INDEX].config(state='disabled')
        self.arr[self.total_row+1][self.DELTA_Y_DIFFERENCE_INDEX].config(state='disabled')
        self.arr[self.total_row ][self.DELTA_X_DIFFERENCE_INDEX].config(state='disabled')
        self.arr[self.total_row ][self.DELTA_X_INDEX].config(state='disabled')
        self.arr[self.total_row ][self.DELTA_Y_INDEX].config(state='disabled')
        self.arr[self.total_row ][self.DELTA_Y_DIFFERENCE_INDEX].config(state='disabled')


    def close_window(self):
        self.win.destroy()
        self.scrollable_frame.destroy()

    def reset_values(self):
        self.create_table(self.point_count, self.nirengi_count)
        self.calculate_button.config(state = 'normal')
        self.plot_button.grid_remove()

    def get_values(self):

        self.plot_button = ttk.Button(self.scrollable_frame, text="Çizdir", command=self.create_plot)
        self.plot_button.grid(row=self.point_count + self.nirengi_count + 4, column=5, padx=10, pady=10)
        self.calculate_button.config(state = 'disabled')
        self.map_button = ttk.Button(self.scrollable_frame, text="Nokta Göster", command=self.create_map)
        self.map_button.grid(row=self.point_count + self.nirengi_count + 4, column=7, padx=10, pady=10)
        self.excel_button = ttk.Button(self.scrollable_frame, text="Excel Oluştur", command=self.create_excel)
        self.excel_button.grid(row=self.point_count + self.nirengi_count + 4, column=9, padx=10, pady=10)

        self.contol()
        self.calculate_azimuth_angle()

        difference = self.find_difference()
        value_to_add_rows = self.convert_number_to_float_5_digit(difference / self.total_row)
        self.apply_error_to_all_values(value_to_add_rows, self.total_row)
        self.calculate_azimuth_angle()
        self.calculate_deltas(self.total_row)
        self.contol_delta_xy(self.total_row)

    def contol(self):
            list1=[self.ACIKLIK_ANGLE_INDEX,self.ACIKLIK_ANGLE_INDEX,self.Y_CORDINATE_INDEX,self.Y_CORDINATE_INDEX,self.Y_CORDINATE_INDEX,self.Y_CORDINATE_INDEX,self.X_CORDINATE_INDEX,self.X_CORDINATE_INDEX,self.X_CORDINATE_INDEX,self.X_CORDINATE_INDEX]
            list2=[0,self.point_count + self.nirengi_count-2,0,1,self.point_count + self.nirengi_count-1,self.point_count + self.nirengi_count-2,0,1,self.point_count + self.nirengi_count-1,self.point_count + self.nirengi_count-2]

            for k,item in enumerate(list1) :

                if len(self.arr[list2[k]][item].get()) != 0 :
                    l = (self.arr[list2[k]][item].get())
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
                    print('sa')

            for J in range(1,self.point_count + self.nirengi_count-1):
                if  len(self.arr[J][self.AZIMUTH_ANGLE_INDEX].get()) != 0 :
                    b=(self.arr[J][self.AZIMUTH_ANGLE_INDEX].get())
                    if not re.search("[0-9]",b) :
                        messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                    elif re.search("[$#@]",b):
                        messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                    elif re.search("[A-Z]",b):
                        messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                    elif re.search("[a-z]",b):
                        messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                    elif re.search("\s",b):
                        messagebox.showinfo("Information", " gerekli değer girilmemiştir ")
                else:
                    print('sa')
            for i in range(1, self.point_count + self.nirengi_count - 2):
                if len(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get()) != 0 :
                    a = (self.arr[i][self.HORIZONTAL_EDGE_INDEX].get())
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
                    print('sa')
    def contol_delta_xy(self, total_row):
        SS = ((float(self.total_delta_x)) * (float(self.total_delta_x) + (float(self.total_delta_y)) * float(self.total_delta_y)))
        S = math.sqrt(SS)
        self.fQ = (1 / S) * ((self.diff_y * self.total_delta_x) - self.diff_x * self.total_delta_y)
        self.fL = (1 / S) * ((self.diff_y * self.total_delta_y) - self.diff_x * self.total_delta_x)
        self.FQ = 0.06 + 0.00015 * S + 0.004 * math.sqrt(S)
        self.FL = 0.006 + 0.00007 * S + 0.007 * math.sqrt(S)
        if self.fQ>self.FQ or self.fL> self.FL :
            root = tk.Tk()
            root.withdraw()


            messagebox.showinfo("Information", "fQ = {} FQ ={} \n fL={} FL={} ".format(self.convert_number_to_float_3_digit(self.fQ),self.convert_number_to_float_3_digit(self.FQ),self.convert_number_to_float_3_digit(self.fL),self.convert_number_to_float_3_digit(self.FL)))
        else:
            self.calculate_new_y_cordinates(self.total_row)
            self.calculate_new_x_cordinates(self.total_row)


    def create_excel(self):

        workbook = xlsxwriter.Workbook('bağlı_poligon_hesabı.xlsx')

        worksheet = workbook.add_worksheet()
        cell_format3 = workbook.add_format({'bold': False, 'font_color': 'blue'})
        cell_format3.set_center_across()
        cell_format2 = workbook.add_format({'bold': False, 'font_color': 'black'})
        cell_format2.set_center_across()
        cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
        cell_format.set_center_across()
        worksheet.write_row(0, 1, self.labels,cell_format)
        worksheet.set_column(0, len(self.labels),17)

        azimuth_value = []
        açıklık_value = []
        azimuth_değişim=[]
        yatay_kenar = []
        delta_y = []
        delta_y_değişim = []
        delta_x = []
        delta_x_değişim = []
        y_coordinate = []
        x_coordinate = []
        nokta_türü=[]
        nokta_num = []

        for i in range(1, self.point_count + self.nirengi_count-1):
            azimuth_value.insert(i, float(self.arr[i][self.AZIMUTH_ANGLE_INDEX].get()))
            azimuth_değişim.insert(i, float(self.arr[i][self.AZIMUTH_ANGLE_DIFFERENCE_INDEX].get()))
        for i in range(1, self.point_count + self.nirengi_count-2):
             yatay_kenar.insert(i, float(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get()))
             delta_y.insert(i, float(self.arr[i][self.DELTA_Y_INDEX].get()))
             delta_y_değişim.insert(i, float(self.arr[i][self.DELTA_Y_DIFFERENCE_INDEX].get()))
             delta_x.insert(i, float(self.arr[i][self.DELTA_X_INDEX].get()))
             delta_x_değişim.insert(i, float(self.arr[i][self.DELTA_X_DIFFERENCE_INDEX].get()))

        for i in range(0, self.point_count + self.nirengi_count):
            y_coordinate.insert(i, self.arr[i][self.Y_CORDINATE_INDEX].get())
            x_coordinate.insert(i, self.arr[i][self.X_CORDINATE_INDEX].get())
            açıklık_value.insert(i, self.arr[i][self.ACIKLIK_ANGLE_INDEX].get())
            nokta_türü.insert(i, self.arr[i][self.POINT_TYPE_INDEX].get())
            nokta_num.insert(i, self.arr[i][self.POINT_NUMBER_INDEX].get())
        for row_num, data in enumerate(nokta_türü):
            worksheet.write(row_num+1, 1, data,cell_format2)

        for row_num, data in enumerate(nokta_num):
            worksheet.write(row_num+1, 2, data,cell_format2)
        for row_num, data in enumerate(azimuth_value):
            worksheet.write(row_num+2, 3, data,cell_format2)
        for row_num, data in enumerate(azimuth_değişim):
            worksheet.write(row_num + 2, 4, data,cell_format2)
        for row_num, data in enumerate(açıklık_value):
            worksheet.write(row_num + 1, 5, data,cell_format2)
        for row_num, data in enumerate(yatay_kenar):
            worksheet.write(row_num+2, 6, data,cell_format2)
        for row_num, data in enumerate(delta_y):
            worksheet.write(row_num + 2, 7, data,cell_format2)
        for row_num, data in enumerate(delta_y_değişim):
            worksheet.write(row_num + 2, 8, data,cell_format2)
        for row_num, data in enumerate(delta_x):
            worksheet.write(row_num + 2, 9, data,cell_format2)
        for row_num, data in enumerate(delta_x_değişim):
            worksheet.write(row_num + 2, 10, data,cell_format2)
        for row_num, data in enumerate(y_coordinate):
            worksheet.write(row_num + 1, 11, data,cell_format2)
        for row_num, data in enumerate(x_coordinate):
            worksheet.write(row_num + 1, 12, data,cell_format2)
        worksheet.write(self.nirengi_count+self.point_count+1, 6, 'S = {}'.format(self.convert_number_to_float_3_digit(self.total_s) ), cell_format3)
        worksheet.write(self.nirengi_count + self.point_count + 1, 11,'Δy = {}'.format(self.convert_number_to_float_3_digit(self.diff_y)), cell_format3)
        worksheet.write(self.nirengi_count + self.point_count + 1, 12,'Δx = {}'.format(self.convert_number_to_float_3_digit(self.diff_x)), cell_format3)
        worksheet.write(self.nirengi_count + self.point_count + 1, 10,'∑Δx = {}'.format(self.convert_number_to_float_3_digit(self.total_delta_x - self.diff_x)), cell_format3)
        worksheet.write(self.nirengi_count + self.point_count + 1, 8,'∑Δy = {}'.format(self.convert_number_to_float_3_digit(self.total_delta_y - self.diff_y)),cell_format3)
        worksheet.write(self.nirengi_count + self.point_count + 1, 4,'∑⦬ = {}'.format(self.convert_number_to_float_5_digit(self.last_sum)), cell_format3)

        workbook.close()
        os.startfile('bağlı_poligon_hesabı.xlsx')

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
        for i in range(0,self.nirengi_count+self.point_count):
            y_coord.insert(i,float(self.arr[i][self.Y_CORDINATE_INDEX].get()))
            x_coord.insert(i, float(self.arr[i][self.X_CORDINATE_INDEX].get()))
            temp1, temp2 = transform(intProj, outProj, y_coord[i], x_coord[i])
            y_coord2.append(temp1)
            x_coord2.append(temp2)



            folium.Marker([x_coord2[i], y_coord2[i]],
                          popup='<strong>Location {} </strong>'.format(i),
                          tooltip='<strong>Location {} </strong>'.format(i)).add_to(m),

            # Generate map
        m.save('map.html')
        os.startfile('map.html')

    def create_plot(self):
        y_index_value = []
        x_index_value =[]
        combine_x_y=[]
        name_of_coordinate=[]
        for i in range(0,self.point_count + self.nirengi_count-1 ):
            y_index_value.insert(i,float(self.arr[i][self.Y_CORDINATE_INDEX].get()))
            x_index_value.insert(i,float(self.arr[i][self.X_CORDINATE_INDEX].get()))
            name_of_coordinate.insert(i,self.arr[i][self.POINT_NUMBER_INDEX].get())

        for i,type in enumerate(name_of_coordinate):
            y=y_index_value[i]
            x=x_index_value[i]
            plt.scatter(y,x)
            plt.text(y+3,x+1,type,fontsize=15)

        combine_x_y.append(y_index_value)
        combine_x_y.append(x_index_value)
        plt.scatter(y_index_value,x_index_value)
        plt.plot(y_index_value,x_index_value)
        plt.axis([float(self.arr[0][self.Y_CORDINATE_INDEX].get())-10,float(self.arr[self.point_count + self.nirengi_count-2][self.Y_CORDINATE_INDEX].get())+100,float(self.arr[0][self.X_CORDINATE_INDEX].get())-100,float(self.arr[self.point_count + self.nirengi_count-2][self.X_CORDINATE_INDEX].get())+100])
        plt.show()


    def calculate_new_y_cordinates(self, total_row):
        for i in range(1, self.total_row - 1):
            value = (float(self.arr[i][self.DELTA_Y_INDEX].get()) + float(self.arr[i][self.Y_CORDINATE_INDEX].get()))
            self.arr[i+1][self.Y_CORDINATE_INDEX].insert(0, self.convert_number_to_float_3_digit(value))

        #print(float(self.arr[9][6].get()) + float(self.arr[9][8].get()))
        
    def calculate_new_x_cordinates(self, total_row):
        for i in range(1, self.total_row - 1):
            value = (float(self.arr[i][self.DELTA_X_INDEX].get()) + float(self.arr[i][self.X_CORDINATE_INDEX].get()))
            self.arr[i+1][self.X_CORDINATE_INDEX].insert(0, self.convert_number_to_float_3_digit(value))
        #print(float(self.arr[9][self.DELTA_X_INDEX].get()) + float(self.arr[9][self.X_CORDINATE_INDEX].get()))
        
    def calculate_deltas(self, total_row):
        self.total_delta_x = 0
        self.total_delta_y = 0
        for i in range(1, self.total_row):
            self.total_delta_x += self.calculate_delta_x(i)
            self.total_delta_y += self.calculate_delta_y(i)
        self.diff_x = float(self.arr[self.total_row][self.X_CORDINATE_INDEX].get()) - float(self.arr[1][self.X_CORDINATE_INDEX].get())
        self.diff_y = float(self.arr[self.total_row][self.Y_CORDINATE_INDEX].get()) - float(self.arr[1][self.Y_CORDINATE_INDEX].get())
        err_x = self.convert_number_to_float_3_digit(self.total_delta_x - self.diff_x)

        err_y = self.convert_number_to_float_3_digit(self.total_delta_y - self.diff_y)

        self.add_error_to_delta_values(err_y, err_x, self.total_row)


    def add_error_to_delta_values(self, err_y, err_x, total_row):

        self.total_s = 0

        for i in range(1, self.total_row):
            self.total_s += float(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get())

        err_x = self.convert_number_to_float_3_digit(err_x )


        for i in range(1, self.total_row):
            new_delta_y_value = self.convert_number_to_float_3_digit(float(self.arr[i][self.DELTA_Y_INDEX].get()))-self.convert_number_to_float_3_digit(((err_y / self.total_s) * float(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get())))
            new_delta_x_value = self.convert_number_to_float_3_digit(float(self.arr[i][self.DELTA_X_INDEX].get())-self.convert_number_to_float_3_digit(((err_x / self.total_s) * float(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get()))))



            self.clear_old_value(self.arr[i][self.DELTA_Y_INDEX])
            self.clear_old_value(self.arr[i][self.DELTA_X_INDEX])
            self.x_hata= self.convert_number_to_float_3_digit((self.convert_number_to_float_3_digit(((err_x / self.total_s) * float(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get())))))
            self.y_hata= self.convert_number_to_float_3_digit((self.convert_number_to_float_3_digit(((err_y / self.total_s) * float(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get())))))
            self.arr[i][self.DELTA_Y_INDEX].insert(0,self.convert_number_to_float_3_digit(new_delta_y_value))
            self.arr[i][self.DELTA_X_INDEX].insert(0,self.convert_number_to_float_3_digit(new_delta_x_value))
            self.arr[i][self.DELTA_Y_DIFFERENCE_INDEX].insert(0,self.y_hata)
            self.arr[i][self.DELTA_X_DIFFERENCE_INDEX].insert(0,self.x_hata)

    def calculate_delta_y(self,i):
        delta_y = math.sin(math.radians(float(self.arr[i][self.ACIKLIK_ANGLE_INDEX].get()) / 400 * 360)) * float(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get())
        self.arr[i][self.DELTA_Y_INDEX].insert(0,self.convert_number_to_float_3_digit(delta_y))
        return self.convert_number_to_float_3_digit(delta_y)
         
    def calculate_delta_x(self,i):
         delta_x = math.cos(math.radians(float(self.arr[i][self.ACIKLIK_ANGLE_INDEX].get()) / 400 * 360)) * float(self.arr[i][self.HORIZONTAL_EDGE_INDEX].get())
         self.arr[i][self.DELTA_X_INDEX].insert(0,self.convert_number_to_float_3_digit(delta_x))
         return self.convert_number_to_float_3_digit(delta_x)
        
    def calculate_azimuth_angle(self):
        for i in range(0, self.point_count+1):
            first_calculation = self.convert_entry_to_float_5_digit(self.arr[i+1][self.AZIMUTH_ANGLE_INDEX])\
                                + self.convert_entry_to_float_5_digit(self.arr[i][self.ACIKLIK_ANGLE_INDEX])
            processed_value = self.calculate_row_value(first_calculation)
            self.clear_old_value(self.arr[i+1][self.ACIKLIK_ANGLE_INDEX])
            self.arr[i+1][self.ACIKLIK_ANGLE_INDEX].insert(0, str(processed_value))

    def apply_error_to_all_values(self, value, total_row):

        for i in range(1, self.total_row + 1):
            new_value = float(self.arr[i][self.AZIMUTH_ANGLE_INDEX].get()) + value
            self.clear_old_value(self.arr[i][self.AZIMUTH_ANGLE_INDEX])
            self.arr[i][self.AZIMUTH_ANGLE_INDEX].insert(0, self.convert_number_to_float_5_digit(new_value))
            self.arr[i][self.AZIMUTH_ANGLE_DIFFERENCE_INDEX].insert(0, value)

        
    def find_difference(self):
        total_sum =self.convert_entry_to_float_5_digit(self.arr[0][self.ACIKLIK_ANGLE_INDEX])
        for i in range(self.point_count+2):
            total_sum += float(self.arr[i+1][self.AZIMUTH_ANGLE_INDEX].get())
        difference = total_sum % 200
        self.last_sum = self.convert_number_to_float_5_digit(difference) - self.convert_entry_to_float_5_digit(self.arr[self.point_count + self.nirengi_count -2][self.ACIKLIK_ANGLE_INDEX])
        last_sum_memory = self.convert_number_to_float_5_digit(float(difference)- float(self.arr[self.point_count + self.nirengi_count -2][self.ACIKLIK_ANGLE_INDEX].get()))

        if(self.last_sum > 0):
            self.last_sum = -self.last_sum
        return self.convert_number_to_float_5_digit(self.last_sum)

    def clear_old_value(self, position):
        previous_string_length = len(position.get())
        position.delete(0, previous_string_length)

    def calculate_row_value(self, first_calculation):
        if(first_calculation >= 600):
            first_calculation -= 600
        elif(first_calculation >= 200):
            first_calculation -= 200
        elif(first_calculation < 200):
            first_calculation += 200
        return self.convert_number_to_float_5_digit(first_calculation)

    def convert_entry_to_float_3_digit(self, entry):
        return float("{0:.3f}".format(float(entry.get())))

    def convert_number_to_float_3_digit(self, entry):
        return float("{0:.3f}".format(float(entry)))

    def convert_entry_to_float_5_digit(self, entry):
        return float("{0:.5f}".format(float(entry.get())))

    def convert_number_to_float_5_digit(self, entry):
        return float("{0:.5f}".format(float(entry)))

if __name__ == '__main__':
    x = deneme()
    x.main()











