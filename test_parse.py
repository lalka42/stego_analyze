from scapy.all import *
pcap = sniff(count=1)
pcap.nsummary()