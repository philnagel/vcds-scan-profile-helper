import sys
sys.path.append(r'C:\Users\Phil\git-repos\vcds-scan-profile-helper')
from vcds_scan_parser.base import *


import tkinter
from tkinter import *
import tkinter.ttk as ttk

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.scan = MyAutoScan()


        self.master = master
        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.content = ttk.Frame(self.master)

        self.frame = ttk.Frame(self.content, borderwidth=5)
        self.create_widgets()
        self.grid_widgets()


    def onselect(_, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        print('You selected item %d: "%s"' % (index, value))


    def create_widgets(self):
        self.cars_title = Label(self.frame, text='Current Cars')
        self.car_list = Listbox(self.frame)
        self.car_list.bind('<<ListboxSelect>>', self.onselect)
        for idx, car in enumerate(self.scan.cars):
            self.car_list.insert(idx, '{}: {}'.format(car, self.scan.cars[car]['description']))

        self.add_car = Button(self.frame, text='Add from Scan', state='disabled')
        self.remove_car = Button(self.frame, text='Remove Car', state='disabled')
        self.discard = Button(self.frame, text='Discard')
        self.save = Button(self.frame, text='Save')
        self.quit = Button(self.frame, text="QUIT", fg="red",
                              command=self.master.destroy)

        self.scan_title = Label(self.frame, text='Available Scans')
        self.scan_list = Listbox(self.frame)
        for idx, logfile in enumerate(self.scan.logfiles):
            self.scan_list.insert(idx, '{}'.format(logfile))

    def grid_widgets(self):
        cc = 0
        self.content.grid(column=cc, row=0)
        self.frame.grid(column=cc, row=0, columnspan=5, rowspan=5)
        self.cars_title.grid(column=cc, row=0, columnspan=2)
        self.car_list.grid(column=cc, row=1, columnspan=2, rowspan=4)

        cc = 2
        self.add_car.grid(column=cc, row=1)
        self.remove_car.grid(column=cc, row=2)
        self.discard.grid(column=cc, row=3)
        self.save.grid(column=cc, row=4)
        self.quit.grid(column=cc, row=5)

        cc = 3
        self.scan_title.grid(column=cc, row=0, columnspan=2)
        self.scan_list.grid(column=cc, row=1, columnspan=2, rowspan=4)


    def say_hi(self):
        print("hi there, everyone!")



root = Tk()
app = Application(master=root)
app.mainloop()