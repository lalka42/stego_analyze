from tkinter import *
from tkinter.ttk import Combobox  
from tkinter.ttk import Radiobutton
from tkinter import messagebox as mb
import tkinter.filedialog as fd
from neural_tcp import tcp_nn
from neural_udp import udp_nn
from neural_ipv4 import ipv4_nn
from knn import udp_knn, tcp_knn, ipv4_knn
from svm import tcp_svm, udp_svm, ipv4_svm
from variable import variable
import subprocess
import os


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
    method_var = combo.get()
    proto_var = selected.get()
    wd = os.getcwd()
    wd= '"' + wd + '\\tshark' + '\\tshark.exe' + '"'
    if variable.path is None:
        mb.showerror("Error",'Не выбран дамп для анализа')
        
    #Обработка по нейронке
    if method_var == 'Нейронная сеть':
        if proto_var == 1:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e tcp.srcport -e tcp.dstport -e tcp.ack -e tcp.urgent_pointer -e tcp.window_size_value -e ip.src -e ip.dst >" + dumpe_file
            os.system(wd)
            tcp_nn(dumpe_file)
        elif proto_var == 2:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e udp.srcport -e udp.dstport -e ip.src -e ip.dst >" + dumpe_file
            os.system(wd)
            udp_nn(dumpe_file)
        elif proto_var == 3:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e ip.len -e ip.id -e ip.proto -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.src -e ip.dst >" + dumpe_file
            os.system(wd)
            ipv4_nn(dumpe_file)
        else:
            mb.showerror("Error",'Не выбран протокол')
   
   #Обработка по SVM
    elif method_var == 'Support vector machine':
        
        #TCP
        if proto_var == 1:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e tcp.srcport -e tcp.dstport -e tcp.ack -e tcp.urgent_pointer -e tcp.window_size_value -e ip.src -e ip.dst > " + dumpe_file
            os.system(wd)
            tcp_svm(dumpe_file)
        
        #UDP
        elif proto_var == 2:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e udp.srcport -e udp.dstport -e ip.src -e ip.dst >" + dumpe_file
            os.system(wd)
            udp_svm(dumpe_file)
        
        #IPv4   
        elif proto_var == 3:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e ip.len -e ip.id -e ip.proto -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.src -e ip.dst >" + dumpe_file
            os.system(wd)
            ipv4_svm(dumpe_file)
        else:
            mb.showerror("Error",'Не выбран протокол')
    
    #Обработка по kNN
    elif method_var == 'k-nearest neigbors':
        
        #TCP
        if proto_var == 1:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e tcp.srcport -e tcp.dstport -e tcp.ack -e tcp.urgent_pointer -e tcp.window_size_value -e ip.src -e ip.dst >" + dumpe_file
            os.system(wd)
            tcp_knn(dumpe_file)
        
        #UDP
        elif proto_var == 2:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e udp.srcport -e udp.dstport -e ip.src -e ip.dst >" + dumpe_file
            os.system(wd)
            udp_knn(dumpe_file)
        
        #IPv4
        elif proto_var == 3:
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e ip.len -e ip.id -e ip.proto -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.src -e ip.dst >" + dumpe_file
            os.system(wd)
            ipv4_knn(dumpe_file)
        else:
            mb.showerror("Error",'Не выбран протокол')
    else:
        mb.showerror("Error",'Не выбран метод анализа')
   

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
selected = IntVar()
rad1 = Radiobutton(window, text='tcp', value=1, variable = selected)  
rad2 = Radiobutton(window, text='udp', value=2, variable = selected)
rad3 = Radiobutton(window, text='ipv4', value=3, variable = selected)  

rad1.place(x=100, y=110, anchor=CENTER)
rad2.place(x=200, y=110, anchor=CENTER)
rad3.place(x=300, y=110, anchor=CENTER)

lbl = Label(window, text=" ")  
lbl.grid(column=0, row=4)  

#Выбор метода анализа
combo = Combobox(window,state = 'readonly')  
combo['values'] = ('Нейронная сеть', 'Support vector machine', 'k-nearest neigbors',)  
combo.current(0)  # установите вариант по умолчанию  
combo.place(x=200,y=150, anchor=CENTER)  

lbl = Label(window, text=" ")  
lbl.grid(column=0, row=6)

#Кнопка анализа
anal = Button(window, text="Анализ", bg = "#ffa500", font=('Arial Bold', 16),fg = 'white', command = analyze)
anal.place(x=200,y=230, anchor=CENTER)

#Отрисовка окна
window.minsize(400, 300)
window.maxsize(400, 300)
window.mainloop()

