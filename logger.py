from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as md
import csv
import configparser
from datetime import datetime
from dateutil import parser
import re
import glob

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master=master
        self.pack(fill=BOTH, expand=1)

        #Read and set defaults
        self.config = configparser.ConfigParser()
        self.config.read('loggersettings')
        self.callsign = self.config['STATION']['callsign']
        self.myGrid = self.config['STATION']['grid']
        self.defaultPath = self.config['LOGGER']['defaultpath']
        self.rowCount = 0


        #Add Menus
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Open Log",command=self.openLog)
        fileMenu.add_command(label="New Log",command=self.newLog)
        fileMenu.add_command(label="Exit",command=self.clickExitBtn)
        menu.add_cascade(label="File",menu=fileMenu)

        exportMenu = Menu(menu)
        exportMenu.add_command(label="SOTA CSV",command=self.exportSota)
        exportMenu.add_command(label="WWFF ADIF",command=self.exportWwff)
        exportMenu.add_command(label="VHF Contest",command=self.vhfTest)
        exportMenu.add_command(label="NAQP Contest",command=self.naqp)
        menu.add_cascade(label="Export", menu=exportMenu)

        #Data Entry Fields
        #Date
        dateTxt = Label(self, text="Date (D/M/Y)")
        dateTxt.grid(row=0,column=0,sticky="E")
        self.dateEnt = Entry(self,width=10)
        self.dateEnt.grid(row=0,column=1)
        #Time
        timeTxt = Label(self, text="Time (UTC)")
        timeTxt.grid(row=0,column=2,sticky="E")
        self.timeEnt = Entry(self, width=4)
        self.timeEnt.grid(row=0,column=3,sticky="W")
        self.timeEnt.bind("<FocusOut>", lambda event:self.checkTime())
        #Callsign
        callTxt = Label(self, text="Callsign")
        callTxt.grid(row=0,column=4,sticky='E')
        self.callEnt = Entry(self, width=10)
        self.callEnt.grid(row=0,column=5,sticky="W")
        self.callEnt.bind('<FocusOut>', lambda event:self.callToCaps())
        #Frequency
        freqTxt = Label(self, text="Freq (MHz)")
        freqTxt.grid(row=0,column=6,sticky="E")
        self.freqEnt = Entry(self, width=9)
        self.freqEnt.grid(row=0,column=7,sticky="W")
        #RST Sent
        rstSentTxt = Label(self, text="RST Sent")
        rstSentTxt.grid(row=1,column=0,sticky="E")
        self.rstSentEnt = Entry(self, width=3)
        self.rstSentEnt.grid(row=1,column=1,sticky="W")
        self.rstSentEnt.bind("<FocusOut>", lambda event:self.rstSCheck())
        #RST Received
        rstRxTxt = Label(self, text="RST Rcv'd")
        rstRxTxt.grid(row=1,column=2,sticky="E")
        self.rstRxEnt = Entry(self, width=3)
        self.rstRxEnt.grid(row=1,column=3,sticky="W")
        self.rstRxEnt.bind("<FocusOut>", lambda event:self.rstRCheck())
        #Name
        nameTxt = Label(self, text="Name")
        nameTxt.grid(row=1,column=4,sticky="E")
        self.nameEnt = Entry(self, width=10)
        self.nameEnt.grid(row=1,column=5,sticky="W")
        #QTH
        qthTxt = Label(self, text="QTH")
        qthTxt.grid(row=1,column=6,sticky="E")
        self.qthEnt = Entry(self, width=10)
        self.qthEnt.grid(row=1,column=7,sticky="W")
        #State
        stateTxt = Label(self, text="State")
        stateTxt.grid(row=2,column=0,sticky="E")
        self.stateEnt = Entry(self, width=3)
        self.stateEnt.grid(row=2, column=1,sticky="W")
        self.stateEnt.bind("<FocusOut>", lambda event:self.stateToCaps())
        #Grid
        gridTxt = Label(self, text="Grid")
        gridTxt.grid(row=2,column=2,sticky="E")
        self.gridEnt = Entry(self, width=6)
        self.gridEnt.grid(row=2,column=3,sticky="W")
        self.gridEnt.bind("<FocusOut>", lambda event:self.gridToCaps())
        #Power
        pwrTxt = Label(self, text="Power")
        pwrTxt.grid(row=2,column=4,sticky="E")
        self.pwrEnt = Entry(self,width=4)
        self.pwrEnt.grid(row=2,column=5,sticky="W")
        #Mode
        modeTxt = Label(self, text="Mode")
        modeTxt.grid(row=2,column=6,sticky="E")
        choices = {'CW','SSB','FM','DIGI'}
        self.modeEnt = StringVar(self)
        self.modeEnt.set('CW')
        popupMenu = OptionMenu(self, self.modeEnt, *choices)
        popupMenu.grid(row=2,column=7,sticky="W")
        #SOTA Peak
        sotaTxt = Label(self, text="My SOTA Peak")
        sotaTxt.grid(row=3,column=0,sticky="E")
        self.sotaEnt = Entry(self, width=10)
        self.sotaEnt.grid(row=3,column=1,sticky="W")
        self.sotaEnt.bind("<FocusOut>", lambda event:self.sotaToCaps())
        #S2S Peak
        s2sTxt = Label(self, text="S2S Peak")
        s2sTxt.grid(row=3,column=2,sticky="E")
        self.s2sEnt = Entry(self, width=10)
        self.s2sEnt.grid(row=3,column=3,sticky="W")
        self.s2sEnt.bind("<FocusOut>", lambda event:self.s2sToCaps())
        #WWFF Ref
        wwffTxt = Label(self, text="Park Ref")
        wwffTxt.grid(row=3,column=4,sticky="E")
        self.wwffEnt = Entry(self, width=9)
        self.wwffEnt.grid(row=3,column=5,sticky="W")
        self.wwffEnt.bind("<FocusOut>", lambda event:self.wwffToCaps())

        #log File Name
        logNameTxt = Label(self, text="Log File")
        logNameTxt.grid(row=7,column=0,sticky="E")
        self.logNameEnt = Entry(self,width=35)
        self.logNameEnt.grid(row=7,column=1,columnspan=4,sticky="W")
        #SOTA CSV File name
        sotaNameTxt = Label(self, text="SOTA File")
        sotaNameTxt.grid(row=8,column=0,sticky="E")
        self.sotaNameEnt = Entry(self,width=30)
        self.sotaNameEnt.grid(row=8,column=1,columnspan=3,sticky="W")
        #ADIF Filename
        adifNameTxt = Label(self, text="ADIF File")
        adifNameTxt.grid(row=8,column=4,sticky="E")
        self.adifNameEnt = Entry(self,width=30)
        self.adifNameEnt.grid(row=8,column=5,columnspan=3,sticky="W")
        #Cabrillo Filename
        vhfNameTxt = Label(self, text="Cabrillo File")
        vhfNameTxt.grid(row=9,column=0,sticky="E")
        self.cabNameEnt = Entry(self,width=30)
        self.cabNameEnt.grid(row=9,column=1,columnspan=3,sticky="W")

        #QSO List
        self.qsoListTxt = Label(self, bg="white",text="No entries yet")
        self.qsoListTxt.grid(row=10,column=0,columnspan=8,rowspan=3)

        #Log Button
        self.logBtn = Button(self, text="Log QSO", command=self.logQsoBtn)
        self.logBtn.grid(row=7,column=5)
        #Exit Button
        exitBtn = Button(self, text="Exit", command=self.clickExitBtn)
        exitBtn.grid(row=7,column=7)

        #check if there are other .log files. If not, prompt dialog to
        # update loggersettings
        numLogFiles = len(glob.glob1('./', '*.log'))
        if numLogFiles == 1 or numLogFiles == 0:
            md.showwarning(title="Edit Settings",\
                message="Be sure to edit the loggersettings file!")

        #Ask for log file
        filetypes = (('Log Files','*.log'),('All Files','*.*'))
        self.logFile = fd.askopenfilename(initialdir=self.defaultPath,\
            filetypes=filetypes,title='Select Log File')
        try:
            #count number of lines
            self.rowCount = 0
            f = open(self.logFile,'r')
            logReader = csv.reader(f)
            for row in logReader:
                self.rowCount += 1
            f.close()
            #print("Open File row count = ",self.rowCount)

            #update list on screen
            qsoText = ''
            lineNums = [self.rowCount-5, self.rowCount-4, self.rowCount-3, \
                self.rowCount-2, self.rowCount-1]
            logFile = open(self.logFile,'r')
            logReader = csv.reader(logFile)
            count = -1
            for row in logReader:
                count += 1
                if count in lineNums:
                    text = ', '.join(row)
                    qsoText = qsoText+text+'\n'
            self.qsoListTxt.configure(text=qsoText)
            logFile.close()
        except TypeError:
            pass
        except Exception as e:
            print(e)
            print("Oh no! What have you done?")

        if not self.logFile:
            self.logFile = fd.asksaveasfilename(\
                initialdir=self.defaultPath,\
                filetypes=filetypes,title='New Log File')
            self.rowCount = 0
        #Set edit in gui
        self.logNameEnt.delete(0,'end')
        self.logNameEnt.insert(0,self.logFile)

        #Default <enter> to Log QSO
        master.bind('<Return>',lambda event:self.logQsoBtn())

        #Flags
        self.logFlag = True #Don't log if this is false
        self.vhfBands = {'50','144','222','432','902','1.2G','10G','122G'}
        self.hfBands = {'1800','3500','7000','14000','21000','28000'}

    def clickExitBtn(self):
        exit()

    def logQsoBtn(self):
        #self.timeEnt.focus_set()
        #double check stuff is capitalized
        self.sotaToCaps()
        self.s2sToCaps()
        self.wwffToCaps()

        #open log file
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

        #Validate stuff
        try:
            parser.parse(date,dayfirst=True)
        except ValueError:
            md.showerror("Date Error","Invalid Date!")
            self.dateEnt.focus_set()
            return
        #band=self.freqToBand(freq,False)
        try:
            if self.freqToBand(freq,False)==-1:
                raise ValueError("Oh no! An incorret band was entered!")
        except ValueError:
            md.showerror("Frequency Error",\
                "Invalid Frequency!\n"\
                "The frequency entered is not in a supported band!")
            self.freqEnt.focus_set()
            return
        #add: time,RST,grid, refs?

        #write into a big string
        qso = date+','+time+','+call+','+freq+','+rstS+','+rstR+','+\
            name+','+qth+','+state+','+grid+','+power+','+mode+','+\
            sota+','+s2s+','+wwff+'\n'

        #write to the log
        if self.logFlag:
            self.logFile.write(qso)
        self.logFile.close()

        #update list on screen
        self.rowCount += 1
        qsoText = ''
        lineNums = [self.rowCount-5, self.rowCount-4, self.rowCount-3, \
            self.rowCount-2, self.rowCount-1]
        self.logFile = open(self.logNameEnt.get(),'r')
        logReader = csv.reader(self.logFile)
        count = -1
        for row in logReader:
            count += 1
            if count in lineNums:
                text = ', '.join(row)
                qsoText = qsoText+text+'\n'
        self.qsoListTxt.configure(text=qsoText)
        self.logFile.close()

        #clear fields
        self.timeEnt.delete(0,'end')
        self.callEnt.delete(0,'end')
        self.nameEnt.delete(0,'end')
        self.qthEnt.delete(0,'end')
        self.stateEnt.delete(0,'end')
        self.gridEnt.delete(0,'end')
        self.s2sEnt.delete(0,'end')
        self.timeEnt.focus_set()

    def exportSota(self):
        #open the SOTA CSV file
        if self.sotaNameEnt.get()=='':
            filetypes = (('CSV Files','*.csv'),('All Files','*.*'))
            fname = fd.asksaveasfilename(initialdir=self.defaultPath,\
                filetypes=filetypes,title='CSV File Name')
            self.sotaNameEnt.delete(0,'end')
            self.sotaNameEnt.insert(0,fname)
            fSota = open(fname,'w')
        else:
            #fSota = open(self.sotaNameEnt.get(),'w')
            pass
        self.logFile = open(self.logNameEnt.get(),'r')

        #Read each line in the log, write corresponding line to CSV
        reader = csv.reader(self.logFile)
        #writer = csv.writer(fSota, newline='')

        with open(self.sotaNameEnt.get(), 'w', newline='') as fSota:
            writer = csv.writer(fSota)
            for row in reader:
                writer.writerow(['V2',self.callsign,row[12],row[0],row[1],\
                    row[3],row[11],row[2],row[13]])

        #fSota.close()

    def exportWwff(self):
        #Open the adif file
        self.logFile = open(self.logNameEnt.get(),'r')
        if self.adifNameEnt.get()=='':
            filetypes = (('ADIF Files','*.adi'),('All Files','*.*'))
            fname = fd.asksaveasfilename(initialdir=self.defaultPath,\
                filetypes=filetypes,title='ADIF File Name')
            self.adifNameEnt.delete(0,'end')
            self.adifNameEnt.insert(0,fname)
            self.fAdif = open(fname,'w')
        else:
            self.fAdif = open(self.adifNameEnt.get(),'w')

        #Write ADIF Header
        self.writeAdifHeader()

        #Read each line, convert to adif form
        reader = csv.reader(self.logFile)
        #rownum = 0
        #adifData = []
        for row in reader:
            self.writeAdif(row)

        self.fAdif.close()
        self.logFile.close()

    def writeAdif(self, row):
        band = self.freqToBand(row[3],False)
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
        self.fAdif.write("<name:"+str(len(row[6]))+">"+row[6])
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
        self.fAdif.write("Exported on "+now+' for '+self.callsign+' \n')
        self.fAdif.write("\n<ADIF_VER:5>3.1.0 \n")
        self.fAdif.write("<PROGRAMID:12>AA6XA logger \n")
        self.fAdif.write("<PROGRAMVERSION:"+str(len(version))+">"\
            +version+" \n<EOH>\n\n")

    def freqToBand(self, freq, cabrillo):
        #Note: freq is assumed to be a string.
        #To Do: check the type of freq
        mhz = int(float(freq))
        if mhz==1:
            band='160m'
            cabBand='1800'
        elif mhz==3:
            band='80m'
            cabBand='3500'
        elif mhz==5:
            band='60m'
            cabBand='-1'
        elif mhz==7:
            band='40m'
            cabBand='7000'
        elif mhz==10:
            band='30m'
            cabBand='-1'
        elif mhz==14:
            band='20m'
            cabBand='14000'
        elif mhz==18:
            band='17m'
            cabBand='-1'
        elif mhz==21:
            band='15m'
            cabBand='21000'
        elif mhz==24:
            band='12m'
            cabBand='-1'
        elif mhz==28 or mhz==29:
            band='10m'
            cabBand='28000'
        elif mhz>=50 and mhz<54:
            band='6m'
            cabBand='50'
        elif mhz>=144 and mhz<=148:
            band='2m'
            cabBand='144'
        elif mhz>=222 and mhz<=225:
            band='1.25m'
            cabBand='222'
        elif mhz>=420 and mhz<=450:
            band='70cm'
            cabBand='432'
        elif mhz>=902 and mhz<=928:
            band='33cm'
            cabBand='902'
        elif mhz>=1240 and mhz<=1300:
            band='23cm'
            cabBand='1.2G'
        elif mhz>=10000 and mhz<=10500:
            band='3cm'
            cabBand='10G'
        elif mhz>=119980 and mhz<=120020:
            band='2.5mm'
            cabBand='122G'
        else:
            #md.showerror('Not a band',\
            #    'Entered frequency is not in a supported band')
            band = -1
            cabBand = -1
        #return band in the correct format
        if cabrillo:
            return cabBand
        else:
            return band

    def vhfTest(self):
        #Open the adif file
        self.logFile = open(self.logNameEnt.get(),'r')
        if self.cabNameEnt.get()=='':
            filetypes = (('Cabrillo Files','*.cbr'),('All Files','*.*'))
            fname = fd.asksaveasfilename(initialdir=self.defaultPath,\
                filetypes=filetypes,title='Cabrillo File Name')
            self.cabNameEnt.delete(0,'end')
            self.cabNameEnt.insert(0,fname)
            self.fCab = open(fname,'w')
        else:
            self.fCab = open(self.adifNameEnt.get(),'w')

        #Write Cabrillo Header
        self.writeCabrilloHeader(self.config['VHFCABRILLO']['contest'],\
            self.config['VHFCABRILLO']['assisted'],\
            self.config['VHFCABRILLO']['station'])

        #Write QSOs to file
        reader = csv.reader(self.logFile)
        for row in reader:
            self.writeVHFCabrillo(row)

        #Write the last line.
        self.fCab.write("END-OF-LOG: \n")
        self.fCab.close()

    def writeVHFCabrillo(self,row):
        #convert stuff to cabrillo format
        #band
        band = self.freqToBand(row[3],True)
        #check the band is valid for VHF
        if not (band in self.vhfBands):
            print("Ignoring HF Contact")
            return
        #mode
        if row[11]=="SSB":
            mode = 'PH'
        elif row[11]=="CW":
            mode='CW'
        elif row[11]=="FM":
            mode='FM'
        elif row[11]=="DIGI":
            mode='DG'
        else:
            #Invalid mode, somehow
            mode=='-1'
        #date
        try:
            dateObj = parser.parse(row[0])
            date = dateObj.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date!")


        #write data to file
        self.fCab.write("QSO: "+band+" "+mode+" "+date+" "+row[1])
        self.fCab.write(" "+self.callsign)
        self.fCab.write(" "+self.config['STATION']['grid']+" "+row[2])
        self.fCab.write(" "+row[9]+" \n")

    def writeCabrilloHeader(self,contest,assisted,station):
        self.fCab.write("START-OF-LOG: 3.0\n")
        self.fCab.write("CALLSIGN: "+self.callsign+"\n")
        self.fCab.write("CONTEST: "+contest+"\n")
        self.fCab.write("CATEGORY-ASSISTED: "+assisted+"\n")
        self.fCab.write("CATEGORY-BAND: ALL\n")
        self.fCab.write("CATEGORY-MODE: MIXED\n")
        self.fCab.write("CATEGORY-OPERATOR: SINGLE-OP\n")
        self.fCab.write("CATEGORY-POWER: QRP\n")
        self.fCab.write("CATEGORY-STATION: "+station+"\n")
        self.fCab.write("CATEGORY-TRANSMITTER: ONE\n")
        self.fCab.write("CLUB: "+self.config['CABRILLO']['club']+"\n")
        self.fCab.write("CREATED-BY: AA6XA-LOGGER v"+version+"\n")
        self.fCab.write("GRID-LOCATOR: "+self.config['STATION']['grid']+"\n")
        self.fCab.write("LOCATION: "+self.config['CABRILLO']['section']+"\n")
        self.fCab.write("CLAIMED-SCORE: \n")
        self.fCab.write("NAME: "+self.config['STATION']['name']+"\n")
        self.fCab.write("EMAIL: "+self.config['CABRILLO']['email']+"\n")
        self.fCab.write("OPERATORS: "+self.callsign+"\n")
        self.fCab.write("SOAPBOX:  \n")
        self.fCab.write("\n")

    def naqp(self):
        #Open the adif file
        self.logFile = open(self.logNameEnt.get(),'r')
        if self.cabNameEnt.get()=='':
            filetypes = (('Cabrillo Files','*.cbr'),('All Files','*.*'))
            fname = fd.asksaveasfilename(initialdir=self.defaultPath,\
                filetypes=filetypes,title='Cabrillo File Name')
            self.cabNameEnt.delete(0,'end')
            self.cabNameEnt.insert(0,fname)
            self.fCab = open(fname,'w')
        else:
            self.fCab = open(self.adifNameEnt.get(),'w')

        #Write Cabrillo Header
        self.writeCabrilloHeader(self.config['NAQPCABRILLO']['contest'],\
            self.config['NAQPCABRILLO']['assisted'],\
            self.config['NAQPCABRILLO']['station'])
        #This contest needs offtimes, have to manually add them
        self.fCab.write("OFFTIME: \n")

        #Write QSOs to file
        reader = csv.reader(self.logFile)
        for row in reader:
            self.writeNAQPCabrillo(row)

        #Write the last line.
        self.fCab.write("END-OF-LOG: \n")
        self.fCab.close()

    def writeNAQPCabrillo(self, row):
        #convert stuff to cabrillo format
        #band
        band = self.freqToBand(row[3],True)
        if not (band in self.hfBands):
            print("Ignoring VHF Contact")
            return
        #mode
        if row[11]=="SSB":
            mode = 'PH'
        elif row[11]=="CW":
            mode='CW'
        elif row[11]=="DIGI":
            mode='DG'
        else:
            #Invalid mode, somehow
            mode=='-1'
        #date
        try:
            dateObj = parser.parse(row[0])
            date = dateObj.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date!")

        #write data to file
        self.fCab.write("QSO: "+band+" "+mode+" "+date+" "+row[1])
        self.fCab.write(" "+self.callsign+" "+self.config['STATION']['name'])
        self.fCab.write(" "+self.config['NAQPCABRILLO']['state']+" "+row[2])
        self.fCab.write(" "+row[6]+" "+row[8]+" \n")

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

    def checkTime(self):
        if not self.timeEnt.get():
            return
        #Must be a valid time to continue
        if not re.match(r"^([01][0-9]|2[0-3])([0-5]\d)$",self.timeEnt.get()):
            print("Invalid Time!")
            self.logFlag = False
            #self.timeEnt.focus_set()

    def callToCaps(self):
        call = self.callEnt.get()
        self.callEnt.delete(0,'end')
        self.callEnt.insert(0,call.upper())
        #Callsign required, don't let them move on until its entered
        if not call:
            self.callEnt.focus_set()

    def rstSCheck(self):
        if not self.rstSentEnt.get():
            return
        if not re.match(r"^\d{2,3}$", self.rstSentEnt.get()):
            print("Invalid RST!")
            #self.logFlag = False
            self.rstSentEnt.focus_set()

    def rstRCheck(self):
        if not self.rstRxEnt.get():
            return
        if not re.match(r"^\d{2,3}$", self.rstRxEnt.get()):
            print("Invalid RST!")
            #self.logFlag = False
            self.rstRxEnt.focus_set()

    def stateToCaps(self):
        st = self.stateEnt.get()
        if not st:
            return
        #check its a valid state
        if (re.match(r"^[a-zA-Z]{2}$",st)):
            self.stateEnt.delete(0,'end')
            self.stateEnt.insert(0,st.upper())
        else:
            print("Invalid State!")
            #self.logFlag = False
            self.stateEnt.focus_set()

    def gridToCaps(self):
        grid = self.gridEnt.get()
        if not grid:
            return
        #validate 4 or 6 character grid
        if re.match(r"^[a-zA-Z]{2}\d{2}([a-zA-Z]{2})?$",grid):
            self.gridEnt.delete(0,'end')
            self.gridEnt.insert(0,grid.upper())
        else:
            print("Invalid Grid!")
            #self.logFlag = False
            self.gridEnt.focus_set()

    def sotaToCaps(self):
        sota = self.sotaEnt.get()
        if not sota:
            return
        #validate summit
        if re.match(r"^[a-zA-Z0-9]{1,3}/[a-zA-Z]{2}-\d{3}$",sota):
            self.sotaEnt.delete(0,'end')
            self.sotaEnt.insert(0,sota.upper())
        else:
            print("Invalid SOTA Peak!")
            #self.logFlag = False
            self.sotaEnt.focus_set()

    def s2sToCaps(self):
        s2s = self.s2sEnt.get()
        if not s2s:
            return
        #validate
        if re.match(r"^[a-zA-Z0-9]{1,3}/[a-zA-Z]{2}-\d{3}$",s2s):
            self.s2sEnt.delete(0,'end')
            self.s2sEnt.insert(0,s2s.upper())
            #self.logFlag = True
        else:
            print("Invalid S2S Peak!")
            #self.logFlag = False
            self.s2sEnt.focus_set()

    def wwffToCaps(self):
        grid = self.wwffEnt.get()
        if not grid:
            return
        #validate
        if re.match(r"^[a-zA-Z0-9]{1,2}(FF|ff)-\d{4}$",grid):
            self.wwffEnt.delete(0,'end')
            self.wwffEnt.insert(0,grid.upper())
            #self.logFlag = True
        else:
            print("Invalid WWFF Reference!")
            #self.logFlag = False
            self.wwffEnt.focus_set()


root=Tk()
app=Window(root)
version = "0.40"
root.wm_title("AA6XA Logger, v"+version)
root.geometry("750x300")
root.mainloop()
