'''
send cmds:
"0" - upadate base
"1" - finish session

recv cmds:
"0" - UOK(you okay)
"1" - UNOK(you not okay)
'''

import os
'''if os.name == "nt":
    path = "%CD%\\variants"
elif os.name == "posix":
    path = "./variants"
'''
MSGLEN = 3
path = "./variants"

def check_base():
    file_list = os.listdir(path)
    number_files = len(file_list)
    return number_files

def update_base(s):
    n = check_base()
    msg = "0 " + str(chr(n))#update base
    s.send(msg)
    ans = s.recv(MSGLEN)
    cmd = ans.split(" ")
    if cmd[0] == "0":
        s.send("1  ")#finish session
    elif cmd[0] == "1":
        for i in range(n + 1, ord(cmd[1]) + 1):
            os.mkdir(path + "/" + str(i))
            for j in range(1, 5):
                f1 = open(path + "/" + str(i) + "/" + str(j) + ".txt",'wb') #open in binary
                while True:	
        	    k1 = s.recv(1)
	 	    k2 = s.recv(1)
		    k = (ord(k1) << 8) + ord(k2)
		    data = s.recv(k)
        	    if data == ";;;;;":
        	        break
        	    f1.write(data)
                f1.close()
                f2 = open(path + "/" + str(i) + "/" + str(j) + ".jpg",'wb') #open in binary
                while True:	
        	    k1 = s.recv(1)
	 	    k2 = s.recv(1)
		    k = (ord(k1) << 8) + ord(k2)
		    data = s.recv(k)
        	    if data == ";;;;;":
        	        break
        	    f2.write(data)
                f2.close()
    else:
        print("wrong answer! "+ans)
    s.send("1  ")
