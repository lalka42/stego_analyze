from scapy.all import *
import pandas as pd
pth = 'D:\Desktop\IP.pcap'
pkts = rdpcap(pth)

frame = pd.DataFrame({'udp.srcport': [],'udp.dstport':[],'ip.src':[],'ip.dst':[]})
udpsprt = pd.Series(range(9))
for i in range(9):
    udpsprt[i] = pkts[i].sport
    #frame.loc[i] = pkts[i].sport
    #frame.loc[i] = pkts[i].dport
    #print(pkts[i].sport)
#frame.to_excel('test.xlsx')
print(udpsprt)