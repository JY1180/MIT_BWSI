from enum import Enum
from random import randint

class State(Enum):
    ZOMBIE = "zombie"
    HEALTHY = "healthy"
    INJURED = "injured"
    CORPSE = "corpse"

"""
Origional values:
SAVE = 30
SQUISH = 5
SKIP = 15
SCRAM = 120
"""
#makes the time you have to do something random

class ActionCost(Enum):
    SAVE = randint(20,40)
    SQUISH = 10.01
    SKIP = 10
    SCRAM = randint(100,140)

