'''
recv cmds:
"0" - upadate base
"1" - recieve new variants
"2" - finish session

send cmds:
"0" - UOK(you okay)
"1" - UNOK(you not okay)
'''
import socket
import sys
from time import sleep
import os

MSGLEN = 3
path = "variants/"

f1 = open("info.txt", "r")
nvar = int(f1.read())
f1.close()

def recv_vars():
    n = sc.recv(1)
    n = ord(n)

    global nvar
    for i in range(nvar + 1, nvar + n + 1):
            nvar += 1
            os.mkdir(path + "/" + str(i))
            for j in range(1, 5):
                f1 = open(path + "/" + str(i) + "/" + str(j) + ".txt",'wb') #open in binary
                while True:	
        	    k1 = sc.recv(1)
	 	    k2 = sc.recv(1)
		    k = (ord(k1) << 8) + ord(k2)
		    data = sc.recv(k)
        	    if data == ";;;;;":
        	        break
        	    f1.write(data)
                f1.close()
                f2 = open(path + "/" + str(i) + "/" + str(j) + ".jpg",'wb') #open in binary
                while True:	
        	    k1 = sc.recv(1)
	 	    k2 = sc.recv(1)
		    k = (ord(k1) << 8) + ord(k2)
		    data = sc.recv(k)
        	    if data == ";;;;;":
        	        break
        	    f2.write(data)
                f2.close()
    f = open("info.txt", "w")
    f.write(str(nvar))
    f.close()

def update_stat():
    sf = open("statistics.txt", "r")
    c = sf.read()
    if c == '':
        c = 0
    else:
        c = int(c)

    sf.close()
    sf = open("statistics.txt", "w")
    c += 1
    sf.write(str(c))
    sf.close()

def update_base(n):
    if n < nvar:
        msg = "1 " + chr(nvar)
        sc.send(msg)
        for i in range(n + 1, nvar + 1):
            for j in range(1, 5):
                zt = path + str(i) + "/" + str(j) + ".txt"
                zp = path + str(i) + "/" + str(j) + ".jpg"
                f1 = open (zt, "rb")
                for line in open(zt, "rb"):
        	        k1 = chr(len(line) >> 8)
        	        k2 = chr(len(line) - (ord(k1) << 8))
        	        sc.send(k1)
        	        sc.send(k2)
        	        sc.send(line)
    	        sc.send(chr(0))
    	        sc.send(chr(5))
    	        sc.send(";;;;;") 
                f1.close()
                f2 = open (zp, "rb")
                for line in open(zp, "rb"):
        	        k1 = chr(len(line) >> 8)
        	        k2 = chr(len(line) - (ord(k1) << 8))
        	        sc.send(k1)
        	        sc.send(k2)
        	        sc.send(line)
    	        sc.send(chr(0))
    	        sc.send(chr(5))
    	        sc.send(";;;;;")
                f2.close()
    else:
        print(str(n) + " " + str(nvar))
        sc.send("0  ")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.31.123", 9999))
s.listen(10)

while (True):
    sc, address = s.accept()
    print(address)
    while (True):
        msg = sc.recv(MSGLEN)
        cmd = msg.split(" ")
        if cmd[0] == "0":
            update_stat()    
            update_base(ord(cmd[1]))
        elif cmd[0] == "1":
            print("i recieved command '1'")
            recv_vars()
        elif cmd[0] == "2":
            break
        #else:
        #    print("Wrong cmd!")
    sc.close()
    break # just for testing(need to remove this break)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

s.close()
