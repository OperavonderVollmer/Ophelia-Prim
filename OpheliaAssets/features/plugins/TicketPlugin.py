from abc import ABC, abstractmethod
from datetime import datetime
import random 


# TODO: move lists to a separate file for persistence

dailyRewardList = [ # daily quest rewards are divided into three tiers
    ["Get a cup of coffee"],
    ["Binge memes 30 minutes", "Listen to an album", "Play a game for 30 minutes", "Brain off for 30 minutes"],
    ["Watch 2-3 amount of episodes of show", "Watch a movie", "Sensual Exercise", "Game time"],
]

mainQuestList = [ # main quest rewards are divided into 10 tiers, some scaling with level of tier
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
dailiesCount = 0
tierIncrement = 0 

class questReward(ABC):
    """
    
        Base class for quest rewards

    """
    def __init__(self, tier: int = 0, specificReward: str = None):
        self.tier = tier
        self.reward = specificReward if specificReward else None

    @property
    def Reward(self): return self.reward
    @property
    def Tier(self): return self.tier

    @abstractmethod
    def rollReward(self, tier):pass

    @abstractmethod
    def getReward(self): pass

    @abstractmethod
    def claimReward(self): pass

    def __str__(self):
        return self.reward if self.reward else None
    
class dailyReward(questReward):
    """
        Determined during initialization. Must not be initialized until reward claiming since it requires the current daily count.
        Tiers are first reward, mid day reward, and dailies completed.
        Cannot have specified reward.
    """
    def __init__(self, tier: int, ):
        super().__init__(tier)
        self.reward = self.rollReward(tier)

    def rollReward(self, tier):
        return random.choice(dailyRewardList[tier - 1])

    def getReward(self):
        return self.reward
    
    def claimReward(self):        
        t = ["First reward of the day: ", "Mid day reward: ", "Dailies completed, reward: "]
        return f"{t[self.tier - 1]}"
    
class mainReward(questReward):
    """
        Predetermined rewards at initialization.
        Upon claiming reward, have the option to claim predetermined reward, upgrade reward with tier increment, or pass reward to increase tier increment by 1
        Tiers are 1 to 10.
        Some of the rewards scale multiplicatively with tier.
        Example: Game time (X hours) where X is the tier.
        Can have specified reward.
    
    """
    def __init__(self, tier: int, specificReward: str = None):
        super().__init__(tier, specificReward)

    def rollReward(self, tier):
        # TODO: Add logic to scale with tier
        return random.choice(mainQuestList[tier - 1])

    def claimReward(self):
        global tierIncrement
        decision = input(f"The reward is {self.reward}. You currently have {tierIncrement} tier increment.\nClaim[1], Upgrade[2], or Pass[3]? ").lower()
        if decision == "2": self.upgradeReward()
        elif decision == "3": return self.passReward()
        return f"Reward for completing main quest: {self.getReward()}"

    def upgradeReward(self):
        global tierIncrement
        self.reward = self.rollReward(self.tier + tierIncrement)
        tierIncrement = 0
        return f"Reward upgraded to: {self.reward}"

    def passReward(self):
        global tierIncrement
        tierIncrement += 1
        self.reward = "+1 tier increment"
        print(f"Reward passed. The next main quest will receive a +{tierIncrement} tier bonus")

    def getReward(self):
        return self.reward



class baseQuest(ABC):
    def __init__(self, name: str, priority: int = None, timeStart: datetime = None, timeEnd: datetime = None, type: str = None):
        self.name = name
        self.priority = priority
        self.timeStart = timeStart 
        self.timeEnd = timeEnd
        self.type = type
        self.reward = None

    @property
    def Name(self): return self.name
    @property
    def Priority(self): return self.priority
    @property
    def Type(self): return self.type
    @property
    def TimeStart(self): return self.timeStart
    @property
    def TimeEnd(self): return self.timeEnd
    @property
    def TimeFrame(self) -> tuple[datetime, datetime]: return self.timeStart, self.timeEnd
    @property
    def Reward(self): 
        if self.reward.__str__(): return self.reward
        else: return f"Expected reward is {self.Priority} tier"

    @abstractmethod
    def finishQuest(self): pass

    @abstractmethod
    def claimReward(self): pass

class dailyQuest(baseQuest):
    """
    
        Completing X amount of daily quests constitutes dailies finished
        X will be 8 for now

        Completing dailies for the day raised tier increment by one
    
    """
    def __init__(self, name: str, priority: int = None, timeStart: datetime = None, timeEnd: datetime = None, type: str = None):
        super().__init__(name, priority, timeStart, timeEnd, type) 

    def finishQuest(self):
        global dailiesCount, tierIncrement
        dailiesCount += 1
        if dailiesCount == 8: tierIncrement += 1
        print(f"Daily quest {self.name} completed. {dailiesCount} dailies completed")
        return self.getReward()
    
    def getDailyCount(self): 
        global dailiesCount
        return dailiesCount

    @property
    def Reward(self):
        dailiesCount = self.getDailyCount()
        if dailiesCount < 4: tier = "Cup of coffee"
        elif dailiesCount < 8: tier = "Mid tier"
        else: tier = "Dailies completed"
        return f"Expected reward is {tier} reward"
    
    # TODO: add implementations for time frame

    def claimReward(self):
        global tierIncrement
        dailiesCount = self.getDailyCount()
        if dailiesCount < 4: tier = 1
        elif dailiesCount < 8: tier = 2
        else: tier = 3; tierIncrement += 1
        self.reward = dailyReward(tier).claimReward()
        return 
    
class mainQuest(baseQuest):
    def __init__(self, name: str, priority: int = None, timeStart: datetime = None, timeEnd: datetime = None, type: str = None):
        super().__init__(name, priority, timeStart, timeEnd, type)
        self.reward = mainReward(priority)
        print(f"Main quest {self.Name} created. Reward: {self.Reward}")

    def finishQuest(self):
        print(f"Main quest {self.name} completed")
        return self.claimReward()

    def claimReward(self):
        return self.reward.claimReward()

class questManager:
    def __init__(self):
        self.quests: dict[str, list] = {
            "daily" : [],
            "main" : []
        }
    

    def loadQuests(self):
        # TODO: Add logic that loads quests from the persistent file
        pass

    def listQuests(self):
        print("Daily Quests: " + "\n".join([f"Quest Name: {quest.Name} | Reward: {quest.Reward}" for quest in self.quests["daily"]]))
        print("Main Quests: " + "\n".join([f"Quest Name: {quest.Name} | Reward: {quest.Reward}" for quest in self.quests["main"]]))

    def addQuestWizard(self):
        name = input("Quest Name: ")
        type = input("Quest Type (Daily / Main): ").lower()
        if type == "main":
            priority = int(input("Level: "))
        else: 
            priority = None
        timeStart = input("Start Time: ")
        timeEnd = input("End Time: ")
        timeStart = None if timeStart == "" else timeStart
        timeEnd = None if timeEnd == "" else timeEnd
        print(self.addQuest(name, priority, timeStart, timeEnd, type))

    def addQuest(self, name: str, priority: int = None, timeStart: datetime = None, timeEnd: datetime = None, type: str = None):
        if type == "daily": self.quests["daily"].append(dailyQuest(name, priority, timeStart, timeEnd, type))
        elif type == "main": self.quests["main"].append(mainQuest(name, priority, timeStart, timeEnd, type))
        else: return("Input was incorrect. Try again")
        return ("Quest successfully added")

    def completeQuest(self, name: str = None, type: str = None):
        name = name or input("Quest Name: ")
        type = type or input("Quest Type (Daily / Main): ").lower()
        for quest in self.quests.get(type, []):
            if quest.Name == name:
                print(f"Completing quest: {quest.Name} | Expected Reward: {quest.Reward}")
                quest.finishQuest() 
                log = (f"Completed quest: {quest.Name}. Reward: {quest.Reward}")
                self.logQuest(quest.Name, quest.Type, quest.Reward)
                self.quests[type].remove(quest)
                return log
        return ("Quest not found")

    def logQuest(self, name: str, type: str = None, reward: str = None, time = None):
        time = time or datetime.now()
        log = {
            "Quest Name" : name,
            "Quest Type" : type,
            "Reward" : reward,
            "Completed" : time
        }
        # TODO: put log in a persistent file
        pass

manager = questManager()

print(manager.addQuest("asd", 5, None, None, "main"))
while True:
    decision = input("Add Quest[1], Complete Quest[2], List Quests[3]? ").lower()
    if decision == "1": manager.addQuestWizard()
    elif decision == "2": print(manager.completeQuest())
    elif decision == "3": manager.listQuests()
    else: break