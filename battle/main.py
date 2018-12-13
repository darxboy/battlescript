from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random



#create black magic
fire = Spell("Fire", 10, 600, "black")
thunder = Spell("Thunder", 50, 600, "black")
blizzard = Spell("Blizzard", 80, 600, "black")
meteor = Spell("Meteor", 30, 1200, "black")
quake = Spell("Quake", 20, 140, "black")

#create white magic
cure = Spell("Cure", 12, 622, "white")
cura = Spell("Cura", 32, 442, "white")
curaga = Spell("Curaga", 50, 6000, "white")

#Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member",9999)
hielixer = Item("Mega Elixer", "elixer", "Fully restores HP/MP",9999)
grenade = Item("Grenade", "attack", "Deals 500 Damage", 500)


#Option of Player

player_spells = [fire, thunder, blizzard, meteor,cure, cura]
enemy_spells = [fire, meteor, cura, curaga]
player_items = [{"item" :potion, "quantity": 5},{"item": hipotion, "quantity": 0}, {"item": superpotion,"quantity":15},
                {"item" : elixer,"quantity": 30}, {"item": hielixer, "quantity": 22},{"item": grenade,"quantity":5}]


#Instatiate People
player1 = Person("Valos: ",1268,532, 342, 223, player_spells, player_items)
player2 = Person("Nick : " ,268,332, 1242, 123, player_spells, player_items)
player3 = Person("Vio  : ",3468,422, 5242, 523, player_spells, player_items)


enemy1 = Person("Magus", 1200, 265, 45, 23,enemy_spells,[])
enemy2 = Person("Mag", 1900, 565, 245, 213,enemy_spells,[])
enemy3 = Person("Gus", 200, 2165, 435, 263,enemy_spells,[])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i= 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)


while running:
    print("==========================================================")

    print("\n\n")
    print("NAME              HP                           MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("   Choose Action:  ")
        index = int(choice)- 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked" + enemies[enemy].name + " for", dmg, "points of damage")

            if enemies[enemy].get_hp()== 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]


        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("  Choice magic:"))-1

            if magic_choice == -1:
                continue


            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for" , str(magic_dmg), "HP", bcolors.ENDC )
            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage to "+ enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]



        elif index == 2:
            player.choose_items()
            item_choice = int(input("   Choose Item : "))- 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"]== 0:
                print(bcolors.FAIL + "\n" + "None left...." + bcolors.ENDC)
                continue

            player_items[item_choice]["quantity"]-= 1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "Heals For" + str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "Fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":

                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)


                print(bcolors.FAIL + "\n" + item.name + "deals", str(item.prop), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ","")+ " has died.")
                    del enemies[enemy]

    # Check If Battle Is Over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp()== 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp()== 0:
            defeated_players += 1

    #Check If Player Won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
   #Check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + " Your Enemy Has defeated you! " + bcolors.ENDC)
        running = False

    print("\n")

    #Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:

            # Choose Attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", " ") + " attacks " + players[target].name.replace(" ", "") + " for ", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + "heals "+ enemy.name + " for", str(magic_dmg), "HP", bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "")+"'s "+ spell.name + "deals", str(magic_dmg),
                      "points of damage to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[player]

           # print("Enemy Choose", spell, "damage is", magic_dmg)
