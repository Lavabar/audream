import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.100.6",9999))


for i in range(1, 5):
    f = open("./" + str(i) + ".txt", "wb")
    while True:	
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
	print(len(data))
        if not data:
            break
        # write data to a file
        f.write(data)
f.close()
s.close()
