import re

# All the input checking goes in this file

def checkTime(inputTime):
    if not inputTime:
        return
    #Must be a valid time to continue
    if not re.match(r"^([01][0-9]|2[0-3])([0-5]\d)$",inputTime):
        print("Invalid Time!")
        return False

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