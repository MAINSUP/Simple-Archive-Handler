import tarfile
import zipfile
#import rarfile
import tkinter as tk
from tkinter.ttk import *
from tkinter import *
import os
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

        self.btn1 = Button(win, text='Extract archive')
        self.btn2 = Button(win, text='Browse File Directory')
        self.b1 = Button(win, width=15, text='Extract archive',command=lambda: extract_archive())
        self.b2 = Button(win, text='Select Output Folder', command=lambda: working_folder(self))
        self.b1.place(x=10, y=50)
        self.b2.place(x=10, y=150)
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
    if type1 in str(filename):
       file = tarfile.open(filename)
       file.extractall(folder_path)
       file.close()
    elif type3 in str(filename):
       file = zipfile.open(filename)
       file = zipfile.extractall(path=folder_path)
       file.close()
    else: print('error')

def clear_globals():
    global filename
    global folder_path
    filename = 'Not selected'
    folder_path = 'Not selected'


window = tk.Tk()
mywin = MyWindow(window)
window.title('Archive Handler')
window.geometry("450x350+10+10")
window.iconbitmap(r"C:\Users\msste\PycharmProjects\pythonProject\Simple PDF Handler.ico")

window.mainloop()

