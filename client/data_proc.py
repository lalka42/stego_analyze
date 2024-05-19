from scapy.all import *
import csv
import socket
class DataProcessor:
    def __init__(self, **kwargs):
        self.dump_path = None
        self.res_path = None
        self.detailed_res_state = False
        self.shorted_res = None
        self.headers = ['udp.srcport', 'udp.dstport', 'tcp.srcport', 'tcp.dstport', 'tcp.ack', 'tcp.urgent_pointer',
                        'tcp.window_size_value', 'tcp.reserved', 'ip.len', 'ip.id', 'ip.tos', 'ip.frag', 'ip.src',
                        'ip.dst']
        self.prepareset_path = os.getcwd() + '\\prepareset.csv'

# Методы для смены путей к дампу/пути сохранения анализа/нужно ли получить полный анализ
    def change_dump_path(self, path):
        self.dump_path = path

    def change_res_path(self,path):
        self.res_path = path

    def change_detailed_res_state(self, state):
        self.detailed_res_state = state

    # Парсим дамп в CSV перед отправкой на сервер
    def dump_parser(self):
        pcap = rdpcap(self.dump_path)
        with open(self.prepareset_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            for pkt in pcap:
                if UDP in pkt:
                    u1 = pkt['UDP'].sport
                    u2 = pkt['UDP'].dport
                else:
                    u1 = -1
                    u2 = -1
                if TCP in pkt:
                    t1 = pkt['TCP'].sport
                    t2 = pkt['TCP'].dport
                    t3 = pkt['TCP'].ack
                    t4 = pkt['TCP'].urgptr
                    t5 = pkt['TCP'].window
                    t6 = pkt['TCP'].reserved
                else:
                    t1 = -1
                    t2 = -1
                    t3 = -1
                    t4 = -1
                    t5 = -1
                    t6 = -1
                if IP in pkt:
                    i1 = pkt['IP'].len
                    i2 = pkt['IP'].id
                    i3 = pkt['IP'].tos
                    i4 = pkt['IP'].frag
                    i5 = pkt['IP'].src
                    i6 = pkt['IP'].dst
                else:
                    i1 = -1
                    i2 = -1
                    i3 = -1
                    i4 = -1
                    i5 = -1
                    i6 = -1
                rows = [u1, u2, t1, t2, t3, t4, t5, t6, i1, i2, i3, i4, i5, i6]
                writer.writerow(rows)
        return self.prepareset_path

proc = DataProcessor()