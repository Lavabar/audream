import Tkinter as tk
import socket
import os

def check_fool(n):
    for one in n:
        s = "./work_directory/" + one 

def sendVar():
    #s = socket.socket()
    #s.connect(("192.168.31.123",9999))
    n = os.listdir("./work_directory")
    print(n)
    '''flag = 0
    if  not len(n) or not check_fool(n):
        flag += 1
        errform = tk.Toplevel(root)
        errform.geometry("200x90")
        errform.transient(root)
        errlbl = tk.Label(errform, text="Error: there is nothing in work_directory\nPlease, read file with instructions", font="10")
        errbtn = tk.Button(errform, text="Ok!", width=5, height=1, command=errform.destroy)
        errlbl.place(x=10, y=20)
        errbtn.place(x=15, y=60)
    if flag:
        return
    s.send("1 0")'''
    '''
    s.send()...
    
    k = s.recv(1)
    lvars = s.recv(ord(k))
    lblvars['text'] = lvars
    s.close()'''
    return

root = tk.Tk()
#root.wm_iconbitmap("./icon.ico")
root.geometry('400x180')
root.title("Audream constructor v0.1")
btn1 = tk.Button(root, text="Send variant", width=15, height=3, command=sendVar)
btn1.place(x=130, y=100)
lbl1 = tk.Label(root, text="Your numbers are:")
lbl1.place(x=10, y=10)
lblvars = tk.Label(root)

root.mainloop()