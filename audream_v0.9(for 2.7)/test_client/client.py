import os
'''if os.name == "nt":
    path = "%CD%\\variants"
elif os.name == "posix":
    path = "./variants"
'''

path = os.getcwd() + "\\variants"

def check_base():
    file_list = os.listdir(path)
    number_files = len(file_list)
    return number_files

def update_base(s):
    n = check_base()
    msg = "update_base " + str(n)
    s.send(len(msg))
    s.send(msg)
    k = recv(1)
    ans = s.recv(k)
    cmd = ans.split(" ")
    if cmd[0] == "UOK":
        s.send("finish_session ")
    elif cmd[0] == "UNOK":
        for i in range(n + 1, int(cmd[1]) + 1):
            os.mkdir(path + "\\" + str(i))
            for j in range(1, 5):
                f1 = open(path + "\\" + str(i) + "\\" + str(j) + ".txt",'wb') #open in binary
                l1 = s.recv(1024)
                while (l1):
                    f1.write(l1)
                    l1 = s.recv(1024)
                f1.close()
                f2 = open(path + "\\" + str(i) + "\\" + str(j) + ".jpg",'wb') #open in binary
                l2 = s.recv(1024)
                while (l2):
                    f2.write(l2)
                    l2 = s.recv(1024)
                f2.close()
    else:
        print("wrong answer! "+ans)
