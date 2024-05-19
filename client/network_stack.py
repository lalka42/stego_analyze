import socket
import threading
import time
from data_proc import proc

END_OF_FILE_MARKER = b"<EOF>"
VARIABLE_MARKER = b"<VAR>"

class ClientThread(threading.Thread):
    def __init__(self, host, port, ui):
        super().__init__()
        self.host = host
        self.port = port
        self.ui = ui
        self.socket = None
        self.running = True

    # Открываем сокет на сервер
    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.ui.update_status(f"Подключение к серверу {self.host}:{self.port} установлено")
        except Exception as e:
            self.ui.update_status(f"Ошибка подключения: {e}")

    # Отправляем на сервер команду - анализ в реальном времени или анализ дампа
    def send_mode(self, mode):
        try:
            self.socket.sendall(str(mode).encode())
        except Exception as e:
            self.ui.update_status(f"Ошибка отправки режима: {e}")

    # Отправляем на сервер команду запуска/остановки анализа в реальном времени
    def send_command(self, command):
        try:
            self.socket.sendall(command.encode())
        except Exception as e:
            self.ui.update_status(f"Ошибка отправки команды: {e}")

    # Отправляем дамп на сервер
    def send_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.socket.sendall(data)
            self.socket.sendall(END_OF_FILE_MARKER)  # Отправляем маркер конца файла
            time.sleep(0.5)
            self.socket.sendall(str(int(proc.detailed_res_state)).encode())  # Отправляем значение detailed_res_state
            self.ui.update_status("Файл отправлен")
        except Exception as e:
            self.ui.update_status(f"Ошибка отправки файла: {e}")

    # Получаем от сервера полный результат анализа
    def receive_file(self, save_path):
        try:
            with open(save_path, 'wb') as f:
                while True:
                    data = self.socket.recv(1024)
                    if END_OF_FILE_MARKER in data:
                        f.write(data.replace(END_OF_FILE_MARKER, b''))
                        break
                    f.write(data)
            self.ui.update_status(f"Файл сохранен по пути: {save_path}")

            # Получение значения переменной
            self.receive_variable()

        except Exception as e:
            self.ui.update_status(f"Ошибка приема файла: {e}")

    # Получаем от сервера значение есть ли вложение или нет
    def receive_variable(self):
        try:
            result_data = b""
            while True:
                data = self.socket.recv(1024)
                if VARIABLE_MARKER in data:
                    result_data += data.replace(VARIABLE_MARKER, b'')
                    break
                result_data += data
            result_variable = result_data.decode() == 'True'
            print(result_variable)
            self.ui.update_analysis_result(result_variable)

        except Exception as e:
            self.ui.update_status(f"Ошибка приема значения переменной: {e}")

    # Получаем данные анализа в реальном времени
    def receive_rts_data(self):
        try:
            while True:
                data = self.socket.recv(1024)
                if END_OF_FILE_MARKER in data:
                    result_data = data.replace(END_OF_FILE_MARKER, b'').decode()
                    result_list = eval(result_data)
                    self.ui.update_rts_result_new(result_list)
        except Exception as e:
            self.ui.update_status(f"Ошибка приема данных RTS: {e}")

    # Закрываем коннекцию с сервером
    def close_connection(self):
        self.running = False
        if self.socket:
            self.socket.close()
            self.ui.update_status("Соединение закрыто")
