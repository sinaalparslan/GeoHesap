import tkinter as  tk
from tkinter import ttk
import folium
import os
import xlsxwriter
from tkinter import  Frame

class map:
    labels = ['Nokta No', 'Enlem', 'Boylam']
    valueOfTemp = 0

    def __init__(self, valueOfTemp):
        self.valueOfTemp = int(valueOfTemp)
    def main(self):
        self.NOKTA_ADI = 0
        self.Latitude = 1
        self.Longitude = 2


        self.win = tk.Tk()
        #self.win.iconbitmap('C:/Users/Sina/Desktop/DesignProject/icon/pointer.ico')
        self.win.title('Nokta Gösterme')
        self.win.geometry("463x300")
        self.win.resizable(0, 0)

        self.nokta_sayısı = self.valueOfTemp

        self.frame = Frame(self.win, width=440, height=300, background='#EBEBEB')
        self.frame.grid()
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self.frame, height=295, width=440, background='#EBEBEB')
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

    def map(self,nokta_sayısı):
        m = folium.Map(location=[39.925054,32.836943], zoom_start=10)

        # Global tooltip
        tooltip = 'Click For More Info'
        lat=[]
        lon=[]
        name=[]
        for i in range(1, nokta_sayısı+1):
            lat.insert(i, self.arr[i][self.Latitude].get())
            lon.insert(i,self.arr[i][self.Longitude].get())
            name.insert(i,self.arr[i][self.NOKTA_ADI].get())

            # Create markers

            folium.Marker([float(lat[i-1]),float(lon[i-1])],
                          popup='<strong>Location {} </strong>'.format(i),
                          tooltip='<strong>Location {} </strong>'.format(i)).add_to(m),
            
        # Generate map
        m.save('map.html')
        os.startfile('map.html')

    def create_labels(self):
        H1 = ttk.Label(self.scrollable_frame, text="Nokta Numarası/Adı")
        H2 = ttk.Label(self.scrollable_frame, text='Enlem')
        H3 = ttk.Label(self.scrollable_frame, text='Boylam')

        H1.grid(row=0, column=0, padx=10, pady=10)
        H2.grid(row=0, column=1, padx=10, pady=10)
        H3.grid(row=0, column=2, padx=10, pady=10)

    def create_table(self, nokta_sayısı):
            cols = 3
            rows = nokta_sayısı+2
            self.arr = [[0 for i in range(cols)] for j in range(rows)]

            for i in range(len(self.labels)):
                for j in range(1, nokta_sayısı + 1):
                    self.cur_entry = ttk.Entry(self.scrollable_frame, justify='center', width=20)
                    self.arr[j][i] = self.cur_entry
                    self.cur_entry.grid(row=j, column=i, sticky=tk.NSEW)

            self.calculate_button = ttk.Button(self.scrollable_frame, text="Nokta Göster", command=self.get_values)
            self.calculate_button.grid(row=self.nokta_sayısı + 3, column=0, padx=10, pady=10)

            self.reset_button = ttk.Button(self.scrollable_frame, text="Sıfırla", command=self.reset_values)
            self.reset_button.grid(row=self.nokta_sayısı + 3, column=2, padx=10, pady=10)

            self.quit_button = ttk.Button(self.scrollable_frame, text="Kapat", command=self.close_window)
            self.quit_button.grid(row=self.nokta_sayısı + 5, column=0, padx=10, pady=10)

            self.export_button = ttk.Button(self.scrollable_frame, text="Excel Oluştur", command=self.create_excel)
            self.export_button.grid(row=self.nokta_sayısı + 5, column=2, padx=10, pady=10)


    def close_window(self):
        self.win.destroy()
        self.scrollable_frame.destroy()

    def create_excel(self):

        workbook = xlsxwriter.Workbook('map.xlsx')

        worksheet = workbook.add_worksheet()
        cell_format3 = workbook.add_format({'bold': False, 'font_color': 'blue'})
        cell_format3.set_center_across()
        cell_format2 = workbook.add_format({'bold': False, 'font_color': 'black'})
        cell_format2.set_center_across()
        cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
        cell_format.set_center_across()
        worksheet.write_row(0, 1, self.labels, cell_format)
        worksheet.set_column(0, len(self.labels), 15)

        nokta_numarası = []
        Latitude = []
        Longitude = []


        for i in range(1, self.nokta_sayısı + 1):
            nokta_numarası.insert(i, self.arr[i][self.NOKTA_ADI].get())
            Latitude.insert(i, self.arr[i][self.Latitude].get())
            Longitude.insert(i, self.arr[i][self.Longitude].get())

        for row_num, data in enumerate(nokta_numarası):
            worksheet.write(row_num + 1, 1, data, cell_format2)
        for row_num, data in enumerate(Latitude):
            worksheet.write(row_num + 1, 2, data, cell_format2)
        for row_num, data in enumerate(Longitude):
            worksheet.write(row_num + 1, 3, data, cell_format2)

        workbook.close()
        os.startfile('map.xlsx')


    def reset_values(self):
        self.create_table(self.nokta_sayısı)
        self.calculate_button.config(state = 'normal')

    def get_values(self):
        self.calculate_button.config(state='disabled')
        self.map(self.nokta_sayısı)
    def convert_entry_to_float_3_digit(self, entry):
        return float("{0:.3f}".format(float(entry.get())))

    def convert_number_to_float_3_digit(self, entry):
        return float("{0:.3f}".format(float(entry)))

    def convert_entry_to_float_5_digit(self, entry):
        return float("{0:.5f}".format(float(entry.get())))

    def convert_number_to_float_5_digit(self, entry):
        return float("{0:.5f}".format(float(entry)))


if __name__ == '__main__':
    x = map()
    x.main()
