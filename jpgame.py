import json  # Importing the JSON module for reading and writing JSON data
import time  # Importing the Time module for time-related functions
import sys   # Importing the System module for system-specific parameters and functions
import os
import threading
# import atexit
from pypresence import Presence #Rich Presence
import pypresence.exceptions
from threading import Thread
# import signal # pour éviter de perdre le total time quand on ferme avec la croix
import win32api

try:
    start_time = int(time.time())
    client_id = "1235640528364900452"  # Rich Presence client ID
    RPC= Presence(client_id)
    RPC.connect()
    RPC.update(
            details = "jpgame.py",
            start = start_time,
            large_image = "1",
            large_text = "JLG"    
                    )

    def parallel_function():
        while True:
            RPC.update(
                details = "jpgame.py",
                start = start_time,
                large_image = "1",
                large_text = "JLG"    
                    )
            time.sleep(6)

    parallel_thread = threading.Thread(target=parallel_function)
    parallel_thread.daemon = True  # Set as daemon so it will terminate when the main program terminates
    parallel_thread.start()
except pypresence.exceptions.DiscordNotFound:
    print("Can't connect to Discord.")
    time.sleep(2)

class JapaneseLearningGame:  # Defining a class named JapaneseLearningGame


    def __init__(self):  # Initializing the class with constructor method
        # Initializing attributes for the game
        self.progress = 0  # Total progress in the game
        self.level = 0      # Current level of the player
        self.xp = 0         # Experience points of the player
        self.badges = []    # List of badges earned by the player
        self.streak = 0     # Streak count for daily goals
        self.daily_goal = 5  # Number of Anki cards to complete daily
        self.currency = 0   # Currency earned by the player
        self.total_cards = 0  # Total number of Anki cards completed
        self.total_time = 0   # Total time spent in the game
        self.load_progress()  # Loading saved progress when initializing the game
        self.initialize_game()  # Initializing the game state
        self.start_time = int(time.time()) - self.total_time  # Starting time of the game
        print("1 lvl = " + str(self.level))
        print("Initializing...")
        

    def load_progress(self):  # Method to load player's progress from a file
        try:
            with open('progress.txt', 'r') as file:  # Opening the progress file in read mode
                data = json.load(file)  # Loading data from the file
                # Assigning loaded data to corresponding attributes or default values if not found
                self.progress = data.get('progress', 0)
                self.level = data.get('level', 0)
                self.xp = data.get('xp', 0)
                self.badges = data.get('badges', [])
                self.streak = data.get('streak', 0)
                self.currency = data.get('currency', 0)
                self.total_cards = data.get('total_cards', 0)
                self.total_time = data.get('total_time', 0)
                print("2 lvl = " + str(self.level))
                print("Loading progress...")
        
        except FileNotFoundError:  # Handling file not found error
            pass

    def save_progress(self):  # Method to save player's progress to a file
        # Creating a dictionary containing player's progress data
        data = {
            'progress': self.progress,
            'level': self.level,
            'xp': self.xp,
            'badges': self.badges,
            'streak': self.streak,
            'currency': self.currency,
            'total_cards': self.total_cards,
            'total_time': self.total_time
        }
        with open('progress.txt', 'w') as file:  # Opening the progress file in write mode
            json.dump(data, file)  # Writing data to the file in JSON format


    def complete_anki_cards(self, num_cards):  # Method to complete Anki cards and update progress
        self.progress += num_cards  # Incrementing progress by the number of completed Anki cards
        self.total_cards += num_cards  # Incrementing total cards completed
        self.xp += 100 * num_cards  # Incrementing XP based on completed cards
        self.total_time += int(time.time()) - self.start_time
        self.check_level_up()  # Checking if the player has leveled up
        self.check_daily_goal()  # Checking if the daily goal has been met
        self.save_progress()  # Saving progress after completion
        print("Completing Anki Cards...")

    def earn_badge(self, badge):  # Method to earn a badge
        self.total_time += int(time.time()) - self.start_time      
        self.badges.append(badge)  # Adding the earned badge to the list
        self.save_progress()  # Saving progress after earning badge
        print("Earning badge...")

    def level_up(self):  # Method to level up the player
     remaining_exp = max(0, self.xp - self.xp_required_for_level(self.level))  # Calculate remaining experience
     self.level += 1  # Incrementing the player's level
     if remaining_exp > 0:  # If there's remaining experience, add it to the next level
        self.xp = remaining_exp  # Set current experience to remaining experience
        print(f"\nCongratulations! You've reached Level {self.level}!")  # Printing level up message
        print(f"{remaining_exp} experience points carried over to Level {self.level + 1}")  # Printing carried over experience
     else:
        self.xp = 0  # Resetting XP to 0 if no remaining experience
        print(f"\nCongratulations! You've reached Level {self.level}!")  # Printing level up message
     self.save_progress()  # Saving progress after leveling up


    def xp_required_for_level(self, level):  # Method to calculate XP required for a level
        if level == 0:
            return 1000
        else:
            return level * 1000 + 1000  # Experience required for each level is equal to the level number * 1000

    def check_level_up(self):  # Method to check if the player has leveled up
        while self.xp >= self.xp_required_for_level(self.level):  # Checking if XP is enough for next level
            self.level_up()  # Leveling up if XP is sufficient
            print("Leveling up...")


    def check_daily_goal(self):  # Method to check if daily goal has been met
        self.streak += 1  # Incrementing daily goal streak count
        if self.streak >= self.daily_goal:  # Checking if streak count equals daily goal
            print("\nCongratulations! You've completed your daily goal!")  # Printing daily goal completion message
            self.streak = 0  # Resetting streak count
            self.currency += 1  # Incrementing currency for completing daily goal
            self.save_progress()  # Saving progress after completing daily goal
            print("Updating daily goal...")

    def initialize_game(self):  # Method to initialize the game state
        while self.xp >= self.xp_required_for_level(self.level + 1):  # Checking if XP is enough for next level
            self.level_up()  # Leveling up until XP is not enough for next level
            ("Processing leveling up function during initialization...")

    def reset_data(self):  # Method to reset all progress data
        confirmation = input("Are you sure you want to reset all data? This action cannot be undone. (yes/no): ")
        if confirmation.lower() == "yes":  # Checking if player confirms data reset
            # Resetting all progress attributes to their initial values
            self.progress = 0
            self.level = 0
            self.xp = 0
            self.badges = []
            self.streak = 0
            self.currency = 0
            self.total_cards = 0
            self.total_time = 0
            self.start_time = int(time.time())
            self.save_progress()  # Saving progress after data reset
            print("Resetting data...")
            print("All data has been reset.")  # Printing data reset confirmation message
            print("5 lvl = " + str(self.level))
        else:
            print("Data reset cancelled.")  # Printing data reset cancellation message

    def show_progress(self):  # Method to display player's progress
        # Printing game header and player's progress information
        os.system("cls")
        total_length = 150

        progress_bar = "#" * int((self.xp / (self.xp_required_for_level(self.level)) * 20))    

        self.total_time += (int(time.time()) - self.start_time - self.total_time)
        
        self.save_progress()
        
        hours = self.total_time // 3600
        minutes = (self.total_time % 3600) // 60
        seconds = self.total_time % 60

        left_texts = [
        "=" * 60,
        " " * 20 + "Japanese Learning Game",
        "=" * 60,
        "",
        "Level:".ljust(20) + str(self.level),
        "XP:".ljust(20) + str(self.xp) + " / " + str(self.xp_required_for_level(self.level)),
        "Progress:".ljust(20) + "[" + str(progress_bar.ljust(20)) + "]" + "{:.2f}%".format((self.xp / self.xp_required_for_level(self.level)) * 100),
        "Total Anki Cards Completed:".ljust(20) + " " + str(self.total_cards),
        "Total Time Spent:".ljust(20) + f"{hours} hours, {minutes} minutes, {seconds} seconds", 
        "Badges Earned:".ljust(20) + ", ".join(self.badges),
        "",
        "",
        "",
        "1. Complete Anki Cards",
        "2. Earn Badge",
        "3. Reset Data",
        "4. Exit",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "=" * 60,
        " " * 20 + "Japanese Learning Game",
        "=" * 60,   
        ]
        
        with open("ascii-art.txt", encoding="utf8") as f:
            right_texts = f.read().splitlines() # Just put the ascii art in ascii-art.txt and this line will split each line of the txt
            t=0
            len_margin = len(f.readline())
            len_ascii = len(right_texts)
            while len_ascii < 32 : # Ensuring that the ascii art has enough lines to not disrupt terminal print
                right_texts.insert(0, " "*len_margin) # Add top margin
                right_texts.append(" "*len_margin) # Add bottom margin
                len_ascii+=2

        for left_text, right_text in zip(left_texts, right_texts):
            space_count = total_length - len(str(left_text)) - len(str(right_text))

            # Construct the final string with the desired length
            final_string = str(left_text) + " " * space_count + str(right_text)
    
            print(final_string)

    def play(self):
        while True:
            self.show_progress()
            choice = input("か => ")
            if choice == '1':
                num_cards = int(input("Enter the number of Anki cards completed: "))
                self.complete_anki_cards(num_cards)
            elif choice == '2':
                badge_name = input("Enter badge name: ")
                self.earn_badge(badge_name)
            elif choice == '3':
                self.reset_data()
            elif choice == '4':
                print("Program Credits: Misudashi. Help for programming : Aidyn.")
                self.show_progress()
                os.system("cls")
                sys.exit()
            else:
                print("Invalid choice. Please enter a valid option.")
                self.show_progress()
            # self.show_progress()
    

JapaneseLearningGame().play()  # Starting the game