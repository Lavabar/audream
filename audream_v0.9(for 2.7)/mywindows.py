import Tkinter as tk
import fileinput
from PIL import Image, ImageTk
import pyaudio
import wave
import threading
fname = 'records/' # this variable take part in forming file name of record
chosen_var = '1' # default variant is '1'

timer_listsec = [5, 90, 90] # there are three conditions of timer 'be ready' 'preparing' and 'recording'. So each condition corresponds to each element of the list. This list defines number of seconds that timer is showing on each condition
c = 0 # this is a relative counter of conditions
total = 0 # this is an absolute counter of conditions
timer_running = False # flag for timer. Everything is understandable
default_seconds = timer_listsec[c] # Defines first condition of timer. 'Be ready'
timer_seconds = default_seconds
timer_labels = ["Be ready for task", "Preparing...", "Recording..."] # the same that timer_listsec, but it changes label below the timer, but not seconds

flag_next = True # flag which controlls switching tasks
flag_voice = True # flag which allows recording

numbers = { # This is a "kostyil'". It is intended to switch tasks. It tells program in which value of "total" it(program) have to change the filling of textbox
                1: '1',
                4: '2',
                7: '3',
                10: '4'
            }

listbox_items = ['var 1', 'var 2'] # list for listbox

def exitAll(root): # killall(in some way)
    root.destroy()

#
#Tasks section
#

def voiceRecorder(suff): #source: 'http://sharewebegin.blogspot.ru/2013/07/record-from-mic-python.html'
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
    txt['state'] = tk.NORMAL
    txt.delete('1.0', tk.END)
    txt['state'] = tk.DISABLED
def openTask(num, txt):
    txt['state'] = tk.NORMAL
    txtname = 'variants/' + chosen_var + '/' + num + '.txt'
    imgname = 'variants/' + chosen_var + '/' + num + '.jpg'
    for i in fileinput.input(txtname):
        txt.insert(tk.END, i)
    fimg = Image.open(imgname)
    img = ImageTk.PhotoImage(fimg)
    txt.image_create(tk.END, image=img)
    txt.image = img
    txt['state'] = tk.DISABLED
#
#Timer section
#

def timer_start_pause(root, tmr, label, txt):
    global timer_running
    timer_running = not timer_running  
    if timer_running:  
        timer_tick(root, tmr, label, txt)

def timer_reset(tmr, label):
    global timer_running, timer_seconds
    timer_running = False  
    timer_seconds = timer_listsec[c]  
    label.config(text=timer_labels[c])
    show_timer(tmr)

def timer_tick(root, tmr, label, txt): # the most meanigful function(must be really carefull)
    root.focus_force() # TODO: make more effective controll of focus
    global timer_seconds, c, total, flag_next
    t = threading.Thread(target=lambda:voiceRecorder(numbers[total - 1])) # recording in another thread
    if timer_running and timer_seconds and flag_next:
        tmr.after(1000, lambda:timer_tick(root, tmr, label, txt))
        timer_seconds -= 1
        show_timer(tmr)
    elif (c < 2) and (total < 11): # change to next condition
        flag_next = True
        c += 1
        total += 1
        timer_reset(tmr, label)
        timer_start_pause(root, tmr, label, txt)
	#depending on relative counter of conditions we are openning next task or starting recording        
	if c == 1:
            openTask(numbers[total], txt) # opens next task
        if c == 2:
            t.start() # starts recording
    elif (c == 2) and (total < 11): # zero relative counter of conditions. Go to next iteration of conditions
        flag_next = True
        clearTextbox(txt)
        c = 0
        total += 1
        timer_reset(tmr, label)
        timer_start_pause(root, tmr, label, txt)
    elif total == 11: # in the end just switching off
        exitAll(root)
def show_timer(tmr):
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
    root.focus_force()
    label1 = tk.Label(root, text="Your task is:")
    #label1.place(x=50, y=10)
    label1.grid(row=0, column=0)
    txt1 = tk.Text(master=root, state=tk.DISABLED, font='Monospace 16', width=int(root.winfo_screenwidth())//15, height=int(root.winfo_screenheight())//27, wrap=tk.WORD)
    #txt1 = tk.Text(master=root, font='Monospace 16', width=122, height=40, wrap=tk.WORD)
    #txt1.place(x=50, y=30)
    txt1.grid(row=1, column=0)

    tmr = tk.Label(root, font='Monospace 30')
    #tmr.place(x=1600, y=30)
    tmr.grid(row=0, column=1)
    show_timer(tmr)
    label2 = tk.Label(root, text=timer_labels[c], font='18')
    #label2.place(x=1600, y=90)
    label2.grid(row=1, column=1, columnspan=2, sticky=tk.N)
    timer_start_pause(root, tmr, label2, txt1)

    btn = tk.Button(root, state=tk.NORMAL, text="Next task", width=15, height=3, command=nextTask)
    #btn.pack(side="right")
    btn.grid(row=1, column=3, columnspan=4, rowspan=2, sticky=tk.W+tk.S)

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
    varform = tk.Toplevel(root)
    varform.geometry('400x180')
    varform.title("Audream v0.9")
    varform.focus_force()
    listbox = tk.Listbox(varform, width=10, height=2, font=('13'))
    listbox.bind('<<ListboxSelect>>', lambda event, arg=listbox:select_item(event, arg))
    listbox.place(x=150, y=20)

    for item in listbox_items:
        listbox.insert(tk.END, item)

    btn1 = tk.Button(varform, text="Continue", width=15, height=3, command=lambda:gotoMain(root, varform))
    btn1.place(x=50, y=80)
    btn2 = tk.Button(varform, text="Exit", width=15, height=3, command=lambda:exitAll(root))
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
    regform = tk.Toplevel(root)
    regform.geometry('400x180')
    regform.title("Audream v0.9")
    #regform.winfo_toplevel().title
    label1 = tk.Label(regform, text="Enter your first and last name")
    label1.place(x=50, y=10)
    e1 = tk.Entry(regform)
    e1.place(x=225, y=10)
    e1.focus_set()
    
    label2 = tk.Label(regform, text="Enter the number of your group")
    label2.place(x=50, y=40)
    e2 = tk.Entry(regform)
    e2.place(x=225, y=40)
    
    btn1 = tk.Button(regform, text="Continue", width=15, height=3, command=lambda:gotoVar(root, regform, e1, e2))
    btn1.place(x=50, y=80)
    btn2 = tk.Button(regform, text="Exit", width=15, height=3, command=lambda:exitAll(root))
    btn2.place(x=200, y=80)
