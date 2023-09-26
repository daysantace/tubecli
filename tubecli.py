apikey = "d53e2401ad8c423396f762a57e1bc9ad" # insert your own API key here

######################
### INITIALISATION ###
######################

# libraries
import argparse
import requests

# arguments
argparser = argparse.ArgumentParser(description="tubecli", add_help=False)
cmdparser = argparser.add_subparsers(dest="command")

infoparse = cmdparser.add_parser('help')
creditparse = cmdparser.add_parser('credits')

statusparse = cmdparser.add_parser('status')
statusparse.add_argument('line',type=str,nargs="?")

args=argparser.parse_args()

# line colour and name
lines = {
        "bakerloo": ["\033[48;5;94m\033[38;5;231m","Bakerloo"],
        "central": ["\033[48;5;160m\033[38;5;231m","Central"],
        "circle": ["\033[48;5;220m\033[38;5;232m","Circle"],
        "district": ["\033[48;5;28m\033[38;5;231m","District"],
        "hammersmith-city": ["\033[48;5;218m\033[38;5;232m","Hammersmith & City"],
        "jubilee": ["\033[48;5;246m\033[38;5;231m","Jubilee"],
        "metropolitan": ["\033[48;5;90m\033[38;5;231m","Metropolitan"],
        "northern": ["\033[48;5;232m\033[38;5;231m","Northern"],
        "piccadilly": ["\033[48;5;27m\033[38;5;231m","Picadilly"],
        "victoria": ["\033[48;5;39m\033[38;5;232m","Victoria"],
        "waterloo-city": ["\033[48;5;86m\033[38;5;232m","Waterloo & City"],
        "dlr": ["\033[48;5;44m\033[38;5;232m","DLR"],
        "elizabeth": ["\033[48;5;93m\033[38;5;231m","Elizabeth Line"],
        "overground": ["\033[48;5;208m\033[38;5;232m","Overground"],
        "tram": ["\033[48;5;76m\033[38;5;232m","Trams"],
        "cable-car": ["\033[48;5;160m\033[38;5;231m","IFS Cloud cable car"]
}



############
### INFO ###
############
if args.command == "help" or args.command == None:
    print("""\033[1mtubecli info\033[0m

Line IDs:
bakerloo - Bakerloo Line
central - Central line
circle - Circle line
district - District lineapikey}
hammersmith-city - Hammersmith & City line
jubilee - Jubilee line
metropolitan - Metropolitan line
northern - Northern line
piccadilly - Piccadilly line
victoria - Victoria line
waterloo-city - Waterloo & City line
dlr - DLR
elizabeth - Elizabeth line
overground - London Overground
tram - London Trams
cable-car - IFS Cloud cable car

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
<id> refers to the name of a station
e.g. station Waterloo gets info about the aformentioned station.
note: To save myself from implementing 500+ stations, the stations
are taken right from TfL's database.""")


###############
### CREDITS ###
###############

elif args.command == "credits":
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
elif args.command == "status":
    if args.line == None:
        lkeys = list(lines.keys())
        lstatus = []

        print("Line overview\n")
        for i in range(len(lkeys)):
            status = requests.get(f"https://api.tfl.gov.uk/Line/{lkeys[i]}/Disruption?app_key={apikey}")
            print(f"{lkeys[i]}: {status}")
            print(str(status.json()))
    else:
        print(f"{args.line}")



###################
### INVALID CMD ###
###################
else:
    print(f"""Error: {args.command} is not a valid command.
Type a valid command, or type 'help' for a list of valid commands.""")
