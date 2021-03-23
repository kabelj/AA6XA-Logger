# AA6XA-Logger
My Portable-OTA logger.


This logger is designed to be an easy to use logger to enter in handwritten 
logs after various on-the-air activations, e.g. SOTA, WWFF. It is written 
in Python, so it should be easy to use on any computer that has Python 
installed. It will export a CSV file formatted for the SOTA database, both 
activator, chaser, and S2S contacts. It also will export an ADIF 3.1.0 file 
so you can upload it for WWFF/POTA or to ClubLog or other general purpose 
logger. It also (soon!) will export a cabrillo file for the ARRRL VHF 
contest, and possibly others. If you're looking for a full featured logger 
that will keep track of your DX and control your transceiver, look elsewhere.
This is a simple one.

Download and Installation
You will need Python 3 installed.

If you know how to get files from GitHub, use your regular procedure.

Linux:
cd to the directory you want to put the program in, then type
"git clone https://github.com/kabelj/AA6XA-Logger.git"
This will download all the necessary files to the directory. It can then be 
run with the command "python logger.py"

Mac:
If you have git installed, you can follow the instructions above. If not, 
click the green "download code" button and download the Zip file. Unzip this 
in the location you want to save it. Open a terminal window, cd to that 
directory, and run the command "python logger.py"

Windows:
Follow the Linux instructions if you have Git installed. Otherwise follow 
the Mac instructions. I don't have a Windows computer, so I can't test that 
everything works there.



Usage
In the directory with the code there is a file "loggersettings" which 
contains settings you should only have to set once, or very infrequently. 
Open this and edit with your information.
On opening the logger, it will prompt you to select a log file. This is 
either a new or existing one. Enter in the log data, clicking save QSO after
each one. Selecting Export>"SOTA CSV" or Export>"WWFF ADIF" will prompt you 
to choose the name of the file, then write the QSOs in the appropriate format.
Currently, you need to give it a new log file name for each activation. It is
not smart, and will write all the QSOs in a log to the CSV or ADIF file. 
There is currently not any data validation, e.g. entering "09gu,hi," for in
the Date field will be accepted and written to log without any complaints or
warnings. Be careful! If you do make a mistake, just open the .log file with 
your favorite text editor and fix your typo.



There are plenty of improvements to add:
> Show the last few QSOs entered
> Show those QSOs in a nice format
> Export cabrillo for VHF Contests
> Input checking (valid date, time, etc)
> Visual improvements to gui
> Any other export settings in a prompt
> Change default log location in settings
> Export cabrillo for other contests

And some things that would be nice to have, but I may never implement, since 
I'm not really a great programmer:
> Remember name/qth/state of people you've contacted before. This would make 
it closer to a general purpose logger, and there are better ones out there, 
so don't hold your breath for this type of feature.
> Export only certain QSOs for a given export
> Other fields people may want




History
When my Macbook, the main computer in my shack, started to die, I replaced it
with a raspberry pi. This meant switching to Linux. Overall this was a good 
experience, however I was not able to find a general purpose logger that I 
liked. Luckily, there is no law against making my own. I wanted a logger that
supported SOTA, WWFF, and other portable operation very well. I am less 
interested in chasing DX awards and stuff like that. This is the result. I
hope you enjoy it and find it useful.
