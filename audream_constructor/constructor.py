import Tkinter as tk
import ttk
import socket
import os
from time import sleep
import threading

n_files = 0
counter = 0

path = "work_directory" + "/"

prbar_flag = True

def progress():
    while prbar_flag:
        prbar['value'] = counter
        if prbar["value"] >= prbar["maximum"]:
            break
    return

def check_fool(outlist):
    for one in outlist:
        if not one.isdigit():
            err = "name dir is wrong: '" + one + "'"
            return 0, err
        inlist = os.listdir(path + one)
        for f in inlist:
            global n_files
            n_files += 1
            partF = f.split(".")
            if (partF[1] != "jpg") and (partF[1] != "png") and (partF[1] != "txt"):
                err = "Wrong format of file: '" + f + "'"
                return 0, err
            if not partF[0].isdigit():
                err = "file name is wrong: '" + f + "'"
                return 0, err 
    return 1, "OK"

def sendFile(s, f, form):
    if form != -1:
        s.send(form)
    if f != -1:
        for line in f:
            k1 = chr(len(line) >> 8)
            k2 = chr(len(line) - (ord(k1) << 8))
            s.send(k1)
            s.send(k2)
            s.send(line)
    s.send(chr(0))
    s.send(chr(5))
    s.send(";;;;;")
    return

def sendVar(n):
    s = socket.socket()
    s.connect(("192.168.43.110",9999))
    global counter
    prbar["maximum"] = n_files
    s.send("1 0")
    s.send(chr(len(n)))
    for i in range(1, len(n) + 1):
        for j in range(1, 5):
            zt = path + str(i) + "/" + str(j) + ".txt"
            zp = path + str(i) + "/" + str(j) + ".jpg"
            try:
                f1 = open (zt, "rb")
            except IOError:
                sendFile(s, -1, -1) # send empty txt file
                counter += 1
            else:
                sendFile(s, f1, -1) # send not empty txt file
                f1.close()
                counter += 1
            if j == 1:
                try:
                    f2 = open (zp, "rb")
                except IOError:
                    try:
                        zp = path + str(i) + "/" + str(j) + ".png"
                        f2 = open (zp, "rb")
                    except IOError:
                        sendFile(s, -1, "J") # send empty jpg file
                        counter += 1
                    else:
                        sendFile(s, f2, "P") # send not empty png file
                        f2.close()
                        counter += 1
                else:
                    sendFile(s, f2, "J")
                    f2.close()
                    counter += 1
            else:
                try:
                    f2 = open (zp, "rb")
                except IOError:
                    try:
                        zp = path + str(i) + "/" + str(j) + ".png"
                        f2 = open(zp, "rb")
                    except IOError:
                        sendFile(s, -1, "J")
                        counter += 1
                    else:
                        sendFile(s, f2, "P")
                        f2.close()
                        counter += 1
                else:
                    sendFile(s, f2, "J")
                    f2.close()
                    counter += 1   

    k = s.recv(1)
    lvars = s.recv(ord(k))
    lblvars['text'] = lvars
    s.close()
    btn1["state"] = tk.NORMAL
    btn2["state"] = tk.NORMAL
    return

def fake_sendVar():
    btn1["state"] = tk.DISABLED
    btn2["state"] = tk.DISABLED
    n = os.listdir(path)
    flag = 0
    code, err = check_fool(n)
    if  not len(n) or not code:
        if err == "OK":
            err = "work_directory is empty"
        flag += 1
        errform = tk.Toplevel(root)
        errform.resizable(0, 0)
        errform.geometry("400x90")
        errform.transient(root)
        errlbl = tk.Label(errform, text="Error:" + err + "\nPlease, complete all instructions", font="7")
        errbtn = tk.Button(errform, text="Ok!", width=5, height=1, command=errform.destroy)
        errlbl.place(x=10, y=20)
        errbtn.place(x=15, y=60)
    if flag:
        btn1["state"] = tk.NORMAL
        btn2["state"] = tk.NORMAL
        return
    threading.Thread(target=lambda:sendVar(n)).start()
    threading.Thread(target=progress).start()
    return

def exitAll():
    global prbar_flag
    prbar_flag = False
    root.destroy()
    return

root = tk.Tk()
#root.iconbitmap(os.getcwd() + "/icon.ico")
root.geometry('400x180')
root.title("Audream constructor v0.1")
#root.protocol('WM_DELETE_WINDOW')
btn1 = tk.Button(root, text="Send variant", width=15, height=3, command=fake_sendVar)
btn1.place(x=130, y=100)
btn2 = tk.Button(root, text="Exit", width=5, height=1, command=exitAll)
btn2.place(x=320, y=15)
lbl1 = tk.Label(root, text="Your numbers are:")
lbl1.place(x=10, y=10)
prbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
prbar.pack(side="bottom")
lblvars = tk.Label(root, font="Monospace 15")
lblvars.place(x=150, y=50)
root.mainloop()
