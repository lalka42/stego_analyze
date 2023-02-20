import csv
from scapy.all import *


def parser(path, dump, mode):
    parse_mode = mode
    headers = ['udp.srcport', 'udp.dstport', 'tcp.srcport', 'tcp.dstport', 'tcp.ack', 'tcp.urgent_pointer',
               'tcp.window_size_value', 'ip.len', 'ip.id', 'ip.tos', 'ip.src', 'ip.dst']
    # Считываем пакеты с файла
    if parse_mode == 1:
        pcap = rdpcap(path)
    # Считываем пакеты с интерфейса
    else:
        pcap = sniff(count=1)
    with open(dump, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for pkt in pcap:
            if UDP in pkt:
                u1 = pkt['UDP'].sport
                u2 = pkt['UDP'].dport
            else:
                u1 = 0
                u2 = 0
            if TCP in pkt:
                t1 = pkt['TCP'].sport
                t2 = pkt['TCP'].dport
                t3 = pkt['TCP'].ack
                t4 = pkt['TCP'].urgptr
                t5 = pkt['TCP'].window
            else:
                t1 = 0
                t2 = 0
                t3 = 0
                t4 = 0
                t5 = 0
            if IP in pkt:
                i1 = pkt['IP'].len
                i2 = pkt['IP'].id
                i3 = pkt['IP'].tos
                i4 = pkt['IP'].src
                i5 = pkt['IP'].dst
            else:
                i1 = 0
                i2 = 0
                i3 = 0
                i4 = 0
                i5 = 0
            rows = [u1, u2, t1, t2, t3, t4, t5, i1, i2, i3, i4, i5]
            writer.writerow(rows)
