import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.31.123", 9999))
s.listen(10)

sc, address = s.accept()
print(address)
for i in range(1, 5):
    for line in open("./" + str(i) + ".jpg", "rb"):
        k1 = chr(len(line) >> 8)
        k2 = chr(len(line) - (ord(k1) << 8))
        sc.send(k1)
        sc.send(k2)
        sc.send(line)
    sc.send(chr(0))
    sc.send(chr(5))
    sc.send(";;;;;")
sc.close()
s.close()
