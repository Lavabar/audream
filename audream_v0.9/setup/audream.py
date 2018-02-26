from tkinter import Tk, Entry, Button, DISABLED, NORMAL, Text, WORD, END, Label, Toplevel, Listbox
import fileinput
from PIL import Image, ImageTk
import pyaudio
import wave
import threading
fname = 'records/'
chosen_var = '1'

timer_listsec = [5, 90, 90]
c = 0
total = 0
timer_running = False  # запущен ли таймер
default_seconds = timer_listsec[c]  # изначальное положение
timer_seconds = default_seconds  # текущее положение таймера, сек
timer_labels = ["Be ready for task", "Preparing...", "Recording..."]

flag_next = True
flag_voice = True

numbers = {
                1: '1',
                4: '2',
                7: '3',
                10: '4'
            }

listbox_items = ['var 1', 'var 2']

def exitAll(root):
    root.destroy()

def voiceRecorder(suff):
    global flag_voice
    flag_voice = True
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16 #paInt8
    CHANNELS = 2 
    RATE = 44100 #sample rate
    WAVE_OUTPUT_FILENAME = fname + suff + ".wav"
    RECORD_SECONDS = timer_listsec[2]

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer

    print("* recording")

    frames = []
    i = 0
    while flag_voice and i < int(RATE / CHUNK * RECORD_SECONDS):
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes(16 bits) per channel
        i += 1

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

def clearTextbox(txt):
    txt.delete('1.0', END)
def openTask(num, txt):
    txtname = 'variants/' + chosen_var + '/' + num + '.txt'
    imgname = 'variants/' + chosen_var + '/' + num + '.jpg'
    for i in fileinput.input(txtname):
        txt.insert(END, i)
    fimg = Image.open(imgname)
    img = ImageTk.PhotoImage(fimg)
    txt.image_create(END, image=img)
    txt.image = img

#
#Timer section
#

def timer_start_pause(root, tmr, label, txt):
    global timer_running
    timer_running = not timer_running  # работа или пауза
    if timer_running:  # работа
        timer_tick(root, tmr, label, txt)

def timer_reset(tmr, label):
    global timer_running, timer_seconds
    timer_running = False  # стоп
    timer_seconds = timer_listsec[c]  # изначальное положение
    label.config(text=timer_labels[c])
    show_timer(tmr)

def timer_tick(root, tmr, label, txt):
    global timer_seconds, c, total, flag_next
    t = threading.Thread(target=lambda:voiceRecorder(numbers[total - 1]))
    if timer_running and timer_seconds and flag_next:
        tmr.after(1000, lambda:timer_tick(root, tmr, label, txt))  # перезапустить через 1 сек
        # уменьшить таймер
        timer_seconds -= 1
        show_timer(tmr)
    elif (c < 2) and (total < 11):
        flag_next = True
        c += 1
        total += 1
        timer_reset(tmr, label)
        timer_start_pause(root, tmr, label, txt)
        if c == 1:
            openTask(numbers[total], txt)
        if c == 2:
            t.start()
    elif (c == 2) and (total < 11):
        flag_next = True
        clearTextbox(txt)
        c = 0
        total += 1
        timer_reset(tmr, label)
        timer_start_pause(root, tmr, label, txt)
    elif total == 11:
        exitAll(root)
def show_timer(tmr):
    '''отобразить таймер'''
    m = timer_seconds // 60
    s = timer_seconds - m * 60
    tmr['text'] = '%02d:%02d' % (m, s)

#
#Main section
#

def nextTask():
    global flag_next, flag_voice
    flag_next = False
    flag_voice = False

def showMain(root):
    root.deiconify()
    root.attributes('-fullscreen', 1)
    
    label1 = Label(root, text="Your task is:")
    label1.place(x=50, y=10)
    txt1 = Text(master=root, font='Monospace 16', width=128, height=43, wrap=WORD)
    txt1.place(x=50, y=30)

    btn = Button(root, state=NORMAL, text="Next task", width=15, height=3, command=nextTask)
    btn.pack(side="right")

    tmr = Label(root, font='Monospace 30')
    tmr.place(x=1600, y=30)
    show_timer(tmr)
    label2 = Label(root, text=timer_labels[c], font='18')
    label2.place(x=1600, y=90)
    timer_start_pause(root, tmr, label2, txt1)

#
#Variant section
#

def gotoMain(root, varform):
    varform.destroy()
    showMain(root)

def select_item(event, arg):
    value = (arg.get(arg.curselection()))
    global chosen_var
    chosen_var = value[-1]

def showVariant(root):
    varform = Toplevel(root)
    varform.geometry('400x180')
    varform.focus_force()
    listbox = Listbox(varform, width=10, height=2, font=('13'))
    listbox.bind('<<ListboxSelect>>', lambda event, arg=listbox:select_item(event, arg))
    listbox.place(x=150, y=20)

    for item in listbox_items:
        listbox.insert(END, item)

    btn1 = Button(varform, text="Continue", width=15, height=3, command=lambda:gotoMain(root, varform))
    btn1.place(x=50, y=80)
    btn2 = Button(varform, text="Exit", width=15, height=3, command=lambda:exitAll(root))
    btn2.place(x=200, y=80)
#
#Registration section
#

def gotoVar(root, regform, e1, e2):
    global fname
    s = e1.get().split(' ')
    s1 = e2.get()
    fname += s1 + s[0] + s[1]
    regform.destroy()
    showVariant(root)

def showReg(root):
    regform = Toplevel(root)
    regform.geometry('400x180')
    
    label1 = Label(regform, text="Enter your first and last name")
    label1.place(x=50, y=10)
    e1 = Entry(regform)
    e1.place(x=225, y=10)
    e1.focus_set()
    
    label2 = Label(regform, text="Enter the number of your group")
    label2.place(x=50, y=40)
    e2 = Entry(regform)
    e2.place(x=225, y=40)
    
    btn1 = Button(regform, text="Continue", width=15, height=3, command=lambda:gotoVar(root, regform, e1, e2))
    btn1.place(x=50, y=80)
    btn2 = Button(regform, text="Exit", width=15, height=3, command=lambda:exitAll(root))
    btn2.place(x=200, y=80)

root = Tk()
root.withdraw()
showReg(root)

root.mainloop()