import sys
import socket
import threading

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

    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.ui.update_status(f"Подключение к серверу {self.host}:{self.port} установлено")
        except Exception as e:
            self.ui.update_status(f"Ошибка подключения: {e}")

    def send_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.socket.sendall(data)
            self.socket.sendall(END_OF_FILE_MARKER)  # Отправляем маркер конца файла
            self.ui.update_status("Файл отправлен")
        except Exception as e:
            self.ui.update_status(f"Ошибка отправки файла: {e}")

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
            result_data = b""
            while True:
                data = self.socket.recv(1024)
                print(data)
                if VARIABLE_MARKER in data:
                    result_data += data.replace(VARIABLE_MARKER, b'')
                    break
                result_data += data

            print(f"Полученные данные: {result_data}")  # Логирование полученных данных
            result_variable = result_data.decode() == 'True'
            print(f"Результат переменной: {result_variable}")
            self.ui.update_analysis_result(result_variable)

        except Exception as e:
            self.ui.update_status(f"Ошибка приема файла: {e}")

    def close_connection(self):
        self.running = False
        if self.socket:
            self.socket.close()
            self.ui.update_status("Соединение закрыто")