import socket
import sys

s = socket.socket()
s.connect(("localhost",9999))
i=1
f = open(str(i)+".jpg",'wb') #open in binary
i=i+1
while (True):       
# recibimos y escribimos en el fichero
    l = sc.recv(1024)
    while (l):
        f.write(l)
        l = sc.recv(1024)
f.close()
s.close()
