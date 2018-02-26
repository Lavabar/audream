from tkinter import Tk, Label

from tkinter.filedialog import askopenfilename
import fileinput

import threading

import pyaudio
import wave

import mywindows as win

root = Tk()
root.withdraw()
win.showReg(root)

root.mainloop()
