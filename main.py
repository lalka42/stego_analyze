import tkinter
from tkinter import *
from tkinter import Checkbutton
import tkinter.filedialog as fd
from variable import variable
from learn_and_calc import calc, learn, rt_calc
import os
from tkinter import messagebox
from dataset_prepare import dataset_prepare
import time
from dump_parser import parser

dump_file = os.getcwd() + '\\dump.csv'
stop_rts = False

# Функция завершения работы программы
def quit_program():
    variable.quit = 1
    dump_file = os.getcwd() + '\\dump.csv'
    prepareset_path = os.getcwd() + '\\prepareset.csv'
    if os.path.exists(dump_file):
        os.remove(dump_file)
    if os.path.exists(prepareset_path):
        os.remove(prepareset_path)
    window.destroy()


# Получение пути дампа
def dumped():
    filename = fd.askopenfilename(filetypes=(("pcapng", "*.pcapng"), ("all files", "*.*")))
    variable.change_path(filename)
    file_name = os.path.basename("r'" + variable.path)
    c.create_text(115, 190, text=file_name, font=('arial', 10, 'normal'))


def dataset():
    filename = fd.askopenfilename(filetypes=(("xlsx", "*.xlsx"), ("all files", "*.*")))
    variable.change_dataset_path(filename)
    file_name = os.path.basename("r'" + variable.dataset_path)
    c.create_text(675, 190, text=file_name, font=('arial', 10, 'normal'))


def dataset_dumped():
    filename = fd.askopenfilename(filetypes=(("pcapng", "*.pcapng"), ("all files", "*.*")))
    variable.change_prepare_set_path(filename)
    file_name = os.path.basename("r'" + variable.prepare_set_path)
    c.create_text(425, 270, text=file_name, font=('arial', 10, 'normal'))


def saved():
    save_dir_path = fd.askdirectory()
    variable.change_save_path(save_dir_path)
    res_save_path = variable.path_of_save
    c.create_text(115, 325, text=res_save_path, font=('arial', 10, 'normal'))


def dataset_saved():
    save = fd.askdirectory()
    variable.change_save_prepare_path(save)
    res_save_path = variable.prepare_set_save_path
    c.create_text(425, 330, text=res_save_path, font=('arial', 10, 'normal'))


def return_mode_state():
    rb1['state'] = tkinter.NORMAL
    rb2['state'] = tkinter.NORMAL
    rb3['state'] = tkinter.NORMAL

# Кнопка ПУСК
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
    rb3['state'] = tkinter.DISABLED

    if var.get() == 1:
        variable.change_save_diag(Check_savediag.get())
        variable.change_mean_diag(Check_diag.get())
        if variable.path is None:
            messagebox.showerror("Ошибка", "Не выбран дамп для анализа")
            return_mode_state()
            return None
        elif variable.path_of_save is None:
            messagebox.showerror("Ошибка", "Не выбрана директория для сохранения результатов")
            return_mode_state()
            return None
        elif not (os.path.isfile('svm_model.joblib' or 'knn_model.joblib' or 'boost_model.joblib')):
            messagebox.showerror("Ошибка", "Одна из моделей не обучена")
            return_mode_state()
            return None
        else:
            mode = 1
            time_start = time.perf_counter()
            parser(variable.path, dump_file, mode)
            calc(dump_file)
            time_elapsed = "{:2.2f}".format(time.perf_counter() - time_start)
            msg = "Анализ завершён.\n\nЗатраченное время: " + str(time_elapsed) + ' секунд(ы)' + '\n'
            messagebox.showinfo("Результаты анализа", msg)
            return_mode_state()
    elif var.get() == 2:
        if variable.dataset_path is None:
            messagebox.showerror("Ошибка", "Не выбран датасет для обучения")
            return_mode_state()
            return None
        else:
            time_start = time.perf_counter()
            variable.change_svm_count(spin_svm.get())
            variable.change_knn_count(spin_knn.get())
            variable.change_boost_count(spin_boost.get())
            learn(variable.dataset_path)
            if not variable.check_learn:
                return_mode_state()
                messagebox.showerror("Ошибка", "Датасет неправильно размечен")
                return None

            time_elapsed = "{:2.2f}".format(time.perf_counter() - time_start)
            msg1 = 'SVC Score: ' + '\n' + str(variable.report1) + '\n' + '\n'
            msg2 = 'k-NN Score: ' + '\n' + str(variable.report2) + '\n' + '\n'
            msg3 = 'Boost Score: ' + '\n' + str(variable.report3) + '\n' + '\n'
            msg4 = 'Затраченное время: ' + str(time_elapsed) + ' секунд(ы)' + '\n' + '\n'
            msg = msg1 + msg2 + msg3 + msg4
            messagebox.showinfo("Результаты обучения", msg)
            return_mode_state()
    elif var.get() == 3:
        if variable.prepare_set_path is None or variable.prepare_set_save_path is None:
            messagebox.showerror("Ошибка", "Не выбран дамп для подготовки датасета или директория для сохранения")
            return_mode_state()
            return None
        else:
            time_start = time.perf_counter()
            dataset_prepare()
            return_mode_state()
            time_elapsed = "{:2.2f}".format(time.perf_counter() - time_start)
            msg = "Формирование датасета завершено.\n\nЗатраченное время: " + str(time_elapsed) + ' секунд(ы)' + '\n'
            messagebox.showinfo("Формирование датасета", msg)
            return None

def rts_analyze_func():
    mode = 2
    path = ''
    #while not variable.stop_rts:
    parser(mode, dump_file, path)
    #time.sleep(5)
        #calc(dump_file)
    return None




# Отрисовка окна
window = Tk()
window.title("Стегоанализ")

# progress_bar = tkinter.Progressbar(orient='horizontal', mode, maximum, value)
bg = PhotoImage(file="home_background.png")
c = Canvas(window, width=850, height=530)
c.pack(fill="both", expand=True)
c.create_image(0, 0, image=bg, anchor="nw")


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
        dataset_dump_choice_button['state'] = tkinter.DISABLED
        dataset_dir_choice_button['state'] = tkinter.DISABLED
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
        dataset_dump_choice_button['state'] = tkinter.DISABLED
        dataset_dir_choice_button['state'] = tkinter.DISABLED
        window.update()

    elif program_mode == 3:
        dump_choice_button['state'] = tkinter.DISABLED
        dir_choice_button['state'] = tkinter.DISABLED
        dataset_choice_button['state'] = tkinter.DISABLED
        need_saved['state'] = tkinter.DISABLED
        need_mean['state'] = tkinter.DISABLED
        spin_knn['state'] = tkinter.DISABLED
        spin_svm['state'] = tkinter.DISABLED
        spin_boost['state'] = tkinter.DISABLED
        dataset_dump_choice_button['state'] = tkinter.NORMAL
        dataset_dir_choice_button['state'] = tkinter.NORMAL
        window.update()

    elif program_mode == 4:
        dump_choice_button['state'] = tkinter.DISABLED
        dir_choice_button['state'] = tkinter.DISABLED
        dataset_choice_button['state'] = tkinter.DISABLED
        need_saved['state'] = tkinter.DISABLED
        need_mean['state'] = tkinter.DISABLED
        spin_knn['state'] = tkinter.DISABLED
        spin_svm['state'] = tkinter.DISABLED
        spin_boost['state'] = tkinter.DISABLED
        dataset_dump_choice_button['state'] = tkinter.DISABLED
        dataset_dir_choice_button['state'] = tkinter.DISABLED
        pusk['state'] = tkinter.DISABLED
        rts_analyze['state'] = tkinter.NORMAL
        rts_stop['state'] = tkinter.NORMAL
        window.update()


# UI секции анализа
dump_choice_button = Button(window, text="Выбрать дамп", bg="#415374", font=('Arial Bold', 14), fg='white',
                            command=dumped, state=DISABLED)
dump_choice_button.place(x=116, y=230, anchor=CENTER)
# ffa500
dir_choice_button = Button(window, text="Выбрать директорию", bg="#415374", font=('Arial Bold', 12), fg='white',
                           command=saved, state=DISABLED)
dir_choice_button.place(x=116, y=360, anchor=CENTER)

where_save = c.create_text(116, 390, text='(Куда сохранять результаты)', font=('arial', 10, 'normal'))

Check_diag = IntVar()
need_mean = Checkbutton(window, text='Нужно ли вывести диаграмму?', onvalue=1, offvalue=0, bg='#81a4c9',
                        variable=Check_diag, state=DISABLED)
need_mean.place(x=40, y=260)
variable.change_mean_diag(Check_diag)

Check_savediag = IntVar()
need_saved = Checkbutton(window, text='Нужно ли сохранить диаграмму?', onvalue=1, offvalue=0, bg='#81a4c9',
                         variable=Check_savediag, state=DISABLED)
need_saved.place(x=40, y=280)
variable.change_save_diag(Check_savediag)

# UI секции подготовки датасета
dataset_dump_choice_button = Button(window, text="Выбрать дамп", bg="#415374", font=('Arial Bold', 14), fg='white',
                                    command=dataset_dumped, state=DISABLED)
dataset_dump_choice_button.place(x=425, y=230, anchor=CENTER)

dataset_dir_choice_button = Button(window, text="Выбрать директорию", bg="#415374", font=('Arial Bold', 12), fg='white',
                                   command=dataset_saved, state=DISABLED)
dataset_dir_choice_button.place(x=425, y=360, anchor=CENTER)

c.create_text(425, 390, text='(Куда сохранять датасет)', font=('arial', 10, 'normal'))

# UI секции обучения
dataset_choice_button = Button(window, text="Выбрать датасет", bg="#415374", font=('Arial Bold', 14), fg='white',
                               command=dataset, state=DISABLED)
dataset_choice_button.place(x=675, y=230, anchor=CENTER)

c.create_text(675, 297, text='Размер обучающей выборки для svm', font=('arial', 9, 'normal'))
spin_svm = Spinbox(window, increment=0.1, state=DISABLED, from_=0.25, to_=0.9, font=('arial', 12, 'normal'),
                   bg='#81a4c9', width=10)
spin_svm.place(x=625, y=310)
c.create_text(675, 347, text='Размер обучающей выборки для k-NN', font=('arial', 9, 'normal'))
spin_knn = Spinbox(window, increment=0.1, state=DISABLED, from_=0.25, to_=0.9, font=('arial', 12, 'normal'),
                   bg='#81a4c9', width=10)
spin_knn.place(x=625, y=360)
c.create_text(675, 397, text='Размер обучающей выборки для boost', font=('arial', 9, 'normal'))
spin_boost = Spinbox(window, increment=0.1, state=DISABLED, from_=0.25, to_=0.9, font=('arial', 12, 'normal'),
                     bg='#81a4c9', width=10)
spin_boost.place(x=625, y=410)

# Кнопки выбора режима работы программы
var = IntVar()
rb1 = Radiobutton(window, text="Анализ", variable=var, value=1, command=pr_mode, bg='#acc1da')
rb1.place(x=273, y=100)
rb2 = Radiobutton(window, text="Обучение", variable=var, value=2, command=pr_mode, bg='#b5c8df')
rb2.place(x=500, y=100)
rb3 = Radiobutton(window, text="Подготовка датасета", variable=var, value=3, command=pr_mode, bg='#b9cbe0')
rb3.place(x=350, y=100)
rb4 = Radiobutton(window, text="RTS Analyze", variable=var, value=4, command=pr_mode, bg='#b9cbe0')
rb4.place(x=600, y=100)

# Основной UI
pusk = Button(window, text="ПУСК", bg="#1a6dc8", font=('arial', 16), fg='white', command=analyze)
pusk.place(x=425, y=450,anchor=CENTER)
rts_analyze = Button(window, text="Анализ в реальном времени", bg="#1a6dc8", font=('arial', 16), fg='white', command=rts_analyze_func, state=DISABLED)
rts_analyze.place(x=645, y=475,anchor=CENTER)
rts_stop = Button(window, text="Остановить анализ", bg="#1a6dc8", font=('arial', 16), fg='white', command=variable.rts_analyze_stop, state=DISABLED)
rts_stop.place(x=165, y=475,anchor=CENTER)
Button(window, text="Закрыть программу", command=quit_program).place(x=425, y=500, anchor=CENTER)
c.create_text(425, 85, text='Пожалуйста, выберите режим работы программы', font=('arial', 12, 'normal'))
c.create_text(670, 155, text='Обучение', font=('arial', 16, 'normal'))
c.create_text(120, 155, text='Анализ', font=('arial', 16, 'normal'))
c.create_text(425, 155, text='Подготовка датасета', font=('arial', 16, 'normal'))
window.geometry('850x530')
window.resizable(width=0, height=0)
window.mainloop()
