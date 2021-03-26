# AA6XA-Logger
My Portable-OTA logger.


This logger is designed to be an easy to use logger to enter in handwritten 
logs after various portable on-the-air activations, e.g. SOTA, WWFF, contests 
from summits or parks. 
It is written in Python, so it should be easy to use on any computer that has 
Python installed. It can export a CSV file formatted for the SOTA database, 
ADIF Files for upload it for WWFF/POTA, or to ClubLog or other general 
purpose logger, and Cabrillo files for a few supported contests. If you're 
looking for a full featured logger that will keep track of your DX and 
control your transceiver, look elsewhere. This is a simple one.

## Download and Installation
You will need Python 3 installed.

If you know how to get files from GitHub, use your regular procedure.

Linux:
cd to the directory you want to put the program in, then type
`git clone https://github.com/kabelj/AA6XA-Logger.git`
This will download all the necessary files to the directory. It can then be 
run with the command `python logger.py`

Mac:
If you have git installed, you can follow the instructions above. If not, 
click the green "download code" button and download the Zip file. Unzip this 
in the location you want to save it. Open a terminal window, cd to that 
directory, and run the command `python logger.py`

Windows:
Follow the Linux instructions if you have Git installed. Otherwise follow 
the Mac instructions. I don't have a Windows computer, so I can't test that 
everything works there, or even if these steps are accurate.



## Usage
In the directory with the code there is a file, "loggersettings", which 
contains settings you should only have to set once, or very infrequently. 
Open this and edit with your information.

On opening the logger, it will prompt you to select a log file. This is 
either a new or existing one. Enter in the log data, clicking <enter> or 
"Save QSO" after each one. Selecting Export>"SOTA CSV" or Export>"WWFF ADIF" 
will prompt you to choose the name of the file, then write the QSOs in the 
appropriate format. Exporting one of the contests will behave similarly.
Currently, you need to give it a new log file name for each activation. It is
not smart, and will write all the QSOs in a log to the CSV, ADIF, or Cabrillo 
file. Currently, only a few fields have data validation. Anything you add to 
fields that aren't checked will be accepted and written to log without any 
complaints or warnings. Be careful! If you do make a mistake, just open the 
.log file with your favorite text editor and fix your typo.

Remember:
- New log file for each activation
- Limited data validation (currently)
- No editing QSOs in the program. Use a text editor to fix

## Features not yet added
There are plenty of improvements to add:
- Show the last few QSOs entered
- Show those QSOs in a nice format
- Export cabrillo for NAQP
- Input checking (valid time, grid, RST, SOTA/WWFF refs, etc)
- Visual improvements to gui
- Export cabrillo for other contests, if desired

And some things that would be nice to have, but I may never implement, since 
I'm not really a great programmer:
- Remember name/qth/state of people you've contacted before. This would make 
it closer to a general purpose logger, and there are better ones out there, 
so don't hold your breath for this type of feature.
- Export only certain QSOs for a given export
- Other fields people may want

### Bugs
If you use this and find a bug, let me know. I'll add it to the list, and I 
might even fix it!

Known Bugs:
- QSOs are written to the SOTA CSV in the order they're in the log. The SOTA 
database expects them to be in chronological order. If they're not, you'll 
need to manually cut/paste lines in a text editor to fix this.
- When starting the program, you can't create a new log. Select an 
existing one, then File>New Log.
- Only bands that I use are currently supported. This shouldn't matter 
unless you're really into microwaves. (All HF/VHF/UHF are supported)
- I haven't looked to closely at how Python's datetime works, so be careful 
with dates where the month and day can be interchanged, e.g. 3/4/2021
- VHF Cabrillo Export will allow you to export QSOs on non-contest bands


## History
When my Macbook, the main computer in my shack, started to die, I replaced it 
with a raspberry pi. This meant switching to Linux. Overall this was a good 
experience; however I was not able to find a general purpose logger that I 
liked. Luckily, there is no law against making my own. I wanted a logger that 
supported SOTA, WWFF, and other portable operation very well. I am less 
interested in chasing DX awards and stuff like that. This is the result. I 
hope you enjoy it and find it useful. 
