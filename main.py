from tkinter import *
import tkinter
from tkinter.ttk import Combobox  
from tkinter.ttk import Checkbutton
import tkinter.filedialog as fd
from variable import variable
from new_algs import knn
import os
import time
import subprocess
from tkinter import messagebox
import sys


dumpe_file = os.getcwd() + '\\dump.csv'
#Функция завершения работы программы
def quit():
    variable.quit = 1
    dump_file = os.getcwd() + '\\dump.csv'
    if os.path.exists(dump_file):
        os.remove(dump_file)
    window.destroy()



#Получение пути дампа
def dumped():
    filename = fd.askopenfilename(filetypes=(("pcapng", "*.pcapng"), ("all files", "*.*")))
    variable.change_path(filename)
    file_name = os.path.basename("r'" + variable.path)
    Label(window, text=file_name, bg='#7FFFD4', font=('arial', 10, 'normal')).place(x=30, y=180)

def saved():
    save_dir_path = fd.askdirectory()
    variable.change_save_path(save_dir_path)
    res_save_path = variable.path_of_save
    Label(window, text=res_save_path, bg='#7FFFD4', font=('arial', 10, 'normal')).place(x=30, y=310)

#Кнопка ПУСК
def analyze():
    if variable.path == None:
        messagebox.showerror("Ошибка", "Не выбран дамп для анализа")
        return None
    elif variable.path_of_save == None:
        messagebox.showerror("Ошибка", "Не выбрана директория для сохранения результатов")
        return None
    else:
     wd = os.getcwd()
     wd = '"' + wd + '\\Wireshark' + '\\tshark.exe' + '"'
     wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e udp.srcport -e udp.dstport -e tcp.srcport -e tcp.dstport -e tcp.ack -e tcp.urgent_pointer -e tcp.window_size_value -e ip.len -e ip.id -e ip.proto -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.src -e ip.dst > "  + '"' + dumpe_file + '"'
     subprocess.call(wd, shell=True)
     knn(dumpe_file)

#Отрисовка окна
window = Tk()
window.title("Стегоанализ")

#Кнопка выбора дампа
Button(window, text="Выбрать дамп", bg = "#ffa500", font=('Arial Bold', 14), fg = 'white', command=dumped).place(x=116,y=230, anchor=CENTER)

#Кнопка выбора куда сохранять диаграмму и результаты
Button(window, text="Выбрать директорию", bg = "#ffa500", font=('Arial Bold', 12), fg = 'white', command=saved).place(x=116,y=360, anchor=CENTER)

#Кнопка закрытия программы
Button(window, text="Закрыть программу", command=quit).place(x=425,y=500, anchor=CENTER)

#Выбор режима работы программы
program_mode=1

frame=Frame(window, width=0, height=0, bg='#7FFFD4')
frame.place(x=345, y=100)
ARBEES=[
('Анализ', '1'),
('Обучение', '2'),
]
for text, mode in ARBEES:
	rbGroup=Radiobutton(frame, text=text, variable=program_mode, value=mode, bg='#7FFFD4', font=('arial', 12, 'normal')).pack(side='left', anchor = 'w')

#Кнопка анализа
Button(window, text="ПУСК", bg = "#ffa500", font=('GOST', 16),fg = 'white', command = analyze).place(x=425,y=450, anchor=CENTER)


#Отрисовка окна
Label(window, text='Пожалуйста, выберите режим работы программы', bg='#7FFFD4', font=('arial', 12, 'normal')).place(x=270, y=65)
Label(window, text='Обучение', bg='#7FFFD4', font=('arial', 16, 'normal')).place(x=621, y=145)
Label(window, text='Анализ', bg='#7FFFD4', font=('arial', 16, 'normal')).place(x=82, y=145)
Label(window, text='(Куда сохранять результаты)', bg='#7FFFD4', font=('arial', 10, 'normal')).place(x=27, y=380)
window.geometry('850x530')
window.configure(background='#7FFFD4')

Check_diag = IntVar()
Checkbutton(window, text='Нужно ли вывести диаграмму?', variable=Check_diag).place(x=40, y=260)


Check_savediag = IntVar()
Checkbutton(window, text='Нужно ли сохранить диаграмму?', variable=Check_savediag).place(x=40, y=280)

file_name = IntVar()


window.mainloop()

