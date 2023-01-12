import tkinter
from tkinter import *
from tkinter.ttk import Checkbutton
import tkinter.filedialog as fd
from variable import variable
from new_algs import calc,learn
import os
import time
import subprocess
from tkinter import messagebox



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

def dataset():
    filename = fd.askopenfilename(filetypes=(("xlsx", "*.xlsx"), ("all files", "*.*")))
    variable.change_dataset_path(filename)
    file_name = os.path.basename("r'" + variable.dataset_path)
    Label(window, text=file_name, bg='#7FFFD4', font=('arial', 10, 'normal')).place(x=650, y=180)
def saved():
    save_dir_path = fd.askdirectory()
    variable.change_save_path(save_dir_path)
    res_save_path = variable.path_of_save
    Label(window, text=res_save_path, bg='#7FFFD4', font=('arial', 10, 'normal')).place(x=30, y=310)

#Кнопка ПУСК
def analyze():
    dump_choice_button['state'] = tkinter.DISABLED
    dir_choice_button['state'] = tkinter.DISABLED
    dataset_choice_button['state'] = tkinter.DISABLED
    need_saved['state'] = tkinter.DISABLED
    need_mean['state'] = tkinter.DISABLED
    spin_knn['state'] = tkinter.DISABLED
    spin_svm['state'] = tkinter.DISABLED
    spin_boost['state'] = tkinter.DISABLED
    rb1['state'] = tkinter.DISABLED
    rb2['state'] = tkinter.DISABLED

    if var.get() == 1:
        variable.change_save_diag(Check_savediag.get())
        variable.change_mean_diag(Check_diag.get())
        if variable.path == None:
            messagebox.showerror("Ошибка", "Не выбран дамп для анализа")
            rb1['state'] = tkinter.NORMAL
            rb2['state'] = tkinter.NORMAL
            return None
        elif variable.path_of_save == None:
            messagebox.showerror("Ошибка", "Не выбрана директория для сохранения результатов")
            rb1['state'] = tkinter.NORMAL
            rb2['state'] = tkinter.NORMAL
            return None
        elif (os.path.isfile('svm_model.joblib') or os.path.isfile('knn_model.joblib') or os.path.isfile('boost_model.joblib')) != True:
            messagebox.showerror("Ошибка", "Одна из моделей не обучена")
            rb1['state'] = tkinter.NORMAL
            rb2['state'] = tkinter.NORMAL
            return None
        else:
            wd = os.getcwd()
            wd = '"' + wd + '\\Wireshark' + '\\tshark.exe' + '"'
            #wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e tcp.srcport -e tcp.dstport -e tcp.ack -e tcp.urgent_pointer -e tcp.window_size_value -e ip.src -e ip.dst >" + '"' + dumpe_file + '"'
            #wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e udp.srcport -e udp.dstport -e ip.src -e ip.dst >" + '"' + dumpe_file + '"'
            #wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e udp.srcport -e udp.dstport -e tcp.srcport -e tcp.dstport -e tcp.ack -e tcp.urgent_pointer -e tcp.window_size_value -e ip.len -e ip.id -e ip.proto -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.src -e ip.dst > "  + '"' + dumpe_file + '"'
            wd = wd + ' -r ' + variable.path + " -T fields -E header=y -E separator=, -E occurrence=f -e ip.len -e ip.id -e ip.tos -e ip.src -e ip.dst >" + '"' + dumpe_file + '"'
            subprocess.call(wd, shell=True)
            calc(dumpe_file)
            rb1['state'] = tkinter.NORMAL
            rb2['state'] = tkinter.NORMAL
    elif var.get() == 2:
        if variable.dataset_path == None:
            messagebox.showerror("Ошибка", "Не выбран датасет для обучения")
            rb1['state'] = tkinter.NORMAL
            rb2['state'] = tkinter.NORMAL
            return None
        else:
            variable.change_svm_count(spin_svm.get())
            variable.change_knn_count(spin_knn.get())
            variable.change_boost_count(spin_boost.get())
            learn(variable.dataset_path)
            rb1['state'] = tkinter.NORMAL
            rb2['state'] = tkinter.NORMAL


#Отрисовка окна
window = Tk()
window.title("Стегоанализ")
#progress_bar = tkinter.Progressbar(orient='horizontal', mode, maximum, value)


def pr_mode():
    program_mode = var.get()

    if program_mode == 1:
        dump_choice_button['state'] = tkinter.NORMAL
        dir_choice_button['state'] = tkinter.NORMAL
        dataset_choice_button['state'] = tkinter.DISABLED
        need_saved['state'] = tkinter.NORMAL
        need_mean['state'] = tkinter.NORMAL
        spin_knn['state'] = tkinter.DISABLED
        spin_svm['state'] = tkinter.DISABLED
        spin_boost['state'] = tkinter.DISABLED
        window.update()

    elif program_mode == 2:
        dump_choice_button['state'] = tkinter.DISABLED
        dir_choice_button['state'] = tkinter.DISABLED
        dataset_choice_button['state'] = tkinter.NORMAL
        need_saved['state'] = tkinter.DISABLED
        need_mean['state'] = tkinter.DISABLED
        spin_knn['state'] = tkinter.NORMAL
        spin_svm['state'] = tkinter.NORMAL
        spin_boost['state'] = tkinter.NORMAL
        window.update()



dump_choice_button = Button(window, text="Выбрать дамп", bg = "#ffa500", font=('Arial Bold', 14), fg = 'white', command=dumped, state=DISABLED)
dump_choice_button.place(x=116,y=230, anchor=CENTER)

dir_choice_button = Button(window, text="Выбрать директорию", bg = "#ffa500", font=('Arial Bold', 12), fg = 'white', command=saved,state=DISABLED)
dir_choice_button.place(x=116,y=360, anchor=CENTER)

where_save = Label(window, text='(Куда сохранять результаты)', bg='#7FFFD4', font=('arial', 10, 'normal'))
where_save.place(x=27, y=380)

dataset_choice_button = Button(window, text="Выбрать датасет", bg="#ffa500", font=('Arial Bold', 14), fg='white', command=dataset,state=DISABLED)
dataset_choice_button.place(x=675, y=230, anchor=CENTER)

Label(window, text='Размер обучающей выборки для svm', bg='#7FFFD4', font=('arial', 9, 'normal')).place(x=570, y=287)
spin_svm = Spinbox(window, increment=0.1, state=DISABLED, from_= 0.25, to_= 0.9, font=('arial', 12, 'normal'), bg='#F0F8FF', width=10)
spin_svm.place(x=625, y=310)
Label(window, text='Размер обучающей выборки для k-NN', bg='#7FFFD4', font=('arial', 9, 'normal')).place(x=570, y=337)
spin_knn = Spinbox(window, increment=0.1, state=DISABLED, from_= 0.25, to_= 0.9, font=('arial', 12, 'normal'), bg='#F0F8FF', width=10)
spin_knn.place(x=625, y=360)
Label(window, text='Размер обучающей выборки для boost', bg='#7FFFD4', font=('arial', 9, 'normal')).place(x=570, y=387)
spin_boost = Spinbox(window, increment=0.1, state=DISABLED, from_= 0.25, to_= 0.9, font=('arial', 12, 'normal'), bg='#F0F8FF', width=10)
spin_boost.place(x=625, y=410)

Check_diag = IntVar()
need_mean = Checkbutton(window, text='Нужно ли вывести диаграмму?', onvalue=1, offvalue=0, variable=Check_diag, state=DISABLED)
need_mean.place(x=40,y=260)
variable.change_mean_diag(Check_diag)

Check_savediag = IntVar()
need_saved = Checkbutton(window, text='Нужно ли сохранить диаграмму?', onvalue=1, offvalue=0, variable=Check_savediag, state=DISABLED)
need_saved.place(x=40, y=280)
variable.change_save_diag(Check_savediag)

var = IntVar()
rb1 = Radiobutton(window, text="Анализ", variable=var, value=1, command=pr_mode)
rb1.place(x=340, y=100)
rb2 = Radiobutton(window, text="Обучение", variable=var, value=2, command=pr_mode)
rb2.place(x=440, y=100)

Button(window, text="ПУСК", bg = "#ffa500", font=('GOST', 16),fg = 'white', command = analyze).place(x=425,y=450, anchor=CENTER)
Button(window, text="Закрыть программу", command=quit).place(x=425,y=500, anchor=CENTER)
#Отрисовка окна
Label(window, text='Пожалуйста, выберите режим работы программы', bg='#7FFFD4', font=('arial', 12, 'normal')).place(x=270, y=65)
Label(window, text='Обучение', bg='#7FFFD4', font=('arial', 16, 'normal')).place(x=621, y=145)
Label(window, text='Анализ', bg='#7FFFD4', font=('arial', 16, 'normal')).place(x=82, y=145)

window.geometry('850x530')
window.configure(background='#7FFFD4')
window.mainloop()

