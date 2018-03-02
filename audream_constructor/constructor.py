import Tkinter as tk
import ttk
import socket
import os
from time import sleep
import threading

n_files = 0
counter = 0

def progress():
    while True:
        prbar['value'] = counter
        if prbar["value"] == prbar["maximum"]:
            break

def check_fool(outlist):
    for one in outlist:
        if not one.isdigit():
            err = "name dir is wrong: '" + one + "'"
            return 0, err
        inlist = os.listdir("./work_directory/" + one)
        for f in inlist:
            global n_files
            n_files += 1
            partF = f.split(".")
            if not partF[0].isdigit() and (partF[1] == "jpg"):
                err = "name file is wrong: '" + f + "'"
                return 0, err 
    return 1, "OK"

def sendVar():
    #s = socket.socket()
    #s.connect(("192.168.31.123",9999))
    n = os.listdir("./work_directory")
    flag = 0
    code, err = check_fool(n)
    if  not len(n) or not code:
        flag += 1
        errform = tk.Toplevel(root)
        errform.geometry("200x90")
        errform.transient(root)
        errlbl = tk.Label(errform, text="Error:" + err + "\nPlease, complete all instructions", font="10")
        errbtn = tk.Button(errform, text="Ok!", width=5, height=1, command=errform.destroy)
        errlbl.place(x=10, y=20)
        errbtn.place(x=15, y=60)
    if flag:
        return
    global counter
    prbar["maximum"] = n_files
    for i in range(0, n_files): 
        print("we are here " + str(i))
        counter = i + 1
        sleep(0.3)
    '''s.send("1 0")
    
    s.send()...
    
    k = s.recv(1)
    lvars = s.recv(ord(k))
    lblvars['text'] = lvars
    s.close()'''
    btn1["state"] = tk.NORMAL
    return

def fake_sendVar():
    threading.Thread(target=sendVar).start()
    btn1["state"] = tk.DISABLED

root = tk.Tk()
#root.wm_iconbitmap("./icon.ico")
root.geometry('400x180')
root.title("Audream constructor v0.1")
btn1 = tk.Button(root, text="Send variant", width=15, height=3, command=fake_sendVar)
btn1.place(x=130, y=100)
lbl1 = tk.Label(root, text="Your numbers are:")
lbl1.place(x=10, y=10)
prbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
prbar.pack(side="bottom")
lblvars = tk.Label(root)
threading.Thread(target=progress).start()
root.mainloop()
