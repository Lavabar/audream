import Tkinter as tk

import mywindows as win

root = tk.Tk()
#root.wm_iconbitmap("./icon.ico")
root.withdraw()
win.showAdv(root)

root.mainloop()
