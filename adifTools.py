from datetime import datetime

# Tools for writing ADIF files

def writeAdifRow(fAdif, row, callsign):
    band = freqToBand(row[3],False)
    date_obj = datetime.strptime(row[0],"%d/%m/%Y")
    date = date_obj.strftime("%Y%m%d")

    fAdif.write("<operator:"+str(len(callsign))+">"+callsign)
    fAdif.write("<call:"+str(len(row[2]))+">"+row[2])
    fAdif.write("<qso_date:8>"+date)
    fAdif.write("<qso_date_off:8>"+date)
    fAdif.write("<time_on:4>"+row[1])
    fAdif.write("<time_off:4>"+row[1])
    fAdif.write("<freq:"+str(len(row[3]))+">"+row[3])
    fAdif.write("<band:"+str(len(band))+">"+band)
    fAdif.write("<mode:"+str(len(row[11]))+">"+row[11])
    fAdif.write("<rst_sent:"+str(len(row[4]))+">"+row[4])
    fAdif.write("<rst_rcvd:"+str(len(row[5]))+">"+row[5])
    fAdif.write("<name:"+str(len(row[6]))+">"+row[6])
    fAdif.write("<state:"+str(len(row[8]))+">"+row[8])
    fAdif.write("<qth:"+str(len(row[7]))+">"+row[7])
    fAdif.write("<tx_pwr:"+str(len(row[10]))+">"+row[10])
    fAdif.write("<my_sota_ref:"+str(len(row[12]))+">"+row[12])
    fAdif.write("<sota_ref:"+str(len(row[13]))+">"+row[13])
    fAdif.write("<my_sig_info:"+str(len(row[14]))+">"+row[14])
    fAdif.write("<gridsquare:"+str(len(row[9]))+">"+row[9])
    fAdif.write("<eor>\n")

def writeAdifHeader(fAdif,version,callsign):
    now = datetime.now().strftime('%d/%m/%Y %H:%M')
    fAdif.write("Exported on "+now+' for '+callsign+' \n')
    fAdif.write("\n<ADIF_VER:5>3.1.0 \n")
    fAdif.write("<PROGRAMID:12>AA6XA logger \n")
    fAdif.write("<PROGRAMVERSION:"+str(len(version))+">"\
        +version+" \n<EOH>\n\n")

def freqToBand(freq, cabrillo):
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
