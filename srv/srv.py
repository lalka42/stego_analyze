import socket
import sys
import signal
import threading
import time
import pandas as pd
from model import NeuralNetwork

# Настройки сервера
HOST = '10.98.14.65'
PORT = 1488
SAVE_PATH = 'received_file.csv'
END_OF_FILE_MARKER = b"<EOF>"
VARIABLE_MARKER = b"<VAR>"

class Server:
    def calc(self, inputs):
        output = 'excel.xlsx'
        nn = NeuralNetwork()
        input_batch = pd.read_csv(inputs)
        input_batch.dropna(subset=['ip.src'], inplace=True)
        input_batch.dropna(subset=['ip.dst'], inplace=True)
        outputs = nn.calculate_batch_output(input_batch.values)
        convert = pd.DataFrame(outputs)
        input_batch['probability'] = convert
        input_batch['probability'] = input_batch['probability'].round()
        input_batch.to_excel(output)
        print("Обработка завершена, отравляю результаты клиенту")
        short_res_detect = input_batch.iloc[:, -1]
        if (short_res_detect == 1).any():
            short_res = True
        else:
            short_res = False
        return output, short_res

server_processor = Server()

def handle_client(conn, addr):
    print(f"Соединение установлено с {addr}")
    try:
        # Получение файла
        with open(SAVE_PATH, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if END_OF_FILE_MARKER in data:
                    f.write(data.replace(END_OF_FILE_MARKER, b''))
                    break
                f.write(data)
        print(f"Файл сохранен по пути: {SAVE_PATH}")

        # Обработка файла
        calculated_file_path, result_variable = server_processor.calc(SAVE_PATH)

        # Чтение обработанного файла
        with open(calculated_file_path, 'rb') as f:
            calculated_data = f.read()

        # Отправка обработанного файла и значения переменной обратно клиенту
        conn.sendall(calculated_data + END_OF_FILE_MARKER)  # Добавляем маркер конца файла
        time.sleep(0.5)
        conn.sendall(str(result_variable).encode() + VARIABLE_MARKER)  # Отправляем значение переменной
        print("Обработанный файл и значение переменной отправлены клиенту")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()
        print(f"Соединение с {addr} закрыто")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен и слушает на {HOST}:{PORT}")

        def signal_handler(sig, frame):
            print("\nОстановка сервера...")
            s.close()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        while True:
            try:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
            except OSError:
                break

if __name__ == "__srv__":
    start_server()