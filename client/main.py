import os
import sys
import threading
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog, QHeaderView
from main_ui import Ui_MainWindow
from network_stack import ClientThread

from properties_ui import Dialog
from data_proc import proc

# Наследуем класс UI_MainWindow от класса, сгенерированного QTDesigner
class user_UI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(user_UI, self).__init__(parent)
        self.setupUi(self)

        self.client_thread = None

        self.settings = QtCore.QSettings("MyCompany", "MyApp")
        self.server_host = self.settings.value("server_host", "")
        self.server_port = int(self.settings.value("server_port", 0))

        self.rb_group = QtWidgets.QButtonGroup()
        self.rb_group.addButton(self.rbt_mode_1, 1)
        self.rb_group.addButton(self.rbt_mode_2, 2)
        self.rb_group.buttonClicked.connect(self.pr_mode_ui)

        self.btn_settings.clicked.connect(self.open_dialog)
        self.btn_dump.clicked.connect(self.choose_file_dump)
        self.line_dump.textChanged[str].connect(proc.change_dump_path)
        self.chekbox_res.stateChanged.connect(self.res_state)
        self.btn_res.clicked.connect(self.save_file_res)
        self.line_res.textChanged[str].connect(proc.change_res_path)
        self.prog_mode = None
        self.btn_start_stop.clicked.connect(self.logic)

        if self.server_host and self.server_port:
            self.connect_to_server()

    # Вызов окна настроек
    def open_dialog(self):
        dialog = Dialog(self, self.server_host, self.server_port)
        if dialog.exec_():
            self.server_host = dialog.lineEdit.text()
            self.server_port = int(dialog.lineEdit_2.text())
            self.settings.setValue("server_host", self.server_host)
            self.settings.setValue("server_port", self.server_port)
            self.connect_to_server()

    # Запускаем поток, в котором подключаемся к серверу
    def connect_to_server(self):
        if self.client_thread:
            self.client_thread.close_connection()
        self.client_thread = ClientThread(self.server_host, self.server_port, self)
        self.client_thread.start()

    # Обновление статуса подключения к серверу
    def update_status(self, message):
        self.label_rts_status.setText(f"Статус: {message}")

    # Обновляем label - результат анализа
    def update_analysis_result(self, result_variable):
        if result_variable:
            self.label.setText("Результат анализа: обнаружены вложения")
            self.label.setStyleSheet("color: red; background:transparent;")
        else:
            self.label.setText("Результат анализа: вложения не обнаружены")
            self.label.setStyleSheet("color: green; background:transparent;")

    # Обновляем таблицу с результатами анализа в реальном времени
    def update_rts_result_new(self, real_row):
        headers = ['Отправитель', 'Получатель', 'Время']
        self.table_real_res.setColumnCount(len(headers))
        self.table_real_res.setHorizontalHeaderLabels(headers)
        self.table_real_res.verticalHeader().setVisible(False)
        # self.rts_results.resizeColumnsToContents()
        self.table_real_res.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_real_res.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        row = self.table_real_res.rowCount()
        self.table_real_res.setRowCount(row + 1)
        col = 0
        for item in real_row:
            cell = QTableWidgetItem(str(item))
            self.table_real_res.setItem(row, col, cell)
            col += 1
        self.table_real_res.scrollToBottom()

    # Получаем флаг чекбокса о полном результате анализа
    def res_state(self):
        proc.change_detailed_res_state(self.chekbox_res.isChecked())
        self.line_res.setEnabled(self.chekbox_res.isChecked())
        self.btn_res.setEnabled(self.chekbox_res.isChecked())

    # Выбор файла дампа для анализа
    def choose_file_dump(self):
        received_path, _ = QFileDialog.getOpenFileName(None, "Выбор файла", None, "Dumps (*.pcap *.pcapng)")
        if received_path:
            received_path = os.path.normpath(received_path)
            proc.change_dump_path(received_path)
            self.line_dump.setText(received_path)

    # Выбор места сохранения результатов анализа
    def save_file_res(self):
        received_path, _ = QFileDialog.getSaveFileName(None, "Сохранение файла", None, "Excel (*.xlsx)")
        if received_path:
            received_path = os.path.normpath(received_path)
            proc.change_res_path(received_path)
            self.line_res.setText(received_path)

    # Смена состояния секции анализа в реальном времени
    def sec_rts(self, mode):
        self.table_real_res.setEnabled(mode)

    # Смена состояния секции анализа в реальном времени
    def sec_analyze(self, mode):
        self.label_dump.setEnabled(mode)
        self.line_dump.setEnabled(mode)
        self.btn_dump.setEnabled(mode)
        self.label.setEnabled(mode)
        self.chekbox_res.setEnabled(mode)
        self.label_res_info.setEnabled(mode)
        if not mode:
            self.line_res.setEnabled(False)
            self.btn_res.setEnabled(False)
        elif proc.detailed_res_state:
            self.line_res.setEnabled(True)
            self.btn_res.setEnabled(True)

    # Блокировка UI при запуске анализа
    def block_ui(self):
        self.sec_rts(False)
        self.sec_analyze(False)
        self.btn_start_stop.setEnabled(False)

    # Смена состояния секций при выборе режима
    def pr_mode_ui(self, button):
        self.mode = self.rb_group.id(button)
        self.btn_start_stop.setEnabled(True)
        if self.mode == 1:
            self.sec_rts(False)
            self.sec_analyze(True)
            self.btn_start_stop.clicked.disconnect()
            self.btn_start_stop.clicked.connect(self.logic)
        elif self.mode == 2:
            self.sec_analyze(False)
            self.sec_rts(True)

    # Окно ошибки если не выбран дамп/путь сохранения анализа
    def msg_error(self, mes):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(mes)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # Метод обработки логики программы при нажатии на кнопку "запуск"
    def logic(self):
        if self.mode == 1:
            if not proc.dump_path or not os.path.exists(proc.dump_path):
                self.msg_error("Не выбран или отсутствует дамп для анализа")
                return
            elif proc.detailed_res_state and not proc.res_path:
                self.msg_error("Не указан путь для сохранения результатов")
                return
            else:
                self.client_thread.send_mode(1)
                processed_file_path = proc.dump_parser()  # Получаем путь до обработанного файла
                threading.Thread(target=self.send_and_receive_file, args=(processed_file_path,)).start()
        elif self.mode == 2:
            self.client_thread.send_mode(2)
            time.sleep(0.5)
            self.client_thread.send_command('1')  # Стартуем захват пакетов
            self.btn_start_stop.setText("Стоп")
            self.btn_start_stop.clicked.disconnect()
            self.btn_start_stop.clicked.connect(self.stop_sniffing)
            threading.Thread(target=self.client_thread.receive_rts_data).start()

    # Остановка режима анализа в RTS
    def stop_sniffing(self):
        self.client_thread.send_command('66')
        self.btn_start_stop.setText("Запуск")
        self.btn_start_stop.clicked.disconnect()
        self.btn_start_stop.clicked.connect(self.logic)

    # Получаем дату от сервера
    def send_and_receive_file(self, file_path):
        self.client_thread.send_file(file_path)
        if proc.detailed_res_state:
            self.client_thread.receive_file(proc.res_path)
        else:
            self.client_thread.receive_variable()

    # Отключаемся от сервера
    def closeEvent(self, event):
        if self.client_thread:
            self.client_thread.close_connection()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = user_UI()
    MainWindow.block_ui()
    MainWindow.show()
    sys.exit(app.exec_())
