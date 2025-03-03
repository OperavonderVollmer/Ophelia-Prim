from abc import ABC, abstractmethod
from datetime import datetime
import random
import json
import os
import shutil

class questManager:

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

    class mainQuest(quest):
        def __init__(self, questName: str, questType: str, questLevel: int, timeStart: datetime = None,timeEnd: datetime = None, questReward: str = None, questRewardPool: list = None):
            super().__init__(
                questName, 
                questType, 
                questLevel, 
                timeStart, 
                timeEnd, 
                questReward = questReward if isinstance(questReward, str) else random.choice(questRewardPool[min(questLevel, len(questRewardPool) - 1)]) if questRewardPool else "No reward", 
                questRewardPool=questRewardPool)

        def updateQuestPool(self, questRewardPool):
            self.questRewardPool = questRewardPool
            self.questReward = random.choice(self.questRewardPool[min(self.questLevel, len(self.questRewardPool) - 1)])
            return True

        def finishQuest(self, **kwargs):
            ti = kwargs["tierIncrement"]
            decision = input(f"The reward is `{self.questReward}`. You currently have {ti} tier increment.\nClaim[1], Upgrade[2], or Pass[3]?: ").lower()
            if decision == "2": 
                if ti != 0: 
                    self.questReward = random.choice(self.questRewardPool[min(ti + self.questLevel, len(self.questRewardPool) - 1)])
                    ti = 0
                else: print("You have no tier increment for an upgrade. Regular reward will be given.")
            elif decision == "3": 
                ti += 1
                self.questReward = "+1 to tier increment"
            return {"dailyCount": kwargs["dailyCount"], "tierIncrement": ti, "reward": self.questReward}

    class genericQuest:
        def __init__(self, questName: str, questType: str, questLevel: int = None, timeStart: datetime = None, timeEnd: datetime = None):
            self.questName = questName
            self.questType = questType
            self.questLevel = questLevel
            self.timeStart = timeStart
            self.timeEnd = timeEnd

    def __init__(self):
        self.dailyRewardList = [ # daily quest rewards are divided into three tiers
            ["Get a cup of coffee"],
            ["Binge memes 30 minutes", "Listen to an album", "Play a game for 30 minutes", "Brain off for 30 minutes"],
            ["Watch 2-3 amount of episodes of show", "Watch a movie", "Sensual Exercise", "Game time"],
        ]

        self.mainRewardList = [ # main quest rewards are divided into 10 tiers, some scaling with level of tier
            # TODO: add quests
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

        # TODO: move counters to a separate file for persistence
        self.dailyCount = 0
        self.tierIncrement = 0
        self.mainQuestList = []
        self.dailyQuestList = []
        self.persistentDaily = []
        self.queuedQuests = [] 
        self.expiredQuests = []
        self.path = "CurrentTickets.json"
        self.persistentPath = "PersistentTickets.json"
        #self.loadState()

    def addQuestWizard(self, questName: str, questType: str, questLevel: int = None, timeStart: datetime = None, timeEnd: datetime = None):
        if questLevel is not None and questType == "daily": print("Daily quests do not have a level.")
        self.addQuest(self.genericQuest(questName, questType, questLevel, timeStart, timeEnd))

    def addQuest(self, q: genericQuest, giveList = False):
        """
            Returns quest if giveList is not None. Else, automatically appends quest to associated quest list.
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
        #self.saveState()

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

    def addToPersistent(self, questName: str, timeStart: datetime = None, timeEnd: datetime = None):
        newDaily = self.genericQuest(questName, "daily", timeStart, timeEnd)
        self.persistentDaily.append(newDaily)


    def removeFromPersistent(self, questName: str):
        for quest in self.persistentDaily:
            if quest.QuestName == questName:
                self.persistentDaily.remove(quest)
                return True
        return False

    def refreshFromPersistent(self):
        self.dailyCount = 0
        temporaryQuestList = []
        for quest in self.persistentDaily:
            if quest.TimeStart is not None and quest.TimeStart < datetime.now():
                self.queuedQuests.append(self.addQuest(quest, True))
            elif quest.TimeEnd is not None and quest.TimeEnd < datetime.now():
                self.expiredQuests.append(self.addQuest(quest, True))
            else: temporaryQuestList.append(self.addQuest(quest, True))

        self.dailyQuestList = temporaryQuestList
        
    def timeSens(self):
        import threading as th
        import time
        from datetime import timedelta
        # TODO: replace req with opheNeu.opheliaRequired 
        def timeSensitiveQuestHandler(self, warningThreshold: timedelta = timedelta(minutes=30)):
            while req:
                reminder = []
                for quest in self.dailyQuestList + self.mainQuestList:
        # Checks if the quest has expired
                    if quest.TimeEnd is not None and quest.TimeEnd < datetime.now():
                        self.expiredQuests.append(self.addQuest(quest, True))
                        if quest.questType == "daily": self.dailyQuestList.remove(quest)
                        elif quest.questType == "main": self.mainQuestList.remove(quest)
        # Checks if any quest is near expiry
                    if quest.TimeEnd is not None and datetime.now() > quest.TimeEnd - warningThreshold:
                        reminder.append(f"{quest.questName} ends in {quest.TimeEnd - datetime.now()}")
        # Checks if queued quest can be started
                for quest in self.queuedQuests.copy():
                    if quest.TimeStart is not None and quest.TimeStart < datetime.now():
                        if quest.questType == "daily" and quest not in self.dailyQuestList: self.dailyQuestList.append(self.addQuest(quest, True))
                        elif quest.questType == "main" and quest not in self.mainQuestList: self.mainQuestList.append(self.addQuest(quest, True))
                        self.queuedQuests.remove(quest)
                if len(reminder) > 0:
                    from opheliaPlugins import plugins
                    plugins["Transmission"].audioThroughMic(f"The following quests are expiring soon: {', '.join(reminder)}", True, False)
                time.sleep(1800) # waits 30 minutes            
        req = True
        warningThreshold = timedelta(hours=1)
        timeSensitiveThread = th.Thread(target=timeSensitiveQuestHandler, args=(self, warningThreshold), daemon=True)
        timeSensitiveThread.start()

    def listQuests(self, isPrint=True):
        if isPrint:
            print("Daily Quests:")
            for quest in self.dailyQuestList:
                print(f"Quest Name: {quest.QuestName} | Reward: {quest.QuestReward}")
            print("\nMain Quests:")
            for quest in self.mainQuestList:
                print(f"Quest Name: {quest.QuestName} | Reward: {quest.QuestReward}")
        return {"daily": self.dailyQuestList, "main": self.mainQuestList, "all": self.dailyQuestList + self.mainQuestList}

    def finishQuest(self, name: str):

        for quest in self.dailyQuestList + self.mainQuestList:
            if quest.QuestName.lower() == name.lower():
                results = quest.finishQuest(tierIncrement=self.tierIncrement, dailyCount=self.dailyCount)
                self.dailyCount = results["dailyCount"]
                self.tierIncrement = results["tierIncrement"]
                print(f"Reward: {results['reward']}")
                if quest.QuestType == "daily": self.dailyQuestList.remove(quest)
                elif quest.QuestType == "main": self.mainQuestList.remove(quest)
                #self.saveState()
                return True
        return False
        

    def saveState(self):
        """
            Returns True if successful
        """
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
                    for quest in self.listQuests()["all"]
                ],
            "persistentDaily": 
            [
                {
                    "questName": quest.QuestName,
                    "timeStart": quest.TimeStart.isoformat() if quest.TimeStart else None,
                    "timeEnd": quest.TimeEnd.isoformat() if quest.TimeEnd else None
                }
                for quest in self.persistentDaily
            ]
        }        
        try:
            if os.path.exists(self.path): shutil.copyfile(self.path, f"{self.path}{datetime.now().strftime('%Y-%m-%d_%H-%M')}.backup")
            with open(self.path, "w") as file:
                json.dump(params, file, indent=4)
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

qm = questManager()

qm.testPopulateQuests(10)
qm.listQuests()

while True:
    dec = input("Add Quest[1], Complete Quest[2], List Quests[3], Save State[4], Load State[5]? ").lower()
    if dec == "1": 
        params = {
            "questName": input("Quest Name: "),
            "questType": input("Quest Type: "),
            "questLevel": input("Quest Level: "),
        }
        qm.addQuestWizard(questName=params["questName"], questType=params["questType"], questLevel=params["questLevel"])
    elif dec == "2": qm.finishQuest(input("Quest Name: "))
    elif dec == "3": qm.listQuests()
    elif dec == "4": qm.saveState()
    elif dec == "5": qm.loadState()