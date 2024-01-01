import tarfile
from zipfile import ZipFile
import py7zr
from rarfile import RarFile
import tkinter.messagebox as tkmb
import tkinter as tk
from tkinter.ttk import *
from tkinter import *
import os
import re
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

filename = 'Not selected'
folder_path = 'Not selected'
type1 = 'tar'
type2 = 'rar'
type3 = 'zip'


class MyWindow:
    def __init__(self, win):
        menubar = Menu()
        window.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New Job', command=lambda: clear_globals())
        file_menu.add_command(label='Open File', command=lambda: open_file(self))
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=window.destroy)

        help_ = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Simple Archive Handler Help', command=lambda: open_win_h1())
        help_.add_separator()
        help_.add_command(label='About', command=lambda: open_win_h2())


        self.b1 = Button(win, width=15, text='Extract archive', command=lambda: extract_archive())
        self.b2 = Button(win, text='Select Output Folder', command=lambda: working_folder(self))
        self.b3 = Button(win, width=15, text='Select file', command=lambda: open_file(self))
        self.b1.place(x=160, y=290)
        self.b2.place(x=10, y=150)
        self.b3.place(x=10, y=50)
        listbox1(self, window)
        listbox2(self, window)


def listbox1(self, win):
    head1, tail1 = os.path.split(filename)
    self.lb1 = Listbox(win, height=3, width=40, selectmode='multiple')
    self.lb1.insert(END, '')
    self.lb1.insert(END, tail1)
    self.lb1.place(x=150, y=50)


def listbox2(self, win):
    head2, tail2 = os.path.split(folder_path)
    self.lb2 = Listbox(win, height=3, width=40, selectmode='multiple')
    self.lb2.insert(END, head2)
    self.lb2.insert(ANCHOR, tail2)
    self.lb2.place(x=150, y=150)


def open_file(self):
    file = askopenfilename(filetypes=[('all files', '*.*')])
    global filename
    filename = file
    listbox1(self, window)
    print(filename)


def working_folder(self):
    global folder_path
    folder_path = filedialog.askdirectory()
    listbox2(self, window)
    print(folder_path)


def extract_archive():
    if filename.endswith('.tar*'):
        arcfile = tarfile.open(filename)
        arcfile.extractall(folder_path)
        arcfile.close()

    elif filename.endswith('.rar'):
        RarFile.UNRAR_TOOL = r"C:\Program Files (x86)\UnrarDLL\UnRAR.exe"
        arcfile = RarFile(filename)
        arcfile.extractall(path=folder_path)
        arcfile.close()

    elif filename.endswith('.zip'):
        with ZipFile(filename,  mode='r') as zp:
            zp.extractall(path=folder_path)
            zp.close()

    elif filename.endswith('.7z'):
        with py7zr.SevenZipFile(filename, mode='r') as z:
            z.extractall(path=folder_path)

    else: tkmb.showinfo("Message", "Error")


def open_win_h1():
    h1 = tk.Toplevel(window)
    h1.geometry("570x400")
    h1.title("Simple Archive Handler Help")
    h1.iconbitmap(r"C:\Users\msste\PycharmProjects\pythonProject\PDF Handler\Simple PDF Handler.ico")
    help_topics = '''
                  Help Topics:
                  1. Quick task on Main Window:
                  1.1 Extract archive
                  Supported formats: TAR, RAR, ZIP, 7Z
                  Note: In order to extract RAR type archive, a correct path to UnRAR.exe file should be added to the code. 
                  To run the task, the source files and an output folder should be selected.

                  2. File Menu Tasks:
                  2.1 New job can be called to clear all inputs
                  2.2 Open files menu item is used to browse for files 
                  2.3 Exit command will close the program

                  '''
    help_topics = re.sub("\n\s*", "\n", help_topics)  # remove leading whitespace from each line
    h = CustomText(h1, wrap="word", width=100, height=10, borderwidth=0)
    h.tag_configure("blue", foreground="blue")
    h.pack(sid="top", fill="both", expand=True)
    h.insert("1.0", help_topics)
    #h.HighlightPattern("^.*? - ", "blue")
    tk.Button(h1, text='OK', command=h1.destroy).pack()


def open_win_h2():
    h2 = tk.Toplevel(window)
    h2.geometry("250x200")
    h2.title("About Simple Archive Handler")
    h2.iconbitmap(r"C:\Users\msste\PycharmProjects\pythonProject\PDF Handler\Simple PDF Handler.ico")
    about = '''
           Simple Archive Handler
           Program version: 1.3.1
           Author: Maksym Stetsenko
           '''
    about = re.sub("\n\s*", "\n", about)
    t = CustomText(h2, wrap="word", width=100, height=10, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top", fill="both", expand=True)
    t.insert("1.0", about)
    #t.HighlightPattern("Maksym Stetsenko", "blue")
    tk.Button(h2, text='OK', command=h2.destroy).pack()


def clear_globals():
    global filename
    global folder_path
    filename = 'Not selected'
    folder_path = 'Not selected'
    MyWindow(window)


class CustomText(tk.Text):
    '''A text widget with a new method, HighlightPattern
    example:
    text = CustomText()
    text.tag_configure("red",foreground="#ff0000")
    text.HighlightPattern("this should be red", "red")
    The HighlightPattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def HighlightPattern(self, pattern, tag, start="1.0", end="end", regexp=True):
        '''Apply the given tag to all text that matches the given pattern'''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", end)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


window = tk.Tk()
mywin = MyWindow(window)
window.title('Archive Handler')
window.geometry("450x350+10+10")
window.iconbitmap(r"C:\Users\msste\PycharmProjects\pythonProject\PDF Handler\Simple PDF Handler.ico")

window.mainloop()
