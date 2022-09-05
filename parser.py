from scapy.all import *

pth = 'D:\Desktop\IP.pcap'
pkts = rdpcap(pth)

print(ls(pkts[7]))
#print(pkts[7].seq)
