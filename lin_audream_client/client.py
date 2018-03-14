#this is a client module for main program
'''
send cmds:
"0" - upadate base
"2" - finish session

recv cmds:
"0" - UOK(you okay)
"1" - UNOK(you not okay)
#"J" - next file in jpeg format
#"P" - next file in png format
'''

import os
'''if os.name == "nt":
    path = os.getcwd() + "\\variants"
elif os.name == "posix":
    path = "./variants"
'''
MSGLEN = 3 # defines standart length of command
path = "./variants" # path for source directory

def check_base():
    file_list = os.listdir(path)
    number_files = len(file_list)
    return number_files

def update_base(s):
    n = check_base()
    msg = "0 " + str(chr(n)) #sending request to update base
    s.send(msg)
    ans = s.recv(MSGLEN) # getting answer
    cmd = ans.split(" ")
    if cmd[0] == "0": # handling answer
        s.send("2  ")#finish session
    elif cmd[0] == "1":
        for i in range(n + 1, ord(cmd[1]) + 1):
            os.mkdir(path + "/" + str(i))
            for _ in range(8):
                nc = s.recv(1)
                name = s.recv(ord(nc)) # recieving file name(now we can use png so as jpg)
                f1 = open(path + "/" + str(i) + "/" + name,'wb') #open in binary
                while True:
                    # getting length of incoming pack(there is one number including 2 bytes because of the problem with sockets)	
                    k1 = s.recv(1)
                    k2 = s.recv(1)
                    k = (ord(k1) << 8) + ord(k2)
                    data = s.recv(k)
                    if data == ";;;;;": # end of file feature
                        break
                    f1.write(data)
                f1.close()
    else:
        print("wrong answer! "+ans)
    s.send("2  ")
