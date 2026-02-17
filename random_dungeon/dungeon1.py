import random

from sqlalchemy.sql.operators import truediv


# room class

class Room:
    def __init__(self, type):
        self.type = type


    def describe(self):
        description = {
            "enemy": "Ein feindlicher Gegner erscheint!",
            "treasure" :" Im Raum ist ein Schatztruhe.",
            "empty":"Der Raum ist leer.",
            "junction":"Es gibt eine Abzweigung. ",
            "merchant":"Du erreichst den Händler.",
            "boss":"Ein mächtiger Boss steht vor dir ! "


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

class Action:
    def __init__(self,name,function):
        self.name=name
        self.function=function

    def fight(player,npc):
        print("Fight Started")
        print(f"Your opponent {npc.name} - HP: {npc.hp} - Attack:{npc.attack} - Defense:{npc.defense}")
        print(f"Your Stats - HP:{player.hp} - Attack:{player.attack} - Defense:{player.defense}")

        while npc.hp > 0 and player.hp >0:

        #players turn

            dmg_2_enm= max(0, player.attack- npc.defense)
            npc.hp -= dmg_2_enm
            print("You Attack....")
            if dmg_2_enm>0:
                print(f"You attacked and dealt {dmg_2_enm} damage")
                print(f"Enemy's HP: {npc.hp}")
            else:
                print("You missed!")

            if npc.hp <= 0:
                print(f" {npc.name} is dead")
                return True

        # enemy turn
            dmg_2_play = max(0, npc.attack - player.defense)
            player.hp -= dmg_2_play
            print("Your Enemy Attack....")
            if dmg_2_play > 0:
                print(f"Your enemy attacked and dealt {dmg_2_play} damage")
                print(f"Your HP: {player.hp}")
            else:
                print("Your Enemy  missed!")

            if player.hp <= 0:
                print(f" your dead")
                exit()
        return False




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
            Action.fight(player, npc)

        elif room.type == "boss":
            npc = Npc("boss")
            Action.fight(player, npc)

        input("Press Enter to continue in the dungeon...")

    print("LEVEL CLEARED !!!!!")

if __name__ == "__main__":
    main()
