from tkinter import *
from tkinter.ttk import Combobox  
from tkinter.ttk import Checkbutton
import tkinter.filedialog as fd
from variable import variable
from new_algs import knn
import os
import time
import subprocess


dumpe_file = os.getcwd() + '\\dump.csv'
#Функция завершения работы программы
def quit():
    dump_file = os.getcwd() + '\\dump.csv'
    if os.path.exists(dump_file):
        os.remove(dump_file)
    window.destroy()

#Получение пути дампа
def dumped():
    filename = fd.askopenfilename(filetypes=(
        ("pcapng", "*.pcapng"), ("all files", "*.*")))
    variable.change_path(filename)

#Кнопка Анализ
def analyze():
    wd = os.getcwd()
    wd = '"' + wd + '\\Wireshark' + '\\tshark.exe' + '"'
    wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e udp.srcport -e udp.dstport -e tcp.srcport -e tcp.dstport -e tcp.ack -e tcp.urgent_pointer -e tcp.window_size_value -e ip.len -e ip.id -e ip.proto -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.src -e ip.dst > "  + '"' + dumpe_file + '"'
    subprocess.call(wd, shell=True)
    if c1 == 1:
        knn(dumpe_file)

    

   

#Отрисовка окна
window = Tk()
window.title("Machine learning")

lbl = Label(window, text=" ")  
lbl.grid(column=0, row=0)  

#Кнопка выбора дампа
Button(window, text="Выбрать дамп", bg = "#ffa500", font=('Arial Bold', 16), fg = 'white', command=dumped).place(x=200,y=50, anchor=CENTER)


lbl = Label(window, text=" ")  
lbl.grid(column=0, row=2)

#Кнопка закрытия программы
Button(window, text="Закрыть программу", command=quit).place(x=425,y=500, anchor=CENTER)


#Выбор протокола
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

window.geometry('850x530')
window.configure(background='#7FFFD4')
window.mainloop()

