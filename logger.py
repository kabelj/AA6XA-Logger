#Import Python Modules
from tkinter import *
#from tkinter.ttk import *
import tkinter.filedialog as fd
import tkinter.messagebox as md
import csv
import configparser
from datetime import datetime
from dateutil import parser
import re
import glob

#Import other logger modules
import adifTools
import inputChecking as ck 

#Main Window
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master=master
        self.pack(fill=BOTH, expand=1)

        #Read loggersettings file and set defaults
        self.config = configparser.ConfigParser()
        self.config.read('loggersettings')
        self.callsign = self.config['STATION']['callsign']
        self.myGrid = self.config['STATION']['grid']
        self.defaultPath = self.config['LOGGER']['defaultpath']
        self.rowCount = 0

        #
        #Add Menus
        #
        # Two menus to start
        #   File - Open/New/Exit
        #   Export - SOTA/ADIF/VHF/NAQP
        # 
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Open Log",command=self.openLog)
        fileMenu.add_command(label="New Log",command=self.newLog)
        fileMenu.add_command(label="Exit",command=self.clickExitBtn)
        menu.add_cascade(label="File",menu=fileMenu)

        #exportMenu = Menu(menu)
        #exportMenu.add_command(label="SOTA CSV",command=self.exportSota)
        #exportMenu.add_command(label="ADIF",command=self.exportWwff)
        #exportMenu.add_command(label="VHF Contest",command=self.vhfTest)
        #exportMenu.add_command(label="NAQP Contest",command=self.naqp)
        #menu.add_cascade(label="Export", menu=exportMenu)

        #
        #Data Entry Fields
        #
        # Put each section in a frame.
        #   Date/Time/Call/Freq/Mode
        #   RST/RST/QTH/Power
        #   Name/State
        #   Grid
        #   SOTA/SOTA/WWFF
        # I think this breakdown will allow frames to be turned on and off to 
        # make the GUI able to support different activities better.
        #

        # Tbe Basic Frame will have the info that is always required
        #  - Date (Day/Month/Year format)
        #  - Time (UTC)
        #  - Call
        #  - Frequency (MHz)
        #  - Mode
        self.basic_frame = Frame(self, bg='yellow')
        self.basic_frame.grid(row=0, column=0, columnspan=2)

        dateTxt = Label(self.basic_frame, text='Date (D/M/Y)')
        dateTxt.grid(row=0, column=0, sticky="E", padx=5, pady=5)
        self.dateEnt = Entry(self.basic_frame, width=10)
        self.dateEnt.grid(row=0, column=1, sticky="W")

        timeTxt = Label(self.basic_frame, text="Time (UTC)")
        timeTxt.grid(row=0, column=2, sticky="E")
        self.timeEnt = Entry(self.basic_frame, width=4)
        self.timeEnt.grid(row=0, column=3, sticky="W")
        self.timeEnt.bind("<FocusOut>", \
            lambda event:ck.checkTime(self.timeEnt.get()))

        callTxt = Label(self.basic_frame, text="Callisign")
        callTxt.grid(row=1, column=0, sticky="E")
        self.callEnt = Entry(self.basic_frame, width=10)
        self.callEnt.grid(row=1, column=1, sticky="W")
        self.callEnt.bind("<FocusOut>", lambda event:self.callToCaps())

        freqTxt = Label(self.basic_frame, text="Freq (MHz)")
        freqTxt.grid(row=1, column=2, sticky="E")
        self.freqEnt = Entry(self.basic_frame, width=9)
        self.freqEnt.grid(row=1, column=3, sticky="W")

        modeTxt = Label(self.basic_frame, text="Mode")
        modeTxt.grid(row=1,column=4,sticky="E")
        choices = {'CW','SSB','FM','DIGI'}
        self.modeEnt = StringVar(self)
        self.modeEnt.set('CW')
        popupMenu = OptionMenu(self.basic_frame, self.modeEnt, *choices)
        popupMenu.grid(row=1,column=5,sticky="W")

        # The common frame will have stuff that is commonly recorded 
        #  - RST Sent
        #  - RST Received
        #  - QTH
        #  - Power
        self.common_frame = Frame(self, bg='blue')
        self.common_frame.grid(row=1, column=0)

        rstSentTxt = Label(self.common_frame, text="RST Sent")
        rstSentTxt.grid(row=0, column=0, sticky="E", padx=8, pady=8)
        self.rstSentEnt = Entry(self.common_frame, width=3)
        self.rstSentEnt.grid(row=0, column=1, sticky="W")

        rstRxTxt = Label(self.common_frame, text="RST Rcv'd")
        rstRxTxt.grid(row=0, column=2, sticky="E")
        self.rstRxEnt = Entry(self.common_frame, width=3)
        self.rstRxEnt.grid(row=0, column=3, sticky="W")

        qthTxt = Label(self.common_frame, text="QTH")
        qthTxt.grid(row=0, column=4, sticky="E")
        self.qthEnt = Entry(self.common_frame, width=10)
        self.qthEnt.grid(row=0, column=5)

        pwrTxt = Label(self.common_frame, text="Power")
        pwrTxt.grid(row=0, column=6, sticky="E")
        self.pwrEnt = Entry(self.common_frame, width=4)
        self.pwrEnt.grid(row=0, column=7, sticky="W")

        # The NAQP frame will have the NAQP exchange info
        #  - Name
        #  - State
        self.naqp_frame = Frame(self, bg='green')
        self.naqp_frame.grid(row=2, column=0)

        nameTxt = Label(self.naqp_frame, text="Name")
        nameTxt.grid(row=0, column=0, sticky="E", padx=5, pady=5)
        self.nameEnt = Entry(self.naqp_frame, width=10)
        self.nameEnt.grid(row=0, column=1, sticky="W")

        stateTxt = Label(self.naqp_frame, text="State")
        stateTxt.grid(row=0, column=2, sticky="E")
        self.stateEnt = Entry(self.naqp_frame, width=2)
        self.stateEnt.grid(row=0, column=3, sticky="W")

        # The VHF Frame has stuff for VHF+ contests
        #  - Grid square, 4 or 6 character
        self.vhf_frame = Frame(self, bg='red')
        self.vhf_frame.grid(row=2, column=1)

        gridTxt = Label(self.vhf_frame, text="Grid")
        gridTxt.grid(row=0, column=0, sticky="E", padx=3, pady=3)
        self.gridEnt = Entry(self.vhf_frame, width=6)
        self.gridEnt.grid(row=0, column=1, sticky="W")

        # The SOTA frame contains portable references
        #  - My SOTA Ref
        #  - SOTA Ref
        #  - WWFF (POTA) Ref
        self.sota_frame = Frame(self, bg='purple')
        self.sota_frame.grid(row=3, column=0)

        sotaTxt = Label(self.sota_frame, text="My SOTA Peak")
        sotaTxt.grid(row=0,column=0,sticky="E", padx=5, pady=5)
        self.sotaEnt = Entry(self.sota_frame, width=10)
        self.sotaEnt.grid(row=0,column=1,sticky="W")

        s2sTxt = Label(self.sota_frame, text="S2S Peak")
        s2sTxt.grid(row=0,column=2,sticky="E")
        self.s2sEnt = Entry(self.sota_frame, width=10)
        self.s2sEnt.grid(row=0,column=3,sticky="W")

        wwffTxt = Label(self.sota_frame, text="Park Ref")
        wwffTxt.grid(row=0,column=4,sticky="E")
        self.wwffEnt = Entry(self.sota_frame, width=9)
        self.wwffEnt.grid(row=0,column=5,sticky="W")


    def callToCaps(self):
        call = self.callEnt.get()
        self.callEnt.delete(0,'end')
        self.callEnt.insert(0,call.upper())
        #Callsign required, don't let them move on until its entered
        if not call:
            self.callEnt.focus_set()


    def openLog(self):
        #File open Dialog
        filetypes = (('Log Files','*.log'),('All Files','*.*'))
        self.logFile = fd.askopenfilename(initialdir=self.defaultPath,\
            filetypes=filetypes,title='Select Log File')
        #Set edit in gui
        self.logNameEnt.delete(0,'end')
        self.logNameEnt.insert(0,self.logFile)

        #count number of lines
        self.rowCount = 0
        self.logFile = open(self.logNameEnt.get(),'r')
        logReader = csv.reader(self.logFile)
        for row in logReader:
            self.rowCount += 1
        self.logFile.close()

        #update list on screen
        qsoText = ''
        lineNums = [self.rowCount-5, self.rowCount-4, self.rowCount-3, \
            self.rowCount-2, self.rowCount-1]
        f = open(self.logNameEnt.get(),'r')
        logReader = csv.reader(f)
        count = -1
        for row in logReader:
            count += 1
            if count in lineNums:
                text = ', '.join(row)
                qsoText = qsoText+text+'\n'
        self.qsoListTxt.configure(text=qsoText)
        f.close()

    def newLog(self):
        #File dialog
        filetypes = (('Log Files','*.log'),('All Files','*.*'))
        self.logFile = fd.asksaveasfilename(initialdir=self.defaultPath,\
            filetypes=filetypes,title='New Log File')
        #Set the text in the gui
        self.logNameEnt.delete(0,'end')
        self.logNameEnt.insert(0,self.logFile)
        #clear fields
        self.dateEnt.delete(0,'end')
        self.timeEnt.delete(0,'end')
        self.callEnt.delete(0,'end')
        self.freqEnt.delete(0,'end')
        self.rstSentEnt.delete(0,'end')
        self.rstRxEnt.delete(0,'end')
        self.nameEnt.delete(0,'end')
        self.qthEnt.delete(0,'end')
        self.stateEnt.delete(0,'end')
        self.gridEnt.delete(0,'end')
        self.pwrEnt.delete(0,'end')
        self.sotaEnt.delete(0,'end')
        self.s2sEnt.delete(0,'end')
        self.wwffEnt.delete(0,'end')
        self.qsoListTxt.configure(text='No QSOs yet')
        self.timeEnt.focus_set()

    def clickExitBtn(self):
        exit()



#Get it running
version = '1.0'
root = Tk()
app = Window(root)
root.title('AA6XA Logger, v'+version)
root.geometry('800x300')
root.config(bg='gray80')

root.mainloop()
