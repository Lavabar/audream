'''
recv cmds:
"0" - upadate base
"1" - finish session

send cmds:
"0" - UOK(you okay)
"1" - UNOK(you not okay)
'''
import socket
import sys
from time import sleep

MSGLEN = 3
path = "variants/"
nvar = 1

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
            break
        else:
            print("Wrong cmd!")
    sc.close()
    break # just for testing(need to remove this break)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

s.close()
