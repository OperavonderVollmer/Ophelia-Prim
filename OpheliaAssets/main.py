#import opheliaWake as opheWake
#import opheliaBridge as opheBri


#--------------------------------------------------------#
#opheWake.opheliaBegin(not opheNeu.debugMode)
#opheWake.opheliaBegin(onStartBool=True)
#opheWake.opheliaBegin(onStartBool=False)
#opheWake.opheliaBegin(onStartBool=False, quickstart=True)

#--------------------------------------------------------#

# opheWake.startDiscord()

#--------------------------------------------------------#

from opheliaPlugins import plugins
from datetime import datetime   

now = datetime.now()
routine = {
    "one": {
        "name": "Go on a walk",
        "timeStart": None,
        "timeEnd": now.replace(hour=10, minute=0, second=0, microsecond=0),
    },
    "two": {
        "name": "Wake up early",
        "timeStart": None,
        "timeEnd": now.replace(hour=7, minute=0, second=0, microsecond=0),
    },
    "three": {
        "name": "Clean up dog poop",
        "timeStart": None,
        "timeEnd": now.replace(hour=10, minute=0, second=0, microsecond=0),
    },
    "four": {
        "name": "Clean up dog poop",
        "timeStart": now.replace(hour=17, minute=0, second=0, microsecond=0),
        "timeEnd": now.replace(hour=23, minute=0, second=0, microsecond=0),
    },
    "five": {
        "name": "Stretches",
        "timeStart": None,
        "timeEnd": now.replace(hour=10, minute=0, second=0, microsecond=0),
    },
    "six": {
        "name": "Stretches",
        "timeStart": now.replace(hour=17, minute=0, second=0, microsecond=0),
        "timeEnd": now.replace(hour=23, minute=0, second=0, microsecond=0),
    },
    "seven": {
        "name": "Brush teeth",
        "timeStart": None,
        "timeEnd": now.replace(hour=10, minute=0, second=0, microsecond=0),
    },
    "eight": {
        "name": "Brush teeth",
        "timeStart": now.replace(hour=12, minute=0, second=0, microsecond=0),
        "timeEnd": now.replace(hour=15, minute=0, second=0, microsecond=0),
    },
    "nine": {
        "name": "Brush teeth",
        "timeStart": now.replace(hour=17, minute=0, second=0, microsecond=0),
        "timeEnd": now.replace(hour=23, minute=59, second=0, microsecond=0),
    },
    "ten": {
        "name": "Clock in",
        "timeStart": None,
        "timeEnd": now.replace(hour=15, minute=0, second=0, microsecond=0),
    },
    "eleven": {
        "name": "Clock out",
        "timeStart": now.replace(hour=17, minute=0, second=0, microsecond=0),
        "timeEnd": None,
    },
    "twelve": {
        "name": "Interact with friends",
        "timeStart": None,
        "timeEnd": None,
    },
    "thirteen": {
        "name": "Tidy up",
        "timeStart": None,
        "timeEnd": None,
    },
    "fourteen": {
        "name": "Drink a full glass of water",
        "timeStart": None,
        "timeEnd": None,
    },
    "fifteen": {
        "name": "Drink a full glass of water",
        "timeStart": None,
        "timeEnd": None,
    },
    "sixteen": {
        "name": "Duolinggo",
        "timeStart": None,
        "timeEnd": None,
    },
    "seventeen": {
        "name": "Shower",
        "timeStart": None,
        "timeEnd": None,    
    },
    "eighteen": {
        "name": "Star Rail Daily",
        "timeStart": None,
        "timeEnd": None,    
    },
    "nineteen": {
        "name": "Blue Archive Daily",
        "timeStart": None,
        "timeEnd": None,    
    },
    "twenty": {
        "name": "Hunting",
        "timeStart": None,
        "timeEnd": None,
    },
    "twentyone": {
        "name": "Push code",
        "timeStart": None,
        "timeEnd": None,
    },
    "twentytwo": {
        "name": "Daily Review",
        "timeStart": now.replace(hour=17, minute=0, second=0, microsecond=0),
        "timeEnd": now.replace(hour=23, minute=59, second=0, microsecond=0),
    },

}

plugins["Ticket"].startQuestManager()


#For testing purposes only
"""for r in routine.values():
    plugins["Ticket"].qm.addToPersistent(questName = r["name"], timeStart = r["timeStart"], timeEnd = r["timeEnd"])"""

print(plugins["Ticket"].cheatResult(command="refresh"))

"""while True:
    decision = input("Finish, List, New, Add, Remove, Progress?: ").lower()
    print(plugins["Ticket"].cheatResult(command=decision))"""