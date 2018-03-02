import Tkinter as tk
import ttk
import time
import threading

counter = 0
def thr_func():
    pb["maximum"] = 50
    global counter
    for i in range(0, 51):
        counter = i
        time.sleep(0.3)
    btn["state"] = tk.NORMAL

def func():
    print("this function does something")
    threading.Thread(target=thr_func).start()
    btn["state"] = tk.DISABLED    


root = tk.Tk()

btn = tk.Button(root, text="start", command=func)
btn.pack()
pb = ttk.Progressbar(root, mode="determinate")
pb.pack()

def progress():
    while True:
        pb['value'] = counter
        if pb["value"] == pb["maximum"]:
            break

threading.Thread(target=progress).start()
root.mainloop()