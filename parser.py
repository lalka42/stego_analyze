import numpy as np
from scapy.all import *
import pandas as pd
pth = 'D:\Desktop\IP.pcap'
pkt = rdpcap(pth)
cnt=0
for i in pkt:
    cnt+=1
print(cnt)

#df = pd.DataFrame({'srcport': [],'dstport':[],'ip.src':[],'ip.dst':[]})
d = []
count = 0
for i in pkt:
    count+=1
    temp = pd.DataFrame({'id':count,'srcport': pkt[i].sport,'dstport': pkt[i].dport})
#df = pd.DataFrame(d)
# for i in pkts:
#     try:
#        df['srcport'] = np.arange(0,pkts[i].sport,cnt)
#     except TypeError as e:
#         print(f"TypeError handled."
#                f"Error reason - {e}")

#ipsrc = pd.Series(range(cnt))
#ipdst = pd.Series(range(cnt))
#udpsprt = pd.Series(range(cnt))
#udpdprt = pd.Series(range(cnt))
# for i in pkts:
#     try:
#         #udpsprt[i] = pkts[i].sport
#         #udpdprt[i] = pkts[i].dport
#         #ipsrc[i] = bytes(pkts[i][IP].ipsrc)
#         #ipdst[i] = pkts[i].ipdst
#
#     except TypeError as e:
#         print(f"TypeError handled."
#               f"Error reason - {e}")
    #frame.loc[i] = pkts[i].sport
    #frame.loc[i] = pkts[i].dport
    #print(pkts[i].sport)
#frame.to_excel('test.xlsx')
print(df)
#print(udpdprt)
#print(ipsrc)