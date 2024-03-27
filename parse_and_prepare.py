import csv
from scapy.all import *
from variable import variable
import pandas as pd
import numpy as np
import os
import openpyxl

def parser(path, dump, mode):
    parse_mode = mode
    headers = ['udp.srcport', 'udp.dstport', 'tcp.srcport', 'tcp.dstport', 'tcp.ack', 'tcp.urgent_pointer',
               'tcp.window_size_value', 'tcp.reserved', 'ip.len', 'ip.id', 'ip.tos', 'ip.frag', 'ip.src', 'ip.dst']
    # Считываем пакеты с файла
    if parse_mode == 1:
        pcap = rdpcap(path)
    # Считываем пакеты с интерфейса
    else:
        pcap = sniff(count=1, iface=variable.iface)
    with open(dump, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
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


def dataset_prepare():
    outpath = variable.prepare_set_save_path + '\\dataset.xlsx'
    outpath = os.path.normpath(outpath)
    dump_file = os.getcwd() + '\\prepareset.csv'
    dump_file = os.path.normpath(dump_file)
    parser(variable.prepare_set_path, dump_file, 1)
    df = pd.read_csv(dump_file)
    df['ip.dst'].replace('', np.nan, inplace=True)
    df.dropna(subset=['ip.dst'], inplace=True)
    df.replace(np.nan, 0, inplace=True)
    df['ip.id'] = df['ip.id'].map(lambda x: int(str(x), 16))
    df.to_excel(outpath)
