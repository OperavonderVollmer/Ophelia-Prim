from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
from abc import ABC, abstractmethod
from datetime import datetime
import random
import json
import os
import shutil
import time

class plugin(opheliaPlugin):
# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead    

    class questManager:
        """
            Methods include addQuestWizard (easily adds quests), addQuest (accepts generic quest objects and adds it to associated list, if giveList is True returns instead), testPopulateQuests (exclusively for testing), addToPersistent (adds quest to persistent list), removeFromPersistent (removes quest from persistent list), refreshFromPersistent (refreshes daily quest list based on persistent list), timeSens (kick starts the timer for handling time sensitive quests, returns true if started properly), listQuests (returns a dictionary of the available quest lists [main, daily, all]), finishQuest (concludes a quest and receives the reward), saveState, loadState
        """
        class quest(ABC):
            def __init__(self, questName: str, questType: str, questLevel: int, timeStart: datetime = None, timeEnd: datetime = None, questReward = None, questRewardPool: list = None):
                self.questName = questName; self.questType = questType
                self.questLevel = questLevel; self.timeStart = timeStart
                self.timeEnd = timeEnd; self.questReward = questReward
                self.questRewardPool = questRewardPool

            @property
            def QuestName(self): return self.questName
            @property
            def QuestType(self): return self.questType
            @property
            def QuestLevel(self): return self.questLevel
            @property
            def TimeStart(self): return self.timeStart
            @property
            def TimeEnd(self): return self.timeEnd
            @property
            def QuestReward(self): return self.questReward
            @property
            def QuestRewardPool(self): return self.questRewardPool

            @abstractmethod
            def updateQuestPool(self, questRewardPool): pass

            @abstractmethod
            def finishQuest(self, **kwargs):
                pass
        class dailyQuest(quest):
            """
                finishQuest will return a dictionary with dailyCount, tierIncrement and reward keys. Does not use quest levels
            """
            def __init__(self, questName: str, questType: str, questLevel: int, timeStart: datetime = None, timeEnd: datetime = None, questReward: str = "+1 to daily count (rewards at 1, 4 and 8)", questRewardPool: list = None):
                super().__init__(
                    questName,
                    questType, 
                    questLevel, 
                    timeStart, 
                    timeEnd, 
                    questReward, 
                    questRewardPool)
        
            def updateQuestPool(self, questRewardPool):
                self.questRewardPool = questRewardPool
                return True

            def finishQuest(self, **kwargs):
                """
                    Increment tier increment only at 8 daily quests completed and no further.
                    Will only provide rewards after 1st, 4th and 8th daily quest completed.
                """
                dc = kwargs["dailyCount"]
                ti = kwargs["tierIncrement"]
                dc += 1
                if dc == 1: tier = 1
                elif dc == 4: tier = 2
                elif dc == 8: tier = 3
                else: tier = 0
                if tier: self.questReward += f"and tier {tier} daily reward: {random.choice(self.questRewardPool[tier - 1])}"
                if dc == 8: ti += 1
                return {"dailyCount": dc, "tierIncrement": ti, "reward": self.questReward}
        class mainQuest(quest):# 5
            def __init__(self, questName: str, questType: str, questLevel: int, timeStart: datetime = None,timeEnd: datetime = None, questReward: str = None, questRewardPool: list = None):
                super().__init__(
                    questName, 
                    questType, 
                    questLevel, 
                    timeStart, 
                    timeEnd, 
                    questReward = questReward if isinstance(questReward, str) else random.choice(questRewardPool[min(questLevel - 1, len(questRewardPool) - 1)]) if questRewardPool else "No reward", 
                    questRewardPool=questRewardPool)

            def updateQuestPool(self, questRewardPool):
                self.questRewardPool = questRewardPool
                self.questReward = random.choice(self.questRewardPool[min(self.questLevel - 1, len(self.questRewardPool) - 1)])
                return True

            def finishQuest(self, **kwargs):
                ti = kwargs["tierIncrement"]
                decision = input(f"The reward is `{self.questReward}`. You currently have {ti} tier increment.\nClaim[1], Upgrade[2], or Pass[3]?: ").lower()
                if decision == "2": 
                    if ti != 0: 
                        self.questReward = random.choice(self.questRewardPool[min(ti + self.questLevel -1, len(self.questRewardPool) - 1)])
                        ti = 0
                    else: print("You have no tier increment for an upgrade. Regular reward will be given.")
                elif decision == "3": 
                    ti += 1
                    self.questReward = "+1 to tier increment"
                return {"dailyCount": kwargs["dailyCount"], "tierIncrement": ti, "reward": self.questReward}
        class genericQuest:
            def __init__(self, questName: str, questType: str, questLevel: int = None, timeStart: datetime = None, timeEnd: datetime = None, questReward: str = None, questRewardPool: list = None):
                self.questName = questName
                self.questType = questType
                self.questLevel = questLevel
                self.timeStart = timeStart
                self.timeEnd = timeEnd
                self.questReward = questReward
                self.questRewardPool = questRewardPool
        def __init__(self):
            self.dailyRewardList = [ # daily quest rewards are divided into three tiers
                ["Get a cup of coffee"],
                ["Binge memes 30 minutes", "Listen to an album", "Play a game for 30 minutes", "Brain off for 30 minutes"],
                ["Watch 2-3 amount of episodes of show", "Watch a movie", "Sensual Exercise", "Game time"],
            ]
            self.mainRewardList = [ # main quest rewards are divided into 10 tiers, some scaling with level of tier
                # TODO: add rewards
                ["Level one reward"],
                ["Level two reward"],
                ["Level three reward"],
                ["Level four reward"],
                ["Level five reward"],
                ["Level six reward"],
                ["Level seven reward"],
                ["Level eight reward"],
                ["Level nine reward"],
                ["Level ten reward"],
            ]
            self.dailyCount = 0
            self.tierIncrement = 0
            self.mainQuestList = []
            self.dailyQuestList = []
            self.persistentDaily = []
            self.queuedQuests = [] 
            self.expiredQuests = []
            self.path = "CurrentTickets.json"
            self.persistentPath = "PersistentTickets.json"
            if self.loadState() and self.saveState(): print ("Tickets loaded successfully")
        def questHelper(self, prompt = None, strip: str = None):
                from functions.opheliaHears import opheliaHears
                from functions.opheliaMouth import opheliaSpeak
                number_corrections = {
                    "fi": "five", 
                    "fiv": "five",
                    "to": "two", 
                    "too": "two", 
                    "tu": "two",
                    "tree": "three", 
                    "thre": "three",
                    "sicks": "six", 
                    "sex": "six",
                    "ate": "eight", 
                    "ateen": "eighteen",
                    "eigh": "eight",
                    "won": "one",
                    "on": "one",
                }
                try:
                    while True:
                        if prompt is not None: opheliaSpeak(prompt)
                        resp = opheliaHears()
                        if resp is None: 
                            opheliaSpeak("No response received. Please try again.")
                            continue
                        else: resp = resp.lower()
                        if strip is not None: resp = resp.lower().strip(strip)
                        if resp == "no": resp = None
                        if resp in number_corrections.keys(): resp = number_corrections[resp]
                        opheliaSpeak(f"Is `{resp if resp is not None else 'None'}` correct?: ")
                        if opheliaHears(timeout=10, timed=True).lower() == "yes": 
                            return resp
                except Exception as e:
                    print(f"Error: {e}, resp: {resp}")
        def addQuestWizard(self, questName: str=None, questType: str=None, questLevel: int = None, timeStart: datetime = None, timeEnd: datetime = None, returnQuest: bool = False, *args):
            if args: 
                questName, questType, questLevel = (args + [None] * 3) [:3]
            if questName is None: 
                questName = self.questHelper("Quest Name")
                questType = self.questHelper("Quest Type. Daily or Main followed by quest", " quest").lower()
                if questType == "main": questLevel = opheNeu.normalizeNumber(self.questHelper("Quest Level. Say Level, followed by a number between 1 and 10", "level "))
                else: questLevel = None
                print(f"Quest Name: {questName} | Quest Type: {questType} | Quest Level: {questLevel if questLevel is not None else 'No level'}")
            if questLevel is not None and questType == "daily": print("Daily quests do not have a level.")
            return self.addQuest(self.genericQuest(questName.capitalize(), questType, questLevel, timeStart, timeEnd), returnQuest)
        def addQuest(self, q: genericQuest, giveList = False):
            """
                Returns quest if giveList is not None. Else, automatically appends quest to associated quest list.
                genericQuests don't have questRewardPool naturally so needs to be added here.
            """
            if not isinstance(q, self.genericQuest):
                raise TypeError(f"Expected a genericQuest object, but got {type(q).__name__}")
            if q.questType == "main": quest = self.mainQuest(q.questName, q.questType, q.questLevel, q.timeStart, q.timeEnd)
            elif q.questType == "daily": quest = self.dailyQuest(q.questName, q.questType, q.questLevel, q.timeStart, q.timeEnd)
            else: raise Exception("Invalid quest type")
            if getattr(quest, "questRewardPool", None) is None:  
                if quest.QuestType == "daily": rewardList = self.dailyRewardList
                elif quest.QuestType == "main": rewardList = self.mainRewardList
                quest.updateQuestPool(rewardList)
            if giveList: return quest
            if quest.QuestType == "daily": self.dailyQuestList.append(quest)
            elif quest.QuestType == "main": self.mainQuestList.append(quest)
            self.saveState()
            return "Quest has been succesfully added"
        def testPopulateQuests(self, max):
            for i in range(max):
                questType = random.choice(["daily", "main"])
                params = {
                    "questName": f"Quest {i+1}",
                    "questType": questType,
                    "questLevel": random.randint(1, 10),
                }
                if questType == "daily": self.addQuest(self.genericQuest(**params))
                elif questType == "main": self.addQuest(self.genericQuest(**params))
        def addToPersistent(self, questName: str = None, timeStart: datetime = None, timeEnd: datetime = None, *args):
            if args: questName = args[0]
            if questName is None: 
                questName = self.questHelper("Quest Name")
            print(f"Adding {questName.capitalize()} to persistent list")
            newDaily = self.genericQuest(questName.capitalize(), "daily", None, timeStart, timeEnd)
            self.persistentDaily.append(newDaily)
            self.saveState()
            return f"Successfully added {questName} to persistent list"
        def removeFromPersistent(self, *args):
            questName = args[0] if args else None
            if questName is None:
                questName = self.questHelper("Quest Name")
            for quest in self.persistentDaily:
                if quest.QuestName == questName:
                    self.persistentDaily.remove(quest)
                    return True
            return False
        def refreshFromPersistent(self):
            self.dailyCount = 0
            temporaryQuestList = []
            currentTime = datetime.now().time()
            for quest in self.persistentDaily:
                qStart = quest.timeStart.time() if quest.timeStart else None
                qEnd = quest.timeEnd.time() if quest.timeEnd else None
                print(f"======================================\nChecking {quest.questName}. Time Start: {qStart} | Time End: {qEnd} | Time Now: {currentTime}")
                # time start > time now 
                # only if time now is less than time start (earlier)
                if qStart:
                    if qStart > currentTime:
                        self.queuedQuests.append(self.addQuest(quest, True))
                        print("Verdict: Queued")
                        continue
                # time now 
                # only if time now is greater than time end (later)
                # if earlier than time end, appends to temporary quest list
                if qEnd:
                    if qStart:
                        if currentTime < qEnd:
                            temporaryQuestList.append(self.addQuest(quest, True))
                            print("Verdict: Temporary")
                            continue
                    if currentTime >= qEnd:
                        self.expiredQuests.append(self.addQuest(quest, True))
                        print("Verdict: Expired")
                        continue
                    else:
                        temporaryQuestList.append(self.addQuest(quest, True))
                        print("Verdict: Temporary")
                        continue
                else: 
                    temporaryQuestList.append(self.addQuest(quest, True)) 
                    print("Verdict: Temporary")
                    # temporary quest list to be added to proper quest list
                time.sleep(0.5)
            print(f"Refreshing Daily Quests. There are currently: {len(temporaryQuestList)} daily quests added. There are {len(self.queuedQuests)} queued quests and {len(self.expiredQuests)} expired quests.")
            self.dailyQuestList = temporaryQuestList.copy()
            self.saveState()
        def timeSens(self):
            import threading as th
            import time
            from datetime import timedelta
            #from functions.opheliaDiscord import discordLoop, sendChannel
            #from functions.opheliaAsync import async_to_sync
            # TODO: replace req with opheNeu.opheliaRequired 
            def timeSensitiveQuestHandler(self, warningThreshold: timedelta = timedelta(minutes=30)):
                firstRun = True
                while req:
                    from opheliaPlugins import plugins 
                    reminder = []
                    for quest in self.dailyQuestList + self.mainQuestList:
            # Checks if the quest has expired
                        currentTime = datetime.now().time()
                        if quest.TimeEnd:
                            if currentTime < quest.TimeEnd.time():
                                self.expiredQuests.append(self.addQuestWizard(questName = quest.questName, questType = quest.questType, questLevel = quest.questLevel, timeStart = quest.timeStart, timeEnd = quest.timeEnd, returnQuest = True))
                            if quest.questType == "daily": self.dailyQuestList.remove(quest)
                            elif quest.questType == "main": self.mainQuestList.remove(quest)
            # Checks if any quest is near expiry. Takes quest time end - warning threshold to check if its earlier than 1 hour
                        if quest.TimeEnd:
                            quest_end_datetime = datetime.combine(datetime.today(), quest.TimeEnd.time())
                            threshold_time = quest_end_datetime - warningThreshold 

                            if currentTime > threshold_time.time():
                                reminder.append(f"{quest.questName} ends in {quest.TimeEnd - datetime.now()}")
            # Checks if queued quest can be started
                    for quest in self.queuedQuests.copy():
                        if quest.TimeStart:
                            if currentTime >= quest.TimeStart.time():
                                if quest.questType == "daily" and quest not in self.dailyQuestList: self.dailyQuestList.append(self.addQuestWizard(questName = quest.questName, questType = quest.questType, questLevel = quest.questLevel, timeStart = quest.timeStart, timeEnd = quest.timeEnd, returnQuest = True))
                                elif quest.questType == "main" and quest not in self.mainQuestList: self.mainQuestList.append(self.addQuestWizard(questName = quest.questName, questType = quest.questType, questLevel = quest.questLevel, timeStart = quest.timeStart, timeEnd = quest.timeEnd, returnQuest = True))
                                self.queuedQuests.remove(quest)           
                    if firstRun:
                        firstRun = False
                    else:
                        if self.dailyCount < 4: t = "no_dailies"
                        elif self.dailyCount < 8: t = "half_dailies"
                        else: t = "full_dailies"
                        fa = opheNeu.getRandomDialogue(t)
                        if len(self.dailyQuestList) != 0: 
                            fa += f"\nRemaining Daily quests: " + str(len(self.dailyQuestList))
                        if len(reminder) > 0:
                            fa += f"\nThe following quests are expiring soon: " + ", ".join(reminder)
                        plugins["Transmission"].audioThroughMic(fa, True, False)
                        print(fa)
                    #async_to_sync(sendChannel("Ticket routine check in. Remaining quests: " + str(len(self.dailyQuestList + self.mainQuestList)), "logChannel"), discordLoop)
                    self.saveState()
                    time.sleep(1800) # waits 30 minutes  
            req = True
            warningThreshold = timedelta(hours=1)
            timeSensitiveThread = th.Thread(target=timeSensitiveQuestHandler, args=(self, warningThreshold), daemon=True)
            timeSensitiveThread.start()
            return True
        def checkProgress(self, *args):
            dailyCount = self.dailyCount
            tierIncrement = self.tierIncrement
            return f"{dailyCount} out of 8 daily quests completed. Tier increment is currently {tierIncrement}. Currently {len(self.dailyQuestList)} daily quests and {len(self.mainQuestList)} main quests remaining."
            pass
        def listQuests(self, isPrint=True, which="both", *args):
            if isPrint:
                print("Daily Quests:")
                for quest in self.dailyQuestList:
                    print (f"Quest Name: {quest.QuestName} | Reward: {quest.QuestReward}")
                print("\nMain Quests:")
                for quest in self.mainQuestList:
                    print (f"Quest Name: {quest.QuestName} | Reward: {quest.QuestReward}")
                which = which.lower()
                if which == "daily": return self.dailyQuestList
                elif which == "main": return self.mainQuestList
            return self.dailyQuestList + self.mainQuestList
        def handleListQuests(self, *args):
            """
                Types: 
                    Full - Gives all information
                    Short - Only gives names
                    Half - Gives names and rewards
                    r suffix returns the given list
            """
            questList = self.listQuests(isPrint=True)
            command = args[0] if args else "short"
            returnFlag = False
            res = []
            if questList:
                if command.startswith("r"):
                    command = command[1:]
                    returnFlag = True
                for quest in questList:
                    if command == "full":
                        res.append(f"Quest Name: {quest.QuestName} | Type: {quest.QuestType} | Level: {quest.QuestLevel} | Time Start: {quest.TimeStart} | Time End: {quest.TimeEnd} | Reward: {quest.QuestReward}")
                    elif command == "short":
                        res.append(f"{quest.QuestName}")
                    elif command == "half":
                        res.append(f"{quest.QuestName} | {quest.QuestReward}")
                    else: 
                        return "The available types are Full, Short, and Half. Prefix r if you want the list returned"
                if returnFlag:
                    return res
                return ("\n").join(res)
            else:
                return "There are no quests to list"
        def finishQuest(self, *args):
            if args: name = args[0]
            else: name = self.questHelper("Quest Name")
            for quest in self.dailyQuestList + self.mainQuestList:
                if quest.QuestName.lower() == name.lower():
                    results = quest.finishQuest(tierIncrement=self.tierIncrement, dailyCount=self.dailyCount)
                    self.dailyCount = results["dailyCount"]
                    self.tierIncrement = results["tierIncrement"]
                    reward = (f"Master's reward is {results['reward']}")
                    if quest.QuestType == "daily": self.dailyQuestList.remove(quest)
                    elif quest.QuestType == "main": self.mainQuestList.remove(quest)
                    self.saveState()
                    return f"Quest has been succesfully finished. {reward}. There are currently {len(self.dailyQuestList)} daily quests and {len(self.mainQuestList)} main quests remaining."
            return f"Couldn't find a quest with the name {name}"
        def saveState(self):
            """
                Saves the current state and limits backups to the most recent 'backup_limit' count.
                Also refreshes the daily quests if the date has changed between save time and last save.
                Returns True if successful.
            """
            backup_limit = 5
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)

            try:                
                if os.path.exists(self.path):                    
                    lastSave = datetime.fromtimestamp(os.path.getmtime(self.path)).date()
                    backupPath = os.path.join(backup_dir, f"TicketBackup_{lastSave.strftime('%Y-%m-%d')}.json")      
                    shutil.copyfile(self.path, backupPath)
                    if lastSave < datetime.now().date(): 
                        os.remove(self.path)
                        print("Last save was on a different day. Refreshing daily quests...")
                        self.refreshFromPersistent()
                params = {
                    "dailyCount": self.dailyCount,
                    "tierIncrement": self.tierIncrement,
                    "questList": 
                        [
                            {
                                "questName": quest.QuestName,
                                "questType": quest.QuestType,
                                "questLevel": quest.QuestLevel,
                                "timeStart": quest.TimeStart.isoformat() if quest.TimeStart else None,
                                "timeEnd": quest.TimeEnd.isoformat() if quest.TimeEnd else None,
                                "questReward": quest.QuestReward,
                                "questRewardPool": quest.QuestRewardPool
                            }
                            for quest in self.listQuests(False)
                        ],
                    "persistentDaily": 
                    [
                        {
                            "questName": quest.questName,
                            "timeStart": quest.timeStart.isoformat() if quest.timeStart else None,
                            "timeEnd": quest.timeEnd.isoformat() if quest.timeEnd else None
                        }
                        for quest in self.persistentDaily
                    ]
                }  
                with open(self.path, "w") as file:
                    json.dump(params, file, indent=4)

                backups = sorted(
                    [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.startswith("TicketBackup_")], key=os.path.getctime
                )
                while len(backups) > backup_limit:
                    os.remove(backups.pop(0))

            except Exception as e:
                print(f"Failed to save state: {e}")
                return False
            return True    
        def loadState(self):
            """
                Returns True if successful
            """
            if not os.path.exists(self.path): return False
            with open(self.path, "r") as file:
                params = json.load(file)
            self.dailyCount = params["dailyCount"]
            self.tierIncrement = params["tierIncrement"]
            questList = params.get("questList", [])
            persistentDaily = params.get("persistentDaily", [])
            for quest in questList:
                self.addQuest(self.genericQuest(
                    quest["questName"],
                    questType=quest.get("questType", "daily"),
                    questLevel=quest.get("questLevel", 0),
                    timeStart=datetime.fromisoformat(quest["timeStart"]) if quest["timeStart"] else None,
                    timeEnd=datetime.fromisoformat(quest["timeEnd"]) if quest["timeEnd"] else None,
                    questReward=quest.get("questReward", "No reward"),
                    questRewardPool=quest.get("questRewardPool", self.dailyRewardList if quest["questType"] == "daily" else self.mainRewardList))
                    )
            for quest in persistentDaily:
                self.addToPersistent(
                    quest["questName"], 
                    datetime.fromisoformat(quest["timeStart"]) if quest["timeStart"] else None,
                    datetime.fromisoformat(quest["timeEnd"]) if quest["timeEnd"] else None)
            return True

    def __init__(self):
        super().__init__(
            name="Ticket", 
            prompt="Which command would you like to execute?", 
            description="Template", 
            needsArgs=True, 
            operaOnly=True)
        self.qm = None

    def interactWithQuests(self, mode, args):    # legend for cheatResult
        controls = {
            "finish": self.qm.finishQuest,          # need quest name
            "list": self.qm.handleListQuests,             
            "new": self.qm.addQuestWizard,          # need quest name, type, level
            "add": self.qm.addToPersistent,         # need quest name
            "remove": self.qm.removeFromPersistent, # need quest name
            "progress": self.qm.checkProgress,
            "refresh": self.qm.refreshFromPersistent,
            "save": self.qm.saveState,
            "load": self.qm.loadState
        }
        try:
            return controls[mode](*args)
        except KeyError:
            return f"Command not recognized. Available commands: {', '.join(controls.keys())}."
    
    def qm(self):
        return self.qm

    def startQuestManager(self)->str:
        self.qm = self.questManager()
        count = str(self.qm.dailyCount)
        if self.qm.timeSens(): print("Ticket handler operational")
        else: print("FAILED: Ticket handler not operational")
        return f"{count} out of 8"

    def execute(self):
        res = self.prepExecute()
        return self.cheatResult(command=res)

#test input "new questname questtype questlevel"
#test input "add questname"
    def cheatResult(self, **kwargs):
        import re
        string = kwargs["command"]
        mode = string.split(" ")[0].lower()
        string = string.replace(mode + " ", "").replace(mode, "").lower()
        type = "main" if string.__contains__("main") else "daily" if string.__contains__("daily") else None
        string = string.replace("main ", "").replace("daily ", "")
        numbers = re.findall(r'\d+', string)
        level = int(numbers[-1]) if numbers else None
        name = re.sub(r'\d+$', '', string).strip()
        
        args = []
        if name: args.append(name)
        if type: args.append(type)
        if level: args.append(level)
        opheNeu.debug_log(f"Mode: {mode} | Args: {args}")
        return self.interactWithQuests(mode = mode, args = args)

def get_plugin():
    return plugin()

