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
dump = Button(window, text="Выбрать дамп", bg = "#ffa500", font=('Arial Bold', 16), fg = 'white', command=dumped)
dump.place(x=200,y=50, anchor=CENTER)

lbl = Label(window, text=" ")  
lbl.grid(column=0, row=2)

#Кнопка закрытия программы
close = Button(window, text="Закрыть программу", command=quit)
close.place(x=320,y=280, anchor=CENTER)

#Выбор протокола
knn_on = BooleanVar()
knn_on.set(1)
svm_on = BooleanVar()
svm_on.set(0)
c1 = Checkbutton(window, text='K-NN',variable= knn_on, onvalue=1, offvalue=0)
#c1.pack()
c2 = Checkbutton(window, text='Save_res',variable= svm_on, onvalue=1, offvalue=0)
#c2.pack()

c1.place(x=100, y=110, anchor=CENTER)
c2.place(x=200, y=110, anchor=CENTER)


#Кнопка анализа
anal = Button(window, text="Анализ", bg = "#ffa500", font=('Arial Bold', 16),fg = 'white', command = analyze)
anal.place(x=200,y=230, anchor=CENTER)

#Отрисовка окна
window.minsize(400, 300)
window.maxsize(400, 300)
window.mainloop()

