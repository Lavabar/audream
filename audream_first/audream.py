from tkinter import Tk, Entry, Button, DISABLED, NORMAL, Text, WORD, END

from tkinter.filedialog import askopenfilename
import fileinput

import threading

import pyaudio
import wave

flag = True

def stop():
    global flag
    flag = False
    btn1.config(state=NORMAL)
    btn2.config(state=DISABLED)
def exitApp():
    master.destroy()
def voiceRecorder():
    def callback(fname):
        global flag
        flag = True
        CHUNK = 1024 
        FORMAT = pyaudio.paInt16 #paInt8
        CHANNELS = 2 
        RATE = 44100 #sample rate
        WAVE_OUTPUT_FILENAME = fname

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK) #buffer

        print("* recording")

        frames = []

        while flag:
            data = stream.read(CHUNK)
            frames.append(data) # 2 bytes(16 bits) per channel

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    fname = e.get()
    t1 = threading.Thread(target=lambda:callback(fname))
    btn2.config(state=NORMAL)
    btn1.config(state=DISABLED)
    t1.start()

def start():
    #print_task
    #timer_20
    #print_warning
    voiceRecorder()
    #print_text and timer_120


def openTxt():
    op = askopenfilename()
    for i in fileinput.input(op):
        txt2.insert(END, i)

master = Tk()
master.attributes('-fullscreen', 1)

txt1 = Text(master=master, font='Monospace 16', height=3, wrap=WORD)
txt1.insert('1.0', "Welcome to Audream!\nTo start recording you need enter the name of out-file with .wav suffix")
txt1.pack(side='top')

e = Entry(master)
e.pack(side='top')
e.focus_set()

txt2 = Text(master=master, font='Monospace 16', wrap=WORD)
txt2.place(x=50, y=100)

btn4 = Button(master=master, text="Open", width=30, height=5, bg="white", fg="black", command=openTxt)
btn4.place(x=1600, y=300)

btn3 = Button(master=master, text = "Exit", width = 30, height = 5, bg = "white", fg = "black", command=exitApp)
btn3.pack(side='bottom')
btn2 = Button(master=master, state=DISABLED, text = "Stop", width = 30, height = 5, bg = "white", fg = "black", command=stop)
btn2.pack(side='bottom')
btn1 = Button(master=master, state=NORMAL, text = "Start", width = 30, height = 5, bg = "white", fg = "black", command=voiceRecorder)
btn1.pack(side='bottom')

master.mainloop()