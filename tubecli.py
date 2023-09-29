apikey = "d53e2401ad8c423396f762a57e1bc9ad"

######################
### INITIALISATION ###
######################

# libraries
import argparse
import requests
import textwrap
import json

# arguments
argparser = argparse.ArgumentParser(description="tubecli", add_help=False)
cmdparser = argparser.add_subparsers(dest="command")

infoparse = cmdparser.add_parser('help')
creditparse = cmdparser.add_parser('credits')
statusparse = cmdparser.add_parser('status')
apikeyparse = cmdparser.add_parser('apikey')

apikeyparse.add_argument('key',type=str,nargs="?")
statusparse.add_argument('line',type=str,nargs="?")

args=argparser.parse_args()

# line colour and name
lines = {
        "bakerloo": ["\033[48;5;94m\033[38;5;231m","Bakerloo"],
        "central": ["\033[48;5;160m\033[38;5;231m","Central"],
        "circle": ["\033[48;5;220m\033[38;5;19m","Circle"],
        "district": ["\033[48;5;28m\033[38;5;231m","District"],
        "hammersmith-city": ["\033[48;5;218m\033[38;5;19m","H'smith & City"],
        "jubilee": ["\033[48;5;246m\033[38;5;231m","Jubilee"],
        "metropolitan": ["\033[48;5;90m\033[38;5;231m","Metropolitan"],
        "northern": ["\033[48;5;232m\033[38;5;231m","Northern"],
        "piccadilly": ["\033[48;5;19m\033[38;5;231m","Piccadilly"],
        "victoria": ["\033[48;5;39m\033[38;5;19m","Victoria"],
        "waterloo-city": ["\033[48;5;86m\033[38;5;19m","Waterloo & City"],
        "dlr": ["\033[48;5;44m\033[38;5;19m","DLR"],
        "elizabeth": ["\033[48;5;93m\033[38;5;231m","Elizabeth Line"],
        "london-overground": ["\033[48;5;208m\033[38;5;19m","Overground"],
        "tram": ["\033[48;5;76m\033[38;5;19m","Trams"],
}



############
### INFO ###
############
match args.command:
    case "help":
        print("""\033[1mtubecli info\033[0m

Line IDs:
bakerloo - Bakerloo line
central - Central line
circle - Circle line
district - District line
hammersmith-city - Hammersmith & City line
jubilee - Jubilee line
metropolitan - Metropolitan line
northern - Northern line
piccadilly - Piccadilly line
victoria - Victoria line
waterloo-city - Waterloo & City line
dlr - DLR
elizabeth - Elizabeth line
london-overground - Overground
tram - London Trams

help
Shows this help message and exit.

credits
Shows credits, copyrights, and licencing information.

status [line]
Without arguments, provides a basic overview of all line statuses.
Type status [line] specifies the line for further info
e.g. status piccadilly would output detailed status of the
Piccadilly line.

station <id>
Provides detailed info about a station.
<id> refers to the name of a station e.g. station Waterloo
note: To save myself from implementing hundreds stations, the stations
are taken right from TfL's database.""")


###############
### CREDITS ###
###############

    case "credits":
        print("""Developed by daysant 🄯 2023
Powered by TfL Open Data
Contains OS data © Crown copyright and database rights 2016
Geomni UK Map data © and database rights [2019]

Licenced under the GNU GPL v3.0-or-later
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
IMPLIED OR EXPLICIT.""")



#############
### LINES ###
#############
    case "status":
        if args.line == None:
            prog=0 # progressbar
            
            # initialise lists
            lkeys = list(lines.keys())
            lstatus = []
            
            # request and parse info from tfl
            for i in range(len(lkeys)):

                # progress bar
                print(f"[{'#'*prog}{' '*(30-prog)}] {round((prog/30)*100)}%\033[0G",end="",flush=True)

                data = requests.get(f"https://api.tfl.gov.uk/Line/{lkeys[i]}/Disruption?app_key={apikey}")
                if data.status_code==200:
                    data=data.json()
                    if not data:
                        severity = "Good service"
                    else:
                        if data:
                            severity = data[0].get("closureText","Severity unavaliable")
                        else:
                            severity = "Unknown"

                        match severity: # severities
                            case "minorDelays":
                                severity="Minor delays"
                            case "severeDelays":
                                severity="Severe delays"
                            case _:
                                severity="Unknown"

                    lstatus.append(severity)
                    prog+=2

                else:
                    lstatus.append(f"Unavailable ({data.status_code})")

                # format and print
            for i in range(len(lkeys)):
                pad = 36-len(lines[lkeys[i]][1])-len(lstatus[i])
                print(f"{lines[lkeys[i]][0]} {lines[lkeys[i]][1]} {' ' * pad} {lstatus[i]} \033[0m")

        else: # specific line requested

            # request and parse data from tfl
            data = requests.get(f"https://api.tfl.gov.uk/Line/{args.line}/Disruption?app_key={apikey}")
            if data.status_code==200:
                data = data.json()
                
                if not data:
                    severity="Good service"
                    info="Good service on the line"
                    
                else:
                    severity=data[0].get("closureText","Severity unavaliable")
                    info=data[0].get("description","Description unavaliable")

                    match severity: # severities
                        case "minorDelays":
                            severity="Minor delays"
                        case "severeDelays":
                            severity="Severe delays"
                        case _:
                            severity="Unknown"

                # format data
                pad = 36-len(lines[args.line][1])-len(severity)
                print(f"{lines[args.line][0]} {lines[args.line][1]} {' ' * pad} {severity} \033[0m")
                print('\n'.join(textwrap.wrap(info, 40)))


            else: # http errors
                print(f"""tubecli: HTTP {data.status_code}""")


####################
### EDIT API KEY ###
####################
    case "apikey":
        if not args.key: # detect a blank
            print("tubecli: Enter an API key after typing apikey")
        else:
            print(f"{args.key}")
