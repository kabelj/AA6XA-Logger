# AA6XA-Logger
My Portable-OTA logger.


This logger is designed to be an easy to use logger to enter in handwritten 
logs after various portable on-the-air activations, e.g. SOTA, WWFF, POTA, 
or contests from summits or parks. 
It is written in Python, so it should be easy to use on any computer that has 
Python installed. It can export a CSV file formatted for the SOTA database, 
ADIF Files for upload it for WWFF/POTA, or to ClubLog or other general 
purpose logger, and Cabrillo files for a few supported contests. If you're 
looking for a full featured logger that will keep track of your DX and 
control your transceiver, look elsewhere; this is a simple one.

## Download and Installation
You will need Python 3 installed.
You also need some Python packages:
- Tk
- dateutil
- datetime
- csv
- configparser
- re (regular expressions)
- glob

On my Raspberry Pi, all of those were installed already. On my Ubuntu laptop, 
I had to install Tk and dateutil. A quick search will show you how to check 
if you have these packages, or how to install them if you don't know how to.

Linux:
cd to the directory you want to put the program in, then type
`git clone https://github.com/kabelj/AA6XA-Logger.git`
This will download all the necessary files to the directory. It can then be 
run with the command `python3 logger.py`. If you have set the `python` 
command to use Python 3, then just use that instead.

Mac:
If you have git installed, you can follow the instructions above. If not, 
click the green "download code" button and download the Zip file. Unzip this 
in the location you want to save it. Open a terminal window, cd to that 
directory, and run the command `python3 logger.py`

Windows:
Follow the Linux instructions if you have Git installed. Otherwise follow 
the Mac instructions. I don't have a Windows computer, so I can't test that 
everything works there, or even if these steps are accurate. Your system may
have a different method of calling python.



## Usage
In the directory with the code there is a file, "loggersettings" which 
contains settings you should only have to set once, or very infrequently. 
Open this and edit with your information.

It is very important you set your callsign, at the very least. Otherwise, I'll
get credit for your activation :D


On opening the logger, it will prompt you to select a log file. Select an 
existing log file. If you wish to create a new file, click "cancel" and 
another dialog will appear to allow you to create a new log. Enter in the 
log data, clicking Enter or "Save QSO" after each one. Selecting 
Export>SOTA CSV or Export>WWFF ADIF will prompt you to choose the name of the 
file, then write the QSOs in the appropriate format. 
Exporting one of the contests will behave similarly.

Currently, you need to give it a new log file name for each activation. It is
not smart, and will write all the QSOs in a log to the CSV, ADIF, or Cabrillo 
file. 
Only a few fields (callsign, name, QTH, power) don't have some sort of input 
validation. Anything you add to these fields will be accepted and written to 
log without any complaints or warnings. Also note that the SOTA checking is 
set up to accept summits from anywhere in the world, but it doesn't have a 
list of valid associations and regions. Anything that could be correct won't 
be caught by the checker, e.g. W6W/AA-123 would not be caught. Similarly for WWFF/POTA. Be careful! 
If you do make a mistake, just open the .log file with your favorite text 
editor and fix your typo.

Remember:
- New log file for each activation
- Data validation, but still be careful
- No editing QSOs in the program. Use a text editor to fix
- The first time you use the logger, edit the loggersettings to your 
information

### Exports
For the SOTA CSV export, the following fields are used:
- Date
- Time
- Callsign
- Frequency
- Mode
- My SOTA Peak
- S2S Peak

For the Parks export, which is just an ADIF files, all of the fields are 
written to the file. "Date" is used for both the <qso_date> and 
<qso_date_off> fields. "Time" is used for both <time_on> and <time_off>. The 
frequency is written to the appropriate field, and the program automatically 
determines the band from it. "Park Ref" is written to <my_sig_info>. The 
<operator> field is taken from the settings file.


## Features not yet added
There are plenty of improvements to add:
- Show the last few QSOs in a nice format
- Visual improvements to gui (though I think it looks ok now)
- Export cabrillo for other contests, if desired
- Re-order QSOs to chronological for SOTA export

And some things that would be nice to have, but I may never implement, since 
I'm not really a great programmer:
- Remember name/qth/state of people you've contacted before. This would make 
it closer to a general purpose logger, and there are better ones out there, 
so don't hold your breath for this type of feature. Also, I'd need to learn 
how to do databases.
- Export only certain QSOs for a given export
- Other fields people may want

### Bugs
If you use this and find a bug, let me know, and I'll add it to the list. I 
might even fix it for you!

Known Bugs:
- QSOs are written to the SOTA CSV in the order they're in the log. The SOTA 
database expects them to be in chronological order. If they're not, you'll 
need to manually cut/paste lines in a text editor to fix this.
- Only bands that I use (or will soon!) are currently supported. This shouldn't 
matter unless you're really into microwaves. (All HF/VHF/UHF are supported)
- I haven't looked to closely at how Python's datetime works, so be careful 
with dates where the month and day can be interchanged, e.g. 3/4/2021. I 
added a note to the GUI to remind you the best format.
- I'm pretty sure I did all the input validation regex's right, so please 
let me know if you find a bug in one!


## History
When my Macbook, the main computer in my shack, started to die, I replaced it 
with a Raspberry pi. This meant switching to Linux. Overall this was a good 
experience; however I was not able to find a general purpose logger that I 
liked. Luckily, there is no law against making my own. In fact, I'd argue it's 
in the spirit of ham radio to make your own. I wanted a logger that 
supported SOTA, WWFF, and other portable operation very well. It also needed
to support the contests that I like to do from summits. I am less 
interested in chasing DX awards and stuff like that. This is the result. I 
hope you enjoy it and find it useful. 
