from gameplay.enums import ActionCost
from gameplay.ui import UI

class ScoreKeeper(object):
    def __init__(self, shift_len, capacity):
        self.ambulance = {
            "zombie": 0,
            "injured": 0,
            "healthy": 0,
            "corpse": 0,
            "paramedic": 0,
            "protector": 0
        }
        self.scorekeeper = {
            "killed": 0,
            "injured humans saved": 0,
            "healthy humans saved": 0,
            "total moves": 0,
            "correct moves": 0,
            "squish count": 0,
            "skip count": 0,
            "act count": 0,
            "suggest count": 0,
            "info count": 0,
            "if paramedic": 0,
            "if protector": 0,
            "scram at low": 0,
            "scram at high": 0
        }
        self.__capacity = capacity
        self.remaining_time = int(shift_len)  # minutes
        self.morality_score = 50
        self.has_paramedic = False

    def addtocorrectmoves(self):
        self.scorekeeper["correct moves"] += 1

    def addtoactcount(self):
        self.scorekeeper["act count"] += 1

    def addtosuggestcount(self):
        self.scorekeeper["suggest count"] += 1

    def addtoinfocount(self):
        self.scorekeeper["info count"] += 1

    def addtoifprotector(self):
        self.scorekeeper["if protector"] += 1

    def addtoifparamedic(self):
        self.scorekeeper["if paramedic"] += 1

    def add_action(self):
        self.scorekeeper["total moves"] += 1


    def save(self, humanoid):
        self.remaining_time -= ActionCost.SAVE.value
        if humanoid.is_injured():
            self.ambulance["injured"] += 1
        elif humanoid.is_corpse():
            self.ambulance["corpse"] += 1
        elif humanoid.is_healthy():
            self.ambulance["healthy"] += 1

    def squish(self, humanoid):
        self.scorekeeper["squish count"] += 1
        self.remaining_time -= ActionCost.SQUISH.value
        if humanoid.is_injured() or humanoid.is_healthy():
            self.scorekeeper["killed"] += 1

    def skip(self, humanoid):
        self.scorekeeper["skip count"] += 1
        self.remaining_time -= ActionCost.SKIP.value
        if humanoid.is_injured():
            self.scorekeeper["killed"] += 1

    def scram(self):
        self.remaining_time -= ActionCost.SCRAM.value
        if self.ambulance["zombie"] > 0:
            self.scorekeeper["killed"] += self.ambulance["injured"] + self.ambulance["healthy"]
        else:
            self.scorekeeper["injured humans saved"] += self.ambulance["injured"]
            self.scorekeeper["healthy humans saved"] += self.ambulance["healthy"]

        self.ambulance["zombie"] = 0
        self.ambulance["injured"] = 0
        self.ambulance["healthy"] = 0
        self.ambulance["corpse"] = 0

    def update_time(self, time_to_subtract):
        self.remaining_time -= time_to_subtract

    def get_current_capacity(self):
        return sum(self.ambulance.values())

    def at_capacity(self):
        return sum(self.ambulance.values()) >= self.__capacity

    def get_score(self):
        self.scram()
        return self.scorekeeper
    def get_zombie_count(self):
        return self.ambulance["zombie"] >= 3


    def skip_update_morality(self, humanoid): 
        #SKIP INJURED HUMAN - 10        
        #SKIP HEALTHY HUMAN - 5
        #SKIP ZOMBIE -10
        #SKIP CORPSE - 0
        if humanoid.is_zombie():
            self.morality_score += 10
        elif humanoid.is_healthy():
            self.morality_score -= 5
        elif humanoid.is_injured():
            self.morality_score -= 10
    
    def squish_update_morality(self, humanoid):
        #SQUISH ZOMBIE + 5
        #SQUISH INJURED HUMAN - 20
        #SQUISH CORPSE - 2
        #SQUISH HEALTHY HUMAN - 30
        if humanoid.is_zombie():
            self.morality_score += 5
        elif humanoid.is_healthy():
            self.morality_score -= 30
        elif humanoid.is_injured():
            self.morality_score -= 20
        elif humanoid.is_corpse(): 
            self.morality_score -= 2
    
    def save_update_morality(self, humanoid):
        #SAVE INJURED HUMAN + 20
        #SAVE HEALTHY HUMAN +10
        #save corpse  - 10?
        #save zombie -20
        if humanoid.is_zombie():
            self.morality_score -= 20
        elif humanoid.is_healthy():
            self.morality_score += 10
        elif humanoid.is_injured():
            self.morality_score += 20
        elif humanoid.is_corpse(): 
            self.morality_score -= 10

    def scram_update_morality(self):
        #SCRAM WHEN CAPACITY <5 AND NO ZOMBIE - 15
        #SCRAM WHEN CAPACITY >= 5 AND NO ZOMBIE - 2
        #SCRAM WHEN CAPACITY <5 AND ZOMBIE -5
        #SCRAM WHEN CAPACITY >=5 AND ZOMBIE -10
        if self.get_current_capacity() < 5: #punish for scramming early
            self.scorekeeper["scram at low"] += 1
            if self.ambulance["zombie"] == 0:
                self.morality_score -= 40
            else:
                self.morality_score -= 30
        
        else:
            self.scorekeeper["scram at high"] += 1
            if self.ambulance["zombie"] == 0:
                self.morality_score -= 20
            else:
                self.morality_score -= 10

    def display_morality(self):
        if self.has_paramedic:
            self.morality_score *= 1.1
        return self.morality_score



       


    

    