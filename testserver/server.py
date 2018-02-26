import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.100.6", 9999))
s.listen(10)

sc, address = s.accept()
print address
for i in range(1, 5):
    f = open("./" + str(i) + ".txt", "rb")
    l = f.read(1024)
    while l:
        sc.sendall(l)
        l = f.read(1024)

sc.close()
s.close()
