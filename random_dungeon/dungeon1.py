import random


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


### main game

def main():
    dungeon=Dungeon(size=6)
    print("Welcome to Dungeon !!!")
    for i,room in enumerate(dungeon.rooms):
        print(f"{i}. {room.describe()}")

        input("Press Enter to continue in the dungeon...")

    print("LEVEL CLEARED !!!!!")

if __name__ == "__main__":
    main()