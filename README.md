# AA6XA-Logger
My Portable OTA logger.


This logger is designed to be an easy to use logger to enter in handwritten 
logs after various on-the-air activations, e.g. SOTA, WWFF. It is written 
in Python, so it should be easy to use on any computer that has Python 
installed. It will export a CSV file formatted for the SOTA database, both 
activator, chaser, and S2S contacts. It also will export an ADIF 3.1.0 file 
so you can upload it for WWFF/POTA or to ClubLog or other general purpose 
logger. It also (soon!) will export a cabrillo file for the ARRRL VHF 
contest.
Currently, you need to give it a new log file name for each activation. It is
not smart, and will write all the QSOs in a log to the CSV or ADIF file. If 
you close a log, entering the same .log file will continue adding to the end,
or allow you to export it in a different format.



There are a number of major improvements needed before I advertise this 
logger to the public:
> Add settings window or file
> Ask for .log file upon opening
> Show the last few QSOs entered

There are some less important things to take care of too:
> Export cabrillo for VHF Contests
> Visual improvements to gui
> Ask for export file name in prompt
> Any other export settings in a prompt
> Change default log location in settings
> Export cabrillo for other contests

And some things that would be nice to have, but I may never implement, since 
I'm not really a great programmer:
> Remember name/qth/state of people you've contacted before
> Export only certain QSOs for a given export
> Other general improvements
> Other fields people may want



History
When my Macbook, the main computer in my shack, started to die, I replaced it
with a raspberry pi. This meant switching to Linux. Overall this was a good 
experience, however I was not able to find a general purpose logger that I 
liked. Luckily, there is no law against making my own. I wanted a logger that
supported SOTA, WWFF, and other portable operation very well. I am less 
interested in chasing DX awards and stuff like that. This is the result. I
hope you enjoy it and find it useful.
