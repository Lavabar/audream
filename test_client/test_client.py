import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.31.123",9999))


for i in range(1, 5):
    f = open("./" + str(i) + ".jpg", "wb")
    while True:	
        print('receiving data...')
        k1 = s.recv(1)
	k2 = s.recv(1)
	k = (ord(k1) << 8) + ord(k2)
	data = s.recv(k)
        print('data=', (data))
	print(len(data))
        if data == ";;;;;":
            break
        # write data to a file
        f.write(data)
f.close()
s.close()
