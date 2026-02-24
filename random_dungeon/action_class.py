class Action:
    def __init__(self,name,function):
        self.name=name
        self.function=function

    def use_item(self,player):
        print("soon...")
    def block(self,player):
        print("You brace yourself and block")

        player.temp_defense_buff = 2
        player.defense += player.temp_defense_buff
        print("Your defense temporarily increased!")

    def fight(self,player,npc):
        print("Fight Started")
        print(f"Your opponent {npc.name} - HP: {npc.hp} - Attack:{npc.attack} - Defense:{npc.defense}")
        print(f"Your Stats - HP:{player.hp} - Attack:{player.attack} - Defense:{player.defense}")

        player.temp_defense_buff = 0

        while npc.hp > 0 and player.hp >0:
    # giving options
            choice=input("""What you are gonna do?
                    F - Fight
                    B - Block
                    I - Item
                    Your Choice: """)

            if choice == "I":

                self.use_item(player)
            elif choice == "B":
                self.block(player)
            elif choice == "F":
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

                if player.temp_defense_buff > 0:
                    player.defense -= player.temp_defense_buff
                    player.temp_defense_buff = 0