from distutils.core import setup
import py2exe
 
setup(
    windows=[{"script":"main.py"}],
    options={"py2exe": {"includes":["Tkinter", "PIL", "fileinput", "pyaudio", "wave", "threading", "mywindows"]}}
)
