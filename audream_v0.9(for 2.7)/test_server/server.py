import socket
import sys
s = socket.socket()
s.bind(("192.168.31.123",9999))
s.listen(10) # Acepta hasta 10 conexiones entrantes.

sc, address = s.accept()

print(address)
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


sc.close()

s.close()
