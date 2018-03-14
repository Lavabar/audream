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
import threading

MSGLEN = 3
path = "variants/"

f1 = open("info.txt", "r")
nvar = int(f1.read())
f1.close()

def recv_vars():
    n = sc.recv(1)
    n = ord(n)
    ans_list = ""
    global nvar
    for i in range(nvar + 1, nvar + n + 1):
        nvar += 1
        ans_list += str(nvar) + ";"
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
            form = sc.recv(1)
            if form == "J":
                f2 = open(path + "/" + str(i) + "/" + str(j) + ".jpg",'wb') #open in binary
            elif form == "P":
                f2 = open(path + "/" + str(i) + "/" + str(j) + ".png",'wb') #open in binary
            while True:	
                k1 = sc.recv(1)
                k2 = sc.recv(1)
                k = (ord(k1) << 8) + ord(k2)
                data = sc.recv(k)
                if data == ";;;;;":
        	        break
                f2.write(data)
            f2.close()
    sc.send(chr(len(ans_list)))
    sc.send(ans_list)
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
        tmp_path = ""
        for i in range(n + 1, nvar + 1):
            tmp_path = path + str(i) + "/"
            tmp_list = os.listdir(tmp_path)
            for j in tmp_list:
                f1 = open (tmp_path + j, "rb")
                sc.send(chr(len(j)))
                sc.send(j)
                for line in f1:
        	        k1 = chr(len(line) >> 8)
        	        k2 = chr(len(line) - (ord(k1) << 8))
        	        sc.send(k1)
        	        sc.send(k2)
        	        sc.send(line)
                sc.send(chr(0))
                sc.send(chr(5))
                sc.send(";;;;;") 
                f1.close()
    else:
        print(str(n) + " " + str(nvar))
        sc.send("0  ")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.43.110", 9999))
s.listen(10)
a = 0
def handleConnection(sc):
    print(address)
    while (True):
        msg = sc.recv(MSGLEN)
        cmd = msg.split(" ")
        if cmd[0] == "0":
            update_stat()    
            update_base(ord(cmd[1]))
            break
        elif cmd[0] == "1":
            print("i recieved command '1'")
            recv_vars()
            break
        elif cmd[0] == "2":
            break
        else:
            print("Wrong cmd!")
            break
    sc.close()

while (True):
    try:
        sc, address = s.accept()
    except socket.error:
        print("we have to try again")
    except KeyboardInterrupt:
        break
    else:
        threading.Thread(target=lambda:handleConnection(sc)).start()
s.close()
