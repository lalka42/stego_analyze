from scapy.all import *

file = open(r'C:\\Users\Nikita\Desktop\111.txt', 'rb')
sym = file.read(1)
arr = []
while sym:
 arr.extend('{:08b}'.format(ord(sym)))
 sym = file.read(1)

while len(arr) > 0:
#length
 a = int(arr.pop(0))
 b = int(arr.pop(0))
 c = int(arr.pop(0))
 d = int(arr.pop(0))
 length = 8*a + 4*b + 2*c + d
#TOS
 f = int(arr.pop(0))
 g = int(arr.pop(0))
 h = int(arr.pop(0))
 i = int(arr.pop(0))
 j = int(arr.pop(0))
 k = int(arr.pop(0))
 l = int(arr.pop(0))
 tos = 128*f + 64*g + 32*h + 16*i + 8*j + 4*k + 2*l
 #Ident
 n = int(arr.pop(0))
 o = int(arr.pop(0))
 p = int(arr.pop(0))
 q = int(arr.pop(0))
 r = int(arr.pop(0))
 s = int(arr.pop(0))
 t = int(arr.pop(0))
 ident = 128*n + 64*o + 32*p + 16*q + 8*r + 4*s + 2*t
#urgptr
 v = int(arr.pop(0))
 w = int(arr.pop(0))
 x = int(arr.pop(0))
 y = int(arr.pop(0))
 z = int(arr.pop(0))
 aa = int(arr.pop(0))
 ab = int(arr.pop(0))
 urg = 128*v + 64*w + 32*x + 16*y + 8*z + 4*aa + 2*ab
#ack
 ad = int(arr.pop(0))
 ae = int(arr.pop(0))
 af = int(arr.pop(0))
 ag = int(arr.pop(0))
 ah = int(arr.pop(0))
 ai = int(arr.pop(0))
 aj = int(arr.pop(0))
 ack = 512*ad + 256*ae + 128*af + 32*ag + 8*ah + 4*ah + 2*aj
#window
 al = int(arr.pop(0))
 am = int(arr.pop(0))
 an = int(arr.pop(0))
 ao = int(arr.pop(0))
 ap = int(arr.pop(0))
 aq = int(arr.pop(0))
 at = int(arr.pop(0))
 wind = 512*al + 256*am + 128*an+ 32*ao + 8*ap + 4*aq + 2*at
 udpone = random.randint(1,1024)
 udptwo = random.randint(1,1024)
 tcpone = random.randint(1,1024)
 tcptwo = random.randint(1,1024)
 pktcp = IP(src="192.168.50.153", dst="192.168.50.15", len=length, tos=tos, id=ident) / TCP(sport=tcpone,dport=tcptwo, ack=ack, urgptr=urg,window=wind,flags="AU")
 pkudp = IP(src="192.168.50.153", dst="192.168.50.15") /UDP(sport=udpone,dport=udptwo)
 time.sleep(random.uniform(0.10,0.20))
 send(pktcp)
 time.sleep(random.uniform(0.10,0.20))
 send(pkudp)