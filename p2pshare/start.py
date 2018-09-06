import tkinter as tk

from p2pshare import WINDOW_SIZE, APP_NAME
from p2pshare.frame import MainFrame

if __name__ == '__main__':
    master = tk.Tk()
    master.title(APP_NAME)
    screenwidth = master.winfo_screenwidth()
    screenheight = master.winfo_screenheight()
    pos = (screenwidth - WINDOW_SIZE[0]) / 2, (screenheight - WINDOW_SIZE[1]) / 2
    master.geometry('%dx%d+%d+%d' % (WINDOW_SIZE[0], WINDOW_SIZE[1], pos[0], pos[1]))
    mf = MainFrame(root=master)
    mf.grid()
    master.mainloop()
