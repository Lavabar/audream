from tkinter import Tk, Entry, Button
import threading

flag = True
master = Tk()
e = Entry(master)
e.pack()
e.focus_set()

def enterName():
    print(e.get())
def stop():
    global flag
    flag = False
def exitApp():
    master.destroy()
def cycle():
    def callback():
        global flag
        a = 0
        flag = True
        while flag:
            a = a + 2
            print(a)
    t1 = threading.Thread(target=callback)
    t1.start()

b1 = Button(master, text="start", width=10, command=cycle)
b1.pack()
b2 = Button(master, text="stop", width=10, command=stop)
b2.pack()
b3 = Button(master, text="exit", width=10, command=exitApp)
b3.pack()

master.mainloop()

