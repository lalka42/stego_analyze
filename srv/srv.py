import socket
from datetime import datetime
import sys
import signal
import threading
import pandas as pd
from scapy.all import sniff, UDP, TCP, IP
from model_7_3_neurons import NeuralNetwork

# Настройки сервера
HOST = '192.168.1.110'  # Адрес, на котором слушает сервер сообщения от клиента
PORT = 1489
INTERFACE = 'wlan0'  # Порт, на котором слушает сервер сообщения от клиента
END_OF_FILE_MARKER = b"<EOF>"
VARIABLE_MARKER = b"<VAR>"
SAVE_PATH = 'received_file.csv'
SIEM_IP = '192.168.1.100'  # IP-адрес системы SIEM
SIEM_PORT = 514  # Порт для отправки Syslog сообщений


class Server:
    def __init__(self):
        self.nn = NeuralNetwork()
        self.sniffing = False
        self.clients = []
        self.lock = threading.Lock()
        self.server_socket = None

    # Просчёт полученного CSV (дампа) от клиента на вложения с помощью НС
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
        print("Обработка завершена, отправляю результаты клиенту")
        short_res_detect = input_batch.iloc[:, -1]
        short_res = (short_res_detect == 1).any()
        return output, short_res

    # Парсим сетевой трафик в реальном времени
    def packet_parser(self, packet):
        data = {
            'udp.srcport': packet[UDP].sport if UDP in packet else -1,
            'udp.dstport': packet[UDP].dport if UDP in packet else -1,
            'tcp.srcport': packet[TCP].sport if TCP in packet else -1,
            'tcp.dstport': packet[TCP].dport if TCP in packet else -1,
            'tcp.ack': packet[TCP].ack if TCP in packet else -1,
            'tcp.urgent_pointer': packet[TCP].urgptr if TCP in packet else -1,
            'tcp.window_size_value': packet[TCP].window if TCP in packet else -1,
            'tcp.reserved': packet[TCP].reserved if TCP in packet else -1,
            'ip.len': packet[IP].len if IP in packet else -1,
            'ip.id': packet[IP].id if IP in packet else -1,
            'ip.tos': packet[IP].tos if IP in packet else -1,
            'ip.frag': packet[IP].frag if IP in packet else -1,
            'ip.src': packet[IP].src if IP in packet else -1,
            'ip.dst': packet[IP].dst if IP in packet else -1,
        }
        return pd.DataFrame([data])

    # Отправляем CEF на SIEM при обнаружении вложений
    def send_cef_event(self, src_ip, dst_ip):
        cef_version = "0"
        device_vendor = "Vendor"
        device_product = "Stego SRV"
        device_version = "3.0"
        signature_id = "1001"
        name = "Steganography detected"
        severity = "7"
        extension = f"src={src_ip} dst={dst_ip}"
        cef_message = f"CEF:{cef_version}|{device_vendor}|{device_product}|{device_version}|{signature_id}|{name}|{severity}|{extension}"

        syslog_message = f"<13>{datetime.now().strftime('%b %d %H:%M:%S')} {socket.gethostname()} {cef_message}"

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(syslog_message.encode(), (SIEM_IP, SIEM_PORT))
        print(f"Сообщение CEF отправлено: {syslog_message}")

    # Захватываем пакеты с сетевого интерфейса
    def sniff_packets(self, conn):
        self.sniffing = True
        while self.sniffing:
            packets = sniff(count=1, iface=INTERFACE)
            for packet in packets:
                dataframe = self.packet_parser(packet)
                result = self.rts_calc(dataframe)
                if result:
                    conn.sendall(str(result).encode() + END_OF_FILE_MARKER)
        print("Остановка RTS анализа")

    # Просчёт сетевого трафика с помощью НС в реальном времени
    def rts_calc(self, dataframe):
        input_batch = dataframe
        input_batch.dropna(subset=['ip.src'], inplace=True)
        input_batch.dropna(subset=['ip.dst'], inplace=True)
        outputs = self.nn.calculate_batch_output(input_batch.values)
        convert = pd.DataFrame(outputs)
        input_batch['probability'] = convert
        input_batch['probability'] = input_batch['probability'].round()
        short_res_detect = input_batch.iloc[:, -1]
        short_res = (short_res_detect == 1).any()
        if short_res:
            if input_batch.at[0, 'probability'] == 1:
                src_ip = input_batch.at[0, 'ip.src']
                dst_ip = input_batch.at[0, 'ip.dst']
                self.send_cef_event(src_ip, dst_ip)
                ip_list = [src_ip, dst_ip]
                print(f"Обнаружены вложения: {ip_list}")
        else:
            ip_list = False
        return ip_list

    # Общение с клиентом
    def handle_client(self, conn, addr):
        print(f"Соединение установлено с {addr}")
        with self.lock:
            self.clients.append(conn)
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    print("Получены пустые данные, закрытие соединения.")
                    break

                try:
                    srv_mode = int(data)
                    print(f"Режим сервера: {srv_mode}")  # Добавлен лог для отладки
                except ValueError:
                    print(f"Неверный формат данных: {data}")
                    break

                if srv_mode == 1:
                    # Получение файла
                    with open(SAVE_PATH, 'wb') as f:
                        while True:
                            data = conn.recv(1024)
                            if END_OF_FILE_MARKER in data:
                                f.write(data.replace(END_OF_FILE_MARKER, b''))
                                break
                            f.write(data)
                    print(f"Файл сохранен по пути: {SAVE_PATH}")

                    # Получение флага detailed_res_state от клиента
                    data = conn.recv(1024).decode()
                    try:
                        detailed_res_state = int(data)
                        print(f"Флаг detailed_res_state: {detailed_res_state}")  # Добавлен лог для отладки
                    except ValueError:
                        print(f"Неверный формат данных: {data}")
                        break

                    # Обработка файла
                    calculated_file_path, result_variable = self.calc(SAVE_PATH)

                    if detailed_res_state == 1:
                        # Чтение обработанного файла
                        with open(calculated_file_path, 'rb') as f:
                            calculated_data = f.read()

                        # Отправка обработанного файла и значения переменной обратно клиенту
                        conn.sendall(calculated_data + END_OF_FILE_MARKER)  # Добавляем маркер конца файла
                        time.sleep(0.5)

                    # Отправка значения переменной
                    conn.sendall(str(result_variable).encode() + VARIABLE_MARKER)  # Отправляем значение переменной
                    print(
                        "Обработанный файл и значение переменной отправлены клиенту" if detailed_res_state == 1 else "Значение переменной отправлено клиенту")
                elif srv_mode == 2:
                    data = conn.recv(1024).decode()
                    try:
                        rts_command = int(data)
                        print(f"Команда RTS: {rts_command}")  # Добавлен лог для отладки
                    except ValueError:
                        print(f"Неверный формат данных: {data}")
                        break

                    if rts_command == 1:
                        sniff_thread = threading.Thread(target=self.sniff_packets, args=(conn,))
                        sniff_thread.start()
                    elif rts_command == 2:
                        self.sniffing = False
                        break
                elif srv_mode == 66:
                    self.sniffing = False

        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            with self.lock:
                self.clients.remove(conn)
            conn.close()
            print(f"Соединение с {addr} закрыто")

    # Безопасная остановка сервера при получении SIGTERM и SIGINT
    def shutdown(self):
        print("Остановка сервера...")
        self.sniffing = False
        with self.lock:
            for conn in self.clients:
                conn.close()
            self.clients.clear()
        if self.server_socket:
            self.server_socket.close()

# Запуск сервера
def start_server():
    server = Server()
    threads = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server.server_socket = s
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен и слушает на {HOST}:{PORT}")

        def signal_handler(sig, frame):
            server.shutdown()
            for t in threads:
                t.join()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        while True:
            try:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=server.handle_client, args=(conn, addr))
                threads.append(client_thread)
                client_thread.start()
            except OSError:
                break

if __name__ == "__main__":
    start_server()
