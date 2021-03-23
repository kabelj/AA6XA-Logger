from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as md
import csv
from datetime import datetime

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master=master
        self.pack(fill=BOTH, expand=1)

        #Defaults, for now
        self.callsign = 'AA6XA'

        #Add Menus
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Open Log", command=self.openLog)
        fileMenu.add_command(label="New Log", command=self.newLog)
        fileMenu.add_command(label="Exit", command=self.clickExitBtn)
        menu.add_cascade(label="File", menu=fileMenu)

        exportMenu = Menu(menu)
        exportMenu.add_command(label="SOTA CSV",command=self.exportSota)
        exportMenu.add_command(label="WWFF ADIF",command=self.exportWwff)
        exportMenu.add_command(label="VHF Contest",command=self.vhfTest)
        menu.add_cascade(label="Export", menu=exportMenu)

        #Data Entry Fields
        #Date
        dateTxt = Label(self, text="Date")
        dateTxt.grid(row=0,column=0)
        self.dateEnt = Entry(self,width=10)
        self.dateEnt.grid(row=0,column=1)
        #Time
        timeTxt = Label(self, text="Time (UTC)")
        timeTxt.grid(row=0,column=2)
        self.timeEnt = Entry(self, width=4)
        self.timeEnt.grid(row=0,column=3)
        #Callsign
        callTxt = Label(self, text="Callsign")
        callTxt.grid(row=0,column=4)
        self.callEnt = Entry(self, width=10)
        self.callEnt.grid(row=0,column=5)
        #Frequency
        freqTxt = Label(self, text="Frequency")
        freqTxt.grid(row=0,column=6)
        self.freqEnt = Entry(self, width=9)
        self.freqEnt.grid(row=0,column=7)
        #RST Sent
        rstSentTxt = Label(self, text="RST Sent")
        rstSentTxt.grid(row=1,column=0)
        self.rstSentEnt = Entry(self, width=3)
        self.rstSentEnt.grid(row=1,column=1)
        #RST Received
        rstRxTxt = Label(self, text="RST Received")
        rstRxTxt.grid(row=1,column=2)
        self.rstRxEnt = Entry(self, width=3)
        self.rstRxEnt.grid(row=1,column=3)
        #Name
        nameTxt = Label(self, text="Name")
        nameTxt.grid(row=1,column=4)
        self.nameEnt = Entry(self, width=10)
        self.nameEnt.grid(row=1,column=5)
        #QTH
        qthTxt = Label(self, text="QTH")
        qthTxt.grid(row=1,column=6)
        self.qthEnt = Entry(self, width=10)
        self.qthEnt.grid(row=1,column=7)
        #State
        stateTxt = Label(self, text="State")
        stateTxt.grid(row=2,column=0)
        self.stateEnt = Entry(self, width=3)
        self.stateEnt.grid(row=2, column=1)
        #Grid
        gridTxt = Label(self, text="Grid")
        gridTxt.grid(row=2,column=2)
        self.gridEnt = Entry(self, width=6)
        self.gridEnt.grid(row=2,column=3)
        #Power
        pwrTxt = Label(self, text="Power")
        pwrTxt.grid(row=2,column=4)
        self.pwrEnt = Entry(self,width=4)
        self.pwrEnt.grid(row=2,column=5)
        #Mode
        modeTxt = Label(self, text="Mode")
        modeTxt.grid(row=2,column=6)
        self.modeEnt = Entry(self, width=4)
        self.modeEnt.insert(0,"CW")
        self.modeEnt.grid(row=2,column=7)
        #SOTA Peak
        sotaTxt = Label(self, text="SOTA Peak")
        sotaTxt.grid(row=3,column=0)
        self.sotaEnt = Entry(self, width=10)
        self.sotaEnt.grid(row=3,column=1)
        #S2S Peak
        s2sTxt = Label(self, text="S2S Peak")
        s2sTxt.grid(row=3,column=2)
        self.s2sEnt = Entry(self, width=10)
        self.s2sEnt.grid(row=3,column=3)
        #WWFF Ref
        wwffTxt = Label(self, text="WWFF Ref")
        wwffTxt.grid(row=3,column=4)
        self.wwffEnt = Entry(self, width=9)
        self.wwffEnt.grid(row=3,column=5)

        #log File Name
        logNameTxt = Label(self, text="Log Filename")
        logNameTxt.grid(row=7,column=0)
        self.logNameEnt = Entry(self,width=35)
        self.logNameEnt.grid(row=7,column=1,columnspan=4)
        #SOTA CSV File name
        sotaNameTxt = Label(self, text="SOTA Filename")
        sotaNameTxt.grid(row=8,column=0)
        self.sotaNameEnt = Entry(self,width=30)
        self.sotaNameEnt.grid(row=8,column=1,columnspan=3)
        #ADIF Filename
        adifNameTxt = Label(self, text="ADIF Filename")
        adifNameTxt.grid(row=8,column=4)
        self.adifNameEnt = Entry(self,width=30)
        self.adifNameEnt.grid(row=8,column=5,columnspan=3)

        #QSO List
        self.qsoListTxt = Label(self, bg="white",text="test")
        self.qsoListTxt.grid(row=10,column=0,columnspan=8,rowspan=3)

        #Log Button
        logBtn = Button(self, text="Log QSO", command=self.logQsoBtn)
        logBtn.grid(row=7,column=5) #place(x=300,y=200)
        #Exit Button
        exitBtn = Button(self, text="Exit", command=self.clickExitBtn)
        exitBtn.grid(row=7,column=7)

    def clickExitBtn(self):
        exit()

    def logQsoBtn(self):
        #make sure we have a valid log name to save to
        #if self.logFile==''
        #    self.logFile=self.logNameEnt.get()

        self.logFile = open(self.logNameEnt.get(),'a+')

        #get data from text fields
        date = self.dateEnt.get()
        time = self.timeEnt.get()
        call = self.callEnt.get()
        freq = self.freqEnt.get()
        rstS = self.rstSentEnt.get()
        rstR = self.rstRxEnt.get()
        name = self.nameEnt.get()
        qth = self.qthEnt.get()
        state = self.stateEnt.get()
        grid = self.gridEnt.get()
        power = self.pwrEnt.get()
        mode = self.modeEnt.get()
        sota = self.sotaEnt.get()
        s2s = self.s2sEnt.get()
        wwff = self.wwffEnt.get()
        #write into a big string
        qso = date+','+time+','+call+','+freq+','+rstS+','+rstR+','+\
            name+','+qth+','+state+','+grid+','+power+','+mode+','+\
            sota+','+s2s+','+wwff+'\n'
        #write to the log
        self.logFile.write(qso)
        #update list on screen
        qsoList = ['']*5
        for i in range(0,4):
            qsoList[i] = self.logFile.readline()
        self.qsoListTxt.configure(text=qso)
        #clear fields
        self.timeEnt.delete(0,'end')
        self.callEnt.delete(0,'end')
        self.nameEnt.delete(0,'end')
        self.qthEnt.delete(0,'end')
        self.stateEnt.delete(0,'end')
        self.gridEnt.delete(0,'end')
        self.s2sEnt.delete(0,'end')
        self.timeEnt.focus_set()
        self.logFile.close()

    def exportSota(self):
        #open the SOTA CSV file
        if self.sotaNameEnt.get()=='':
            filetypes = (('CSV Files','*.csv'),('All Files','*.*'))
            fname = fd.asksaveasfilename(initialdir='./',\
                filetypes=filetypes,title='CSV File Name')
            self.sotaNameEnt.insert(0,fname)
            fSota = open(fname,'w')
        else:
            fSota = open(self.sotaNameEnt.get(),'w')
        self.logFile = open(self.logNameEnt.get(),'r')

        #Read each line in the log, write corresponding line to CSV
        reader = csv.reader(self.logFile)
        writer = csv.writer(fSota)

        for row in reader:
            writer.writerow(['V2',self.callsign,row[12],row[0],row[1],\
                row[3],row[11],row[2],row[13]])

        fSota.close()

    def exportWwff(self):
        #Open the adif file
        self.logFile = open(self.logNameEnt.get(),'r')
        if self.adifNameEnt.get()=='':
            filetypes = (('ADIF Files','*.adi'),('All Files','*.*'))
            fname = fd.asksaveasfilename(initialdir='./',\
                filetypes=filetypes,title='ADIF File Name')
            self.adifNameEnt.insert(0,fname)
            self.fAdif = open(fname,'w')
        else:
            self.fAdif = open(self.adifNameEnt.get(),'w')

        #Write ADIF Header
        self.writeAdifHeader()

        #Read each line, convert to adif form
        reader = csv.reader(self.logFile)
        rownum = 0
        adifData = []
        for row in reader:
            self.writeAdif(row)

        self.fAdif.close()
        self.logFile.close()

    def writeAdif(self, row):
        band = self.freqToBand(row[3])
        self.fAdif.write("<operator:"+str(len(self.callsign))+\
            ">"+self.callsign)
        self.fAdif.write("<call:"+str(len(row[2]))+">"+row[2])
        self.fAdif.write("<qso_date:"+str(len(row[0]))+">"+row[0])
        self.fAdif.write("<qso_date_off:>"+str(len(row[0]))+">"+row[0])
        self.fAdif.write("<time_on:"+str(len(row[1]))+">"+row[1])
        self.fAdif.write("<time_off:"+str(len(row[1]))+">"+row[1])
        self.fAdif.write("<freq:"+str(len(row[3]))+">"+row[3])
        self.fAdif.write("<band:"+str(len(band))+">"+band)
        self.fAdif.write("<mode:"+str(len(row[11]))+">"+row[11])
        self.fAdif.write("<rst_sent:"+str(len(row[4]))+">"+row[4])
        self.fAdif.write("<rst_rcvd:"+str(len(row[5]))+">"+row[5])
        self.fAdif.write("<state:"+str(len(row[8]))+">"+row[8])
        self.fAdif.write("<qth:"+str(len(row[7]))+">"+row[7])
        self.fAdif.write("<tx_pwr:"+str(len(row[10]))+">"+row[10])
        self.fAdif.write("<my_sota_ref:"+str(len(row[12]))+">"+row[12])
        self.fAdif.write("<sota_ref:"+str(len(row[13]))+">"+row[13])
        self.fAdif.write("<my_sig_info:"+str(len(row[14]))+">"+row[14])
        self.fAdif.write("<gridsquare:"+str(len(row[9]))+">"+row[9])
        self.fAdif.write("<eor>\n")

    def writeAdifHeader(self):
        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.fAdif.write("Exported on "+now+' for '+self.callsign+'\n')
        self.fAdif.write("\n<ADIF_VER:5>3.1.0 \n")
        self.fAdif.write("<PROGRAMID:12>AA6XA logger \n")
        self.fAdif.write("<PROGRAMVERSION:3>0.1 \n<EOH>\n\n")

    def freqToBand(self, freq):
        #Note: freq is assumed to be a string.
        #To Do: check the type of freq
        mhz = int(float(freq))
        if mhz==1:
            band='160m'
        elif mhz==3:
            band='80m'
        elif mhz==5:
            band='60m'
        elif mhz==7:
            band='40m'
        elif mhz==10:
            band='30m'
        elif mhz==14:
            band='20m'
        elif mhz==18:
            band='17m'
        elif mhz==21:
            band='15m'
        elif mhz==24:
            band='12m'
        elif mhz==28 or mhz==29:
            band='10m'
        elif mhz>=50 and mhz<=54:
            band='6m'
        elif mhz>=144 and mhz<=148:
            band='2m'
        elif mhz>=222 and mhz<=225:
            band='1.25m'
        elif mhz>=420 and mhz<=450:
            band='70cm'
        elif mhz>=902 and mhz<=928:
            band='33cm'
        elif mhz>=1240 and mhz<=1300:
            band='23cm'
        elif mhz>=10000 and mhz<=10500:
            band='3cm'
        elif mhz>=119980 and mhz<=120020:
            band='2.5mm'
        else:
            md.showerror('Not a band',\
                'Entered frequency is not in a supported band')
            band = -1
        return band

    def vhfTest(self):
        print("Exported VHF Contest Log")

    def openLog(self):
        #File open Dialog
        filetypes = (('Log Files','*.log'),('All Files','*.*'))
        self.logFile = fd.askopenfilename(initialdir='./',\
            filetypes=filetypes,title='Select Log File')
        #Set edit in gui
        self.logNameEnt.insert(0,self.logFile)

    def newLog(self):
        #File dialog
        filetypes = (('Log Files','*.log'),('All Files','*.*'))
        self.logFile = fd.asksaveasfilename(initialdir='./',\
            filetypes=filetypes,title='New Log File')
        #Set the text in the gui
        self.logNameEnt.insert(0,self.logFile)


root=Tk()
#dateText=StringVar()

app=Window(root)

root.wm_title("AA6XA Logger, v0.1")
root.geometry("810x300")
root.mainloop()
