import random
from action_class import *

from sqlalchemy.sql.operators import truediv


# room class

class Room:
    def __init__(self, type):
        self.type = type


    def describe(self):
        description = {
             "enemy": "A hostile enemy appears!",
            "treasure": "There is a treasure chest in the room.",
            "empty": "The room is empty.",
            "junction": "There is a junction ahead.",
            "merchant": "You arrive at the merchant.",
            "boss": "A powerful boss stands before you!"



        }
        return description[self.type]

#player class
class Player:
    def __init__(self):
        self.hp= 25
        self.attack=random.randint(3,7)
        self.defense=random.randint(2,5)
        self.inventory=[]

## npc class
class Npc:
    def __init__(self,type):
        self.type = type

        stats={
            "enemy": {
                "name": "Goblin",
                "hp": 12,
                "attack": random.randint(1, 4),
                "defense": random.randint(0, 2)
            },
            "boss": {
                "name": "Dämonenlord",
                "hp": 30,
                "attack": random.randint(5, 8),
                "defense": random.randint(2, 4)
            }
        }
        npc_stats = stats[type]

        self.name = npc_stats["name"]
        self.hp = npc_stats["hp"]
        self.attack = npc_stats["attack"]
        self.defense = npc_stats["defense"]


# action class




# dungeon class
class Dungeon:
    def __init__(self, size=6):
        self.rooms = self.generate_dungeon(size)

    def generate_dungeon(self, size):
        rooms = []
        room_types = ["enemy", "treasure", "empty", "merchant"]

        unique=["treasure","merchant"] # theese rooms can only be appear once per run
        used_unique=set()

        rooms.append(Room("enemy")) ## first room is a enemy

        for _ in range(size - 2):
            possible=[]

            for r in room_types:
                if r in used_unique and r in unique:
                    continue

                possible.append(r)

            chosen=random.choice(possible)
            if chosen in unique:
                used_unique.add(chosen)

            rooms.append(Room(chosen))

        rooms.append(Room("boss"))
        return rooms

# test

### main game

def main():
    dungeon=Dungeon(size=6)
    player = Player()
    print("Welcome to Dungeon !!!")
    for i,room in enumerate(dungeon.rooms):
        print(f"{i}. {room.describe()}")
        if room.type == "enemy":
            npc = Npc("enemy")
            action = Action("fight", None)
            action.fight(player, npc)


        elif room.type == "boss":
            npc = Npc("boss")
            action = Action("fight", None)
            action.fight(player, npc)

        input("Press Enter to continue in the dungeon...")

    print("LEVEL CLEARED !!!!!")

if __name__ == "__main__":
    main()
