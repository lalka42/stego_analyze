import pandas as pd
import numpy as np
import os
import subprocess
from variable import variable

def dataset_prepare():
 pathofdump = variable.prepare_set_path
 tablepath = 'prepareset.csv'
 outpath = variable.prepare_set_save_path + '/dataset.xlsx'
 wd = os.getcwd()
 ww = '"' + wd + '\\Wireshark' + '\\' + tablepath + '"'
 wd = '"' + wd + '\\Wireshark' + '\\tshark.exe' + '"'
 fw = wd + ' -r ' + pathofdump + " -T fields -E header=y -E separator=, -E occurrence=f -e udp.srcport -e udp.dstport -e tcp.srcport -e tcp.dstport -e tcp.ack -e tcp.urgent_pointer -e tcp.window_size_value -e ip.len -e ip.id -e ip.dsfield.dscp -e ip.src -e ip.dst > " + ww
 subprocess.call(fw, shell=True)
 df = pd.read_csv("C:/Users/Nikita/PycharmProjects/stego_analyze/Wireshark/prepareset.csv")
 df['ip.dst'].replace('', np.nan, inplace=True)
 df.dropna(subset=['ip.dst'], inplace=True)
 df.replace(np.nan, 0, inplace=True)
 df['ip.id'] = df['ip.id'].map(lambda x: int(str(x), 16))
 df.to_excel(outpath)