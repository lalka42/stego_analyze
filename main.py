import os
import time
import threading
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem
from scapy.arch.windows import get_windows_if_list

from data_proc import DataProcessor as data_proc
from qt_ui import Ui_MainWindow
from variable import variable


# Основной класс user_UI, отвечающий за отрисовку UI
class user_UI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(user_UI, self).__init__(parent)
        self.setupUi(self)

        self.button_group.buttonClicked.connect(self.pr_mode)
        self.button_pusk.clicked.connect(self.analyze)
        self.button_analyze_dump_choice.clicked.connect(self.choose_file_dump_analyze)
        self.button_analyze_res_choice.clicked.connect(self.save_file_analyze_res)
        self.button_dataset_dump_choice.clicked.connect(self.choose_file_dump_dataset)
        self.button_dataset_res_choice.clicked.connect(self.save_file_dataset)
        self.button_new_model_choice.clicked.connect(self.choose_file_model)
        # self.button_rts_analyze.clicked.connect(self.start_rts_in_bg)
        self.button_rts_stop.clicked.connect(self.stop_rts)
        self.combobox_dataset_type_choice.addItems(["Excel", "CSV"])
        self.combobox_dataset_type_choice.activated[str].connect(variable.change_dataset_res_type)

        self.checkbox_need_mean.stateChanged.connect(self.plot_state)
        # self.checkbox_need_saved.stateChanged.connect(self.plot_state)
        self.combobox_iface_choice.activated[str].connect(variable.change_iface)

        self.mode = 0

        # Отдельный метод для чекбоксов в секции "Анализ"
        # При изменении состояния чекбоксов меняем значения переменных, отвечающих за вывод графиков и результатов
    def plot_state(self):
        variable.change_mean_diag(self.checkbox_need_mean.isChecked())
        # variable.change_save_diag(self.checkbox_need_saved.isChecked())

        # Изначально, когда не выбран режим работы - блокируем все элементы UI кроме выбора режимов
    def block_ui(self):
        self.button_pusk.setEnabled(False)
        self.sec_import_model(False)
        self.sec_prepare(False)
        self.sec_analyze(False)
        self.sec_rts(False)
        self.button_rts_stop.setEnabled(False)

        # При выборе режима "Анализ" раз/блокируем соответствующие элементы

    def sec_analyze(self, mode):
        self.button_pusk.setEnabled(mode)
        self.button_analyze_dump_choice.setEnabled(mode)
        self.button_analyze_res_choice.setEnabled(mode)
        self.line_analyze_res_choice.setEnabled(mode)
        self.line_analyze_dump_choice.setEnabled(mode)
        self.checkbox_need_mean.setEnabled(mode)
        # self.checkbox_need_saved.setEnabled(mode)

        # При выборе режима "Подготовка датасета" раз/блокируем соответствующие элементы

    def sec_prepare(self, mode):
        self.button_pusk.setEnabled(mode)
        self.button_dataset_dump_choice.setEnabled(mode)
        self.button_dataset_res_choice.setEnabled(mode)
        self.line_dataset_dump_choice.setEnabled(mode)
        self.line_dataset_res_choice.setEnabled(mode)

        # При выборе режима "Обучение" раз/блокируем соответствующие элементы
        # Будет переработана на "Подгрузку модели нейронной сети"

    def sec_import_model(self, mode):
        self.button_pusk.setEnabled(mode)
        self.button_new_model_choice.setEnabled(mode)
        self.line_new_model_choice.setEnabled(mode)

        # При выборе режима "RTS Анализ" раз/блокируем соответствующие элементы

    def sec_rts(self, mode):
        self.combobox_iface_choice.setEnabled(mode)
        self.button_rts_analyze.setEnabled(mode)
        self.table_rts_results.setEnabled(mode)

        # При остановке/запуске работы любого режима раз/блокируем rb выбора режима

    def rb_state(self, mode):
        self.rb1.setEnabled(mode)
        self.rb2.setEnabled(mode)
        self.rb3.setEnabled(mode)
        self.rb4.setEnabled(mode)

    # Выбор режима работы
    def pr_mode(self, button):
        self.mode = self.button_group.id(button)
        if self.mode == 1:
            self.sec_import_model(False)
            self.sec_prepare(False)
            self.sec_rts(False)
            self.sec_analyze(True)
        elif self.mode == 2:
            self.sec_import_model(False)
            self.sec_analyze(False)
            self.sec_rts(False)
            self.sec_prepare(True)
        elif self.mode == 3:
            self.sec_prepare(False)
            self.sec_analyze(False)
            self.sec_rts(False)
            self.sec_import_model(True)
        elif self.mode == 4:
            self.sec_import_model(False)
            self.sec_prepare(False)
            self.sec_analyze(False)
            self.sec_rts(True)
            self.rts_iface()

    def start_analyze_in_bg(self):
        threading.Thread(target=self.analyze).start()

    def choose_file_dump_analyze(self):
        received_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Выбор файла", None, "Dumps (*.pcap *.pcapng)")
        if received_path is not None:
            received_path = os.path.normpath(received_path)
            variable.change_analyze_dump_path(received_path)
            self.line_analyze_dump_choice.setText(os.path.basename(received_path))
        else:
            return None

    def choose_file_dump_dataset(self):
        received_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Выбор файла", None, "Dumps (*.pcap *.pcapng)")
        if received_path is not None:
            received_path = os.path.normpath(received_path)
            variable.change_dataset_dump_path(received_path)
            self.line_dataset_dump_choice.setText(os.path.basename(received_path))
        else:
            return None

    def choose_file_model(self):
        received_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Выбор файла", None, "Python file (*.py)")
        if received_path is not None:
            received_path = os.path.normpath(received_path)
            variable.change_new_model_path(received_path)
            self.line_new_model_choice.setText(os.path.basename(received_path))
        else:
            return None


    def save_file_analyze_res(self):
        received_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Сохранение файла", None,
                                                                 "Excel (*.xlsx)")
        if received_path is not None:
            received_path = os.path.normpath(received_path)
            variable.change_analyze_res_path(received_path)
            self.line_analyze_res_choice.setText(os.path.basename(received_path))
        else:
            return None

    def save_file_dataset(self):
        print(variable.selected_dataset_res_type)
        if variable.selected_dataset_res_type == "CSV":
            filter = "CSV (*.csv)"
        elif variable.selected_dataset_res_type == "Excel":
            filter = "Excel (*.xlsx)"
        else:
            return None
        received_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Сохранение файла", None, filter)
        if received_path is not None:
            received_path = os.path.normpath(received_path)
            variable.change_dataset_res_path(received_path)
            self.line_dataset_res_choice.setText(os.path.basename(received_path))
        else:
            return None

    # Определение информационного диалогового окна (вывод инфо о работе программы)
    def msg_info(self, title, mes):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(mes)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # Определение критического диалогового окна (ошибка ввода)
    def msg_error(self, title, mes):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(mes)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def msg_res(self, title, mes):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(mes)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # Вывод интерфейсов в комбобокс
    def rts_iface(self):
        interfaces = pd.DataFrame(get_windows_if_list())
        iface_filter = interfaces['ipv4_metric'] != 0
        interfaces = pd.DataFrame(interfaces[iface_filter])
        df = interfaces[['name']]
        iface_list = df['name'].tolist()
        self.combobox_iface_choice.addItems(iface_list)


    def rts_show_results(self, real_row):
        headers = ['ip.src', 'ip.dst', 'probability']
        self.table_rts_results.setColumnCount(len(headers))
        self.table_rts_results.setHorizontalHeaderLabels(headers)
        self.table_rts_results.verticalHeader().setVisible(False)
        # self.rts_results.resizeColumnsToContents()
        self.table_rts_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_rts_results.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        row = self.table_rts_results.rowCount()
        self.table_rts_results.setRowCount(row + 1)
        col = 0
        for item in variable.rts_row:
            cell = QTableWidgetItem(str(item))
            self.table_rts_results.setItem(row, col, cell)
            col += 1
        self.table_rts_results.scrollToBottom()

    def stop_rts(self):
        variable.rts_analyze_stop()
        self.rb_state(True)
        self.button_rts_analyze.setEnabled(True)
        self.button_rts_stop.setEnabled(False)

    def analyze(self):
        title = "Ошибка"
        self.block_ui()
        self.rb_state(False)
        processor = data_proc()
        if self.mode == 1:
            dataset_type = 0
            if variable.path_analyze_dump is None or os.path.exists(variable.path_analyze_dump) is False:
                self.msg_error(title, "Не выбран или отсутствует дамп для анализа")
                self.sec_analyze(True)
                self.rb_state(True)
                return None
            elif variable.path_analyze_res is None:
                self.msg_error(title, "Не указан путь для сохранения результатов")
                self.sec_analyze(True)
                self.rb_state(True)
                return None
            else:
                time_start = time.perf_counter()
                processor.dump_parser(1, variable.selected_iface, variable.path_analyze_dump)
                processor.import_to_(dataset_type, processor.prepareset_path)
                processor.calc(processor.prepareset_path, variable.path_analyze_res)
                time_elapsed = "{:2.2f}".format(time.perf_counter() - time_start)
                msg = "Анализ завершён.\n\nЗатраченное время: " + str(time_elapsed) + ' секунд(ы)' + '\n'
                self.msg_res("Результаты анализа", msg)
                self.sec_analyze(True)
                self.rb_state(True)

        elif self.mode == 3:
            if os.path.exists(variable.model_path) is False:
                self.msg_error(title, "Не выбрана новая модель")
                return None
            else:
                '''
                Здесь написать логику загрузки новой модели
                self.msg_res("Результаты обучения", msg)
                '''
            self.sec_import_model(True)
            self.rb_state(True)

        elif self.mode == 2:
            if variable.path_dataset_dump is None or os.path.exists(variable.path_dataset_dump) is False:
                self.msg_error(title,"Не выбран\отсутствует дамп для подготовки датасета")
                return None
            if variable.path_dataset_res is None:
                self.msg_error(title,"Не выбран\отсутствует путь для сохранения датасета")
                return None
            else:
                if variable.selected_dataset_res_type == "Excel":
                    dataset_type = 1
                elif variable.selected_dataset_res_type == "CSV":
                    dataset_type = 0
                else:
                    dataset_type = 2
                time_start = time.perf_counter()
                processor.dump_parser(1, variable.selected_iface, variable.path_dataset_dump)
                processor.import_to_(dataset_type, variable.path_dataset_res)
                time_elapsed = "{:2.2f}".format(time.perf_counter() - time_start)
                msg = "Формирование датасета завершено.\n\nЗатраченное время: " + str(
                    time_elapsed) + ' секунд(ы)' + '\n'
                self.msg_res("Формирование датасета", msg)
            self.sec_prepare(True)
            self.rb_state(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = user_UI()
    MainWindow.block_ui()
    MainWindow.show()
    sys.exit(app.exec_())
