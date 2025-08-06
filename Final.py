#Luke Edmundson
#Final Project
#Choose your adventure game
import random, os

#context
def background():
    print("Mission Home.\n"
          "You are part of an expeditionary mission on the far side of the moon.\n"
          "You and your team were gathering resources from a crater when all communication with NASA cut out.\n"
          "Your mission is to now return home. Alive.\n")
#Global variables
crew = 7

#------------player class information to save info------------
#custom character stats
class Character:
    def __init__(self, name, health, strength, stamina, wins, loses):
        self.name = name
        self.health = health
        self.strength = strength
        self.stamina = stamina
        self.wins = wins
        self.loses = loses
        self.inventory = Inventory()

    def health_check(self):
        print(f"Health is at {self.health}.")
    def stamina_check(self):
        print(f"Stamina is at {self.stamina}.")
#Track inventory of character
class Inventory:
    def __init__(self, weapon="none", gear="none", weight=50):
        self.weapon = weapon
        self.gear = gear
        self.weight = weight

    def display(self):
        print(f"Weapon: {self.weapon}, Gear: {self.gear}, Weight: {self.weight}")

#------------menu code------------
#main menu to start the game
def main_menu():
    while True:
        selection = input("\n--MAIN MENU--\n"
                          "1. Create New Game\n"
                          "2. Load Game\n"
                          "3. Delete Game\n"
                          "4. Credits\n"
                          "5. Exit\n")
        if selection == "1":
            background()
            create_new_game()
        elif selection == "2":
            load_game()
        elif selection == "3":
            delete_game()
        elif selection == "4":
            end_credits()
        elif selection == "5":
            break
        else:
            print("Invalid Selection, try again.")
#create new game function
def create_new_game():
    # making directory to Game
    if not os.path.exists("Game"):
        os.mkdir("Game")

    #limiting to 3 save files
    saves = os.listdir("Game")
    if len(saves) >= 3:
        print("Maximum of 3 save files. Please delete a save file.")
        main_menu()

    #display existing games
    if saves:
        existing_games()
    else:
        print("No save files.")

    while True:
        game_name = input("Enter a new game name (other than esc): ").strip()
        if game_name.lower() == "esc":
            print("Cannot name file 'esc'")
            continue

        file_path = os.path.join("Game", f"{game_name}.txt")

        #check if game name already exists
        if os.path.exists(file_path):
            print("Game file already exists. Please choose a different name.")
            continue

    #saving character info
        player = Character(name=game_name, health=100, strength=100, stamina=100, wins=0, loses=0)
        with open(file_path, "w") as f:
            f.write(f"{player.name},{player.health},{player.strength},{player.stamina}, {player.wins}, {player.loses}"
                    f"{player.inventory.weapon},{player.inventory.gear},{player.inventory.weight}\n")

        #prompt to let user know game saved
        print(f"Game saved as {file_path}")
        run_game_beginning(player)
        break
#function to load previous game
def load_game():
    if not os.path.exists("Game"):
        print("No save files found.")
        return

    saves = os.listdir("Game")
    #checks for existing games
    if not saves:
        print("No save files.")
        return
    #print games
    existing_games()

    game_name = input("Enter game name you would like to load (type 'esc' to go to main menu): ").strip()
    if game_name.lower() == "esc":
        print("Load canceled. Returning to main menu.")
        return
    file_path = os.path.join("Game", f"{game_name}.txt")
    if not game_check(file_path):
        return

    try:
        with open(file_path, "r") as f:
            line = f.readline().strip()
            parts = line.split(",")
            name, health, strength, stamina, wins, loses = parts[0:6]
            weapon, gear, weight = parts[6:9]
            checkpoint_label = parts[7] if len(parts) > 7 else "start"

            player = Character(name, int(health), int(strength), int(stamina), int(wins), int(loses))
            player.inventory = Inventory(weapon, gear, int(weight))

    except Exception as e:
        print(f"Error loading game. Try again. {e}")
        return

    checkpoint(player, checkpoint_label)
#function to delete game
def delete_game():
    game = os.listdir("Game")
    saves = os.listdir("Game")
    #printing existing game file
    print("Existing save files:")
    for save in sorted(saves):
        print(f"- {save.replace('.txt', '')}")

    print("WARNING! This action cannot be undone! (type 'esc' to escape)")
    game_name = input("Enter game name you would like to delete: ").strip()
    if game_name.lower() == "esc":
        print("Delete canceled.")
        return
    file_path = os.path.join("Game", f"{game_name}.txt")

    if not game_check(file_path):
        return
    if game:
        confirm = input(f"Are you sure you want to delete '{game_name}'? (y/n): ").lower() #REPLACE THIS WITH A TRY STATEMENT
        if confirm == "y":
            os.remove(file_path)
            print(f"Game '{game_name}' deleted successfully.")
        else:
            print("Returning to main menu.")
            main_menu()
#credits function
def end_credits():
    print("---CREDITS---\n"
          "Game Director: Luke Edmundson\n"
          "Lead Gameplay Programmer: Luke Edmundson\n"
          "UX Developer: <NAME>\n"
          "Level Design: Luke Edmundson\n"
          "Gameplay Tester: Luke Edmundson\n"
          "Save System Programmer: Luke Edmundson\n"
          "Creative Director: Luke Edmundson\n"
          "Credit Design: Luke Edmundson\n"
          "Credit Tester: Luke Edmundson\n"
          "Publisher: Luke Edmundson\n"
          "Copyright© Luke Edmundson 2025\n"
          "All rights reserved.\n"
          "---END CREDITS---\n")
    main_menu()

#------------Game existence check------------
#function to display existing games
def existing_games():
    saves = os.listdir("Game")
    #printing existing games
    print("Existing save files:")
    for save in sorted(saves):
        #get rid of .txt for display
        if save.endswith(".txt"):
            print(f"- {save.replace('.txt', '')}")
#check if game file exists
def game_check(file_path):
    if not os.path.exists(file_path):
        print(f"Game name '{file_path}' does not exist.")
        return False
    return True

#------------save game info------------
#function to save game where players leaves it
def save_point(player, checkpoint_label="start"):
    file_path = os.path.join("Game", f"{player.name}.txt")
    try:
        with open(file_path, "w") as f:
            f.write(f"{player.name},{player.health},{player.strength},{player.stamina}, {player.wins}, {player.loses}"
                    f"{player.inventory.weapon},{player.inventory.gear},{player.inventory.weight},{checkpoint_label}\n")
        print(f" Game saved at checkpoint: {checkpoint_label}")
    except Exception as e:
        print(f"Failed to save game: {e}")
#checkpoint for each path
def checkpoint(player, checkpoint_label):
    print(f"Game '{player.name}' loaded successfully. Resuming from checkpoint: {checkpoint_label}")

    if checkpoint_label == "start":
        run_game_beginning(player)
    elif checkpoint_label == "path_four":
        path_four(player)
    elif checkpoint_label == "path_five":
        path_five(player)
    elif checkpoint_label == "path_six":
        path_six(player)
    elif checkpoint_label == "path_seven":
        path_seven(player)
    elif checkpoint_label == "path_eight":
        path_eight(player)
    elif checkpoint_label == "path_nine":
        path_nine(player)
    elif checkpoint_label =="path_ten":
        path_ten(player)
    elif checkpoint_label == "path_eleven":
        path_eleven(player)
    elif checkpoint_label == "path_twelve":
        path_twelve(player)
    elif checkpoint_label == "path_thirteen":
        path_thirteen(player)
    elif checkpoint_label == "path_fourteen":
        path_fourteen(player)
    elif checkpoint_label == "path_fifteen":
        path_fifteen(player)
    elif checkpoint_label == "path_sixteen":
        path_sixteen(player)
    else:
        print("Unknown checkpoint. Starting from beginning.")
        run_game_beginning(player)

#------------player stats and functions to check if player stats are true------------
#function to check stats of player
def player_stats(player):
    print(f"Health is {player.health}")
    print(f"Strength is {player.strength}")
    print(f"Weight is {player.inventory.weight}")
    print(f"Your weapon is {player.inventory.weapon}")
    print(f"Your gear is {player.inventory.gear}")
    print("Crew members left:" + str(crew))
    print("")
#function to see if player is still alive
def is_alive(player):
    if player.health > 0:
        return player.health
    elif player.health < 0:
        print("You have died. Game Over.")
        player.loses += 1
        main_menu()
    return player.health
#function to see if player has enough health
def is_weight(player):
    if player.inventory.weight < 80:
        return True
    elif player.inventory.weight > 80:
        return False
    return player.inventory.weight
#Function to see if player has enough stamina
def is_stamina(player):
    if player.stamina > 20:
        return True
    elif player.stamina < 20:
        return False
    return player.stamin
#Checks if player has weapon
def is_weapon(player):
    if player.inventory.weapon == "metal rod":
        return True
    else:
        return False
#Checks is player has armour
def is_gear(player):
    if player.inventory.gear == "reinforced spacesuit":
        return True
    else:
        return False
#Count for how many crew members
def reduce_crew():
    global crew
    if crew > 0:
        crew -= 1
        print(f"There is now {crew} remaining left in your crew.")
    else:
        print("No one left in your crew.")

#------------the game starts here------------
# Starts at crater
def run_game_beginning(player):
    print(f"\nWelcome, {player.name}!")
    player.health_check()
    player.stamina_check()
    print(f"Wins: {player.wins} Loses: {player.loses}")

    print(f"\n{player.name}! Get up here! Connection has been lost with HQ back on earth! We need to make our "
          f"way back to base now!\n{player.name}, your incharge here, what should we do?\n")
    while True:
        option = input("1. Try radioing for help.\n"
                       "2. Return back to base.\n"
                       "3. Take a moment to think.\n"
                       "4. Check player stats.\n")
        if option == "1":
            path_one(player)
        elif option == "2":
            path_two(player)
        elif option == "3":
            path_three(player)
        elif option == "4":
            player_stats(player)
            continue
        else:
            print("Invalid option.")

#------------the game will now branch off into different paths------------
#Radio path
def path_one(player):
    print("All you can hear from the radio is static. They are no help. ")
    choice = input("Would you like to drop the radio? (y/n): ").lower()
    if choice == "y":
        player.inventory.weight -= 5
        print(f"Weight reduced. New total: {player.inventory.weight}")

    else:
        print("You keep the radio")
    while True:
        option = input("What should we do next?\n"
                       "1. return to base.\n"
                       "2. Take a moment to think.\n"
                       "3. Check player stats.\n")

        if option == "1":
            path_two(player)
        elif option == "2":
            path_three(player)
        elif option == "3":
            player_stats(player)
            continue
        else:
            print("Invalid option.")
#Head back to base path
def path_two(player):
    print("You and the team decide to head back to base. Along the way, you begin to hear weird noises.\n"
          "It sounds like someone is screaming. You ask you team what is that noise and they do not respond.\n"
          "What should we do next?\n")
    while True:
        option = input("1. Look around the area to see where the screaming is coming from.\n"
                       "2. continue back to base.\n"
                       "3. Check player stats.\n")
        if option == "1":
            path_four(player)
        elif option == "2":
            path_five(player)
        elif option == "3":
            player_stats(player)
            continue
        else:
            print("Invalid option.")
#Moment to think path
def path_three(player):
    print("You take a moment to think. While you were thinking, you decided the team should check the truck\n"
          "for supplies. In the truck, you find a metal rod. ")
    choice = input("Do you want to equip the metal rod? (y/n)\n ")
    if choice == "y":
        player.inventory.weight += 15
        player.inventory.weapon = "metal rod"
    print("Your team decides to start heading back to base.")
    path_two(player)
#you are attacked by monster path
def path_four(player):
    save_point(player, "path_four")
    print("A mysterious creature jumps out from a crater while your investigating!")
    if is_weapon(player):
        print("You use your metal rod and defeat the creature. You take a bit of damage and loose stamina.")
        player.health -= 10
        player.stamina -= 15
        is_alive(player)
        print(f"Your stamina is now at {player.stamina}")
    else:
        print("You have no weapons to fight back. You lose a great deal of health.")
        player.health -= 40
        is_alive(player)
    print(f"Your health is now at {player.health}")

    print("You continue onward towards base.")
    path_five(player)
#Made it back to base path
def path_five(player):
    save_point(player, "path_five")
    print("You have made it back to base. You notice that the lights are out inside the base.\n")
    while True:
        option = input("What should we do next?\n"
                       "1. Enter the base\n"
                       "2. Look around base\n"
                       "3. Check player stats.\n")
        if option == "1":
            path_six(player)
        elif option == "2":
            path_seven(player)
        elif option == "3":
            player_stats(player)
            continue
        else:
            print("Invalid option.")
#Entering the base
def path_six(player):
    save_point(player, "path_six")
    print("You and your team decides to enter the base. You notice claw marks around the door entrance.\n"
          "As you are looking, one of your crew members screams from one of the rooms.")
    while True:
        option = input("What should we do next?\n"
                       "1. Go help your teammate.\n"
                       "2. Do nothing.\n"
                       "3. Check player stats.\n")
        if option == "1":
            path_eight(player)
        if option == "2":
            path_nine(player)
        if option == "3":
            player_stats(player)
            continue
        else:
            print("Invalid option.")
#looking around the base
def path_seven(player):
    save_point(player, "path_seven")
    print("You decide to look outside around the base. While looking around, you find a reinforced spacesuit. ")
    option = input("Do you want to equip the reinforced spacesuit? (y/n)\n").strip()
    if option == "y":
        if is_weight(player) is True:
            player.inventory.weight += 30
            player.inventory.gear = "reinforced spacesuit"
            print(f" player weight is now {player.inventory.weight}")
        elif is_weight(player) is False:
            print("You do not have enough room!")
    print("Your team decides to enter the base.")
    path_six(player)
#You help your teammate screaming (death with no armour)
def path_eight(player):
    save_point(player, "path_eight")
    print("You help your crewmate escape, but the creature grabs you instead as your crew runs off.")
    if player.inventory.gear == "reinforced spacesuit":
        player.health -= 60
        is_alive(player)
        print(f"You take a lot of damage, but manager to walk away alive.\n Your health is now at {player.health}")
        path_ten(player)
    else:
        player.health -= 100
        is_alive(player)
#Staying inside base and not helping crew
def path_nine(player):
    save_point(player, "path_nine")
    print("The screams from your crewmate die down. There was nothing you could do to help him.\n"
          "You can hear the creature start to run towards the main room you are in.")
    reduce_crew()
    while True:
        option = input("What should we do next?\n"
                       "1. Fight back.\n"
                       "2. Run away.\n"
                       "3. Find a place to hide.\n"
                       "4. Check player stats.\n")
        if option == "1":
            path_eleven(player)
        if option == "2":
            path_twelve(player)
        if option == "3":
            path_thirteen(player)
        if option == "4":
            player_stats(player)
            continue
        else:
            print("Invalid option.")
#Look around base for power source Chance option
def path_ten(player):
    save_point(player, "path_ten")
    print("You look around the base and find a power source. You try to turn the power source on.")
    chance = random.randint(1,2)
    if chance == 1:
        print("It worked! The power is on!")
        path_fourteen(player)
    if chance == 2:
        print("Nuts! The power does not work")
        while True:
            option = input("What should we do next?\n"
                           "1. Look around for a power reserve.\n"
                           "2. Figure out what went wrong.\n"
                           "3. Check player stats.")
            if option == "1":
                path_sixteen(player)
            elif option == "2":
                path_fifteen(player)
            elif option == "3":
                player_stats(player)
            else:
                print("Invalid option.")
#Fight back creature
def path_eleven(player):
    save_point(player, "path_eleven")
    if is_weight(player) is True and is_weapon(player) is True:
        print(f"You use your {player.inventory.weapon} and {player.inventory.gear} gear. and easily fight off the creature.")
        player.health -= 10
    elif player.inventory.gear is True:
        print(f"You use your {player.inventory.gear} for protection, but take damage.")
        player.health -= 30
    elif player.inventory.weapon is True:
        print(f"You use your {player.inventory.weapon} to attack, but take damage.")
        player.health -= 40
    print(f"your health is now {player.health}.")
    is_alive(player)
    path_ten(player)
#Run away from creature
def path_twelve(player):
    save_point(player, "path_twelve")
    print("You run away from the creature but he claws your back as you run away.")
    if player.inventory.gear is True:
        player.health -= 20
    else:
        player.health -= 40

    print(f"your health is now {player.health}.")
    path_ten(player)
#Hide from creature
def path_thirteen(player):
    save_point(player, "path_thirteen")
    print("You hide from the creature in another room. The creature decides to go into another room finding two of "
          "your crew members.")
    reduce_crew()
    reduce_crew()
    path_ten(player)
#Radio HQ -- GOING HOME
def path_fourteen(player):
    save_point(player, "path_fourteen")
    print("You have successfully turned on the power. You radioed HQ and they are sending a rescue ship on the way.")
    player.wins += 1
    main_menu()
#Figure out what went wrong.
def path_fifteen(player):
    save_point(player, "path_fifteen")
    print("Your crew scans the power box. You see it blew a fuse.")
    if crew > 5:
        print("Luckily someone in your crew knows how to fix it. After a while, he is able to fix it.")
        path_fourteen(player)
    else:
        print("Luckily, Terry in your crew knows how to fix it.\n"
              "Unluckily, Terry was killed by the creature.\n"
              "You now must look for the power reserve.")
        path_sixteen(player)
#Look for power reserve, then go home
def path_sixteen(player):
    save_point(player, "path_sixteen")
    print("You look around for the power reserve. You find it, but as you are turning on the power, you get shocked.")
    if player.inventory.gear is True:
        player.health -= 20
    elif player.inventory.power is False:
        player.health -= 40
    is_alive(player)
    print(f"Your health is now {player.health}.")
    path_fourteen(player)
main_menu()