###########
# MOD LOG
###########
# 10/4/2023
# Began code edit for 'chapter 10' guidelines
# replaced string concat of tuple items for a join function, adding a comma through the loop of items
# replaced tabs with format specs in def display_lineup
#
# 10/8/2023
# Began Chapter 11 - Getting the dates
#
# 10/9
# Began object-oriented approach -- Established ui.py/objects.py/db.py
# Failed -- backtrack to Dictionaries
#
# 10/10
# Instantiated Dictionary in read_player_data, inserted dict through .update method
# Initial makeover starts in add_player, where this will ultimately test whether the csv file is being read/written correctly
#
# 10/19
# Completed reading/writing data to a list of dictionaries
# Altered write_player_data to take values from add_player only.
# read_player_data takes each value in a record and updates dictionary to its correct key/value pair
# removed all indices from ui.py and replaced with matching keys/values
# Began creating Player class in objects.py
#



# I just like the tuple to be at the tippy top
POSITIONS = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")
# From there I code a global import for the read and write functions
from db import write_player_data, read_player_data
from objects import Player, Lineup
from datetime import date, datetime 

def get_game_date():
    while True:
        game_date_str = input(f"{'GAME DATE:':17}")   
        if game_date_str == "":
            break
        try:
            dt = datetime.strptime(game_date_str, "%Y-%m-%d")
        except ValueError:
            print("Incorrect date format. Please try again.")
            continue

        # create date objects
        game_date = date(dt.year, dt.month, dt.day)
        current_date = date.today()
        future_game = (game_date - current_date).days

        # check if date object is today or earlier
        if future_game > 0:
            print(f"DAYS UNTIL GAME: {future_game}")
            return game_date
        else:
            print(f"DAYS UNTIL GAME:")
            break

# function validates name being only of string type and greater than 0 and less than/equal to 20
def validate_fname():
    while True:
        fname = input("First name: ")
        if any(char.isdigit() for char in fname):                    # if any char in the name is a digit, using a for loop, throw a flag
            print("Please do not include digits in your name.")
        elif len(fname) <= 0 or len(fname) >= 40:                     # or if name has 0 char or over 20 char, throw the flag
            print("Please keep your name between 1-40 characters")
        else: 
            return fname
        
def validate_lname():
    while True:
        lname = input("Last name: ")
        if any(char.isdigit() for char in lname):                    # if any char in the name is a digit, using a for loop, throw a flag
            print("Please do not include digits in your name.")
        elif len(lname) <= 0 or len(lname) >= 40:                     # or if name has 0 char or over 20 char, throw the flag
            print("Please keep your name between 1-40 characters")
        else: 
            return lname

# function validates the lineup number
def validate_lineup(prompt, high):
    while True:
        try:
            number = int(input(prompt))
            if number < 1 or number > high:
                print("*ERROR*. Choose a valid lineup number or select * option 1 * to view the lineup.")
                continue
            else:
                return number
        except ValueError as e:
            print(type(e), "The lineup number must be a positive integer. Please try again.")
        
# function validates correct position from POSITIONS
def validate_pos():
    while True:
        pos = input("Position: ")
        for i in POSITIONS:         # for every item in tuple, if input equals an item, return it
            if pos.upper() == i:
                return pos.upper()            
        print("Invalid position. Try again.")
        print("POSITIONS")
        print(POSITIONS)

# function to validate at bats
def validate_ab():
    while True:
        try:
            number = int(input("At bats: "))
            if number >= 0 and number <= 10000:
                return number
            else:
                print("At bats must be greater than 0 and less than or equal to 10,000. Please try again.")
        except ValueError as e:
            print(type(e), "'At bats' must be a positive integer greater than 0 and less than or equal to 10,000. Please try again.")
            
# function to validate hits
def validate_hit(high):            # This function is the same as 'validate_ab' just with a different message
    while True:
        try:
            number = int(input("Hits: "))
            if number >= 0 and number <= high:
                return number
            else:
                print("Hits must be greater than or equal to 0 and less than or equal to the value of 'At bats'. Please try again.")

        except ValueError as e:
            print(type(e), "'Hits' must be a positive integer greater than 0 and less than or equal to the value of 'At bats'. Please try again.")

# function adds player
def add_player(lineup):
    fname = validate_fname()
    lname = validate_lname()
    pos = validate_pos()
    ab = validate_ab()
    hits = validate_hit(ab)
    avg = Player().getBattingAvg(hits, ab)
    player = Player(fname, lname, pos, ab, hits, avg)
    lineup.addPlayer(player)               # Receives all validated values and throws them into 1 dictionary
    write_player_data(lineup)                                  # Write each appended list of dictionaries to the .csv file
    print(f"{player} was added.")

# function moves player index on the list
def move_player(lineup):
    current_lineup = validate_lineup("Enter the lineup number you want to move: ", lineup.count)
    current_player = lineup.getPlayer(current_lineup)
    print(f"{current_player} was selected.")                               # uses input as the 'list' index to display the name
    new_lineup = validate_lineup("Enter the new lineup number: ", lineup.count)
    lineup.movePlayer(current_lineup, new_lineup)                          # insert the current lineup 'list item' into the new index         
    write_player_data(lineup)
    new_player = lineup.getPlayer(new_lineup)
    print(f"{new_player} was moved successfully.")       

# function removes player
def del_player(lineup):
    lineup_no = validate_lineup("Enter the lineup number you want to remove: ", lineup.count)
    player = lineup.getPlayer(lineup_no)
    lineup.removePlayer(player)
    write_player_data(lineup)
    print(f"{player} was removed")

# function edits player stats
def edit_player_stats(lineup):
    lineup_no = validate_lineup("Enter the lineup number you want to edit [Stats]: ", lineup.count)
    player = lineup.getPlayer(lineup_no)
    print(f"You selected {player} AB=[{player.ab}] H=[{player.hits}]")
    new_ab = validate_ab()
    new_hits = validate_hit(new_ab)
    new_avg = Player().getBattingAvg(new_hits, new_ab)
    lineup.editPlayerStats(player, new_ab, new_hits, new_avg)
    write_player_data(lineup)
    print(f"{player.fname}'s stats were updated.")

# function edits player position
def edit_player_pos(lineup):
    lineup_no = validate_lineup("Enter the lineup number you want to edit [Position]: ", lineup.count)
    player = lineup.getPlayer(lineup_no)
    print(f"{player} was selected. Current position: {player.pos}")    
    new_pos = validate_pos()
    lineup.editPlayerPos(player, new_pos)
    write_player_data(lineup)
    print(f"{player.fname}'s position was updated.")

# function displays lineup
def display_lineup(lineup):
    print(f"{'Player':>10} {'POS':>26} {'AB':>8} {'H':>8} {'AVG':>8}")
    print("-" * 64)      
    if lineup is None or lineup.count == 0:        # "If PLAYERS is None" prevents the program from crashing if .csv file is newly created. 
        print("No players added. Please select * option 2 * to add players to the lineup.")
    else:
        for i, player in enumerate(lineup, start=1):
            print(f"{i:<4}{str(player):<30}{player.pos:<6}{player.ab:>6}{player.hits:>9}{player.avg:>9}")
                
    
def display_title():
    print("=" * 64)
    print("Baseball Team Manager".center(64))
    print()
    print(f"{'CURRENT DATE:':16} {date.today()}")
    get_game_date()
    print()
    print()
    print("MENU OPTIONS")
    print("1 - Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Move player")
    print("5 - Edit player position")
    print("6 - Edit player stats")
    print("7 - Exit program")
    print()
    print("POSITIONS")
    items = ', '.join(str(item) for item in POSITIONS)
    print(items)
    print("=" * 64)

def display_menu(): 
    print()
    print("MENU OPTIONS")
    print("1 - Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Move player")
    print("5 - Edit player position")
    print("6 - Edit player stats")
    print("7 - Exit program")
    print()

def main():
    display_title()
    data = read_player_data()
    while True:
        try:
            option = int(input("Menu option: "))
            if option == 1:
                display_lineup(data)
            elif option == 2:
                add_player(data)
            elif option == 3:
                del_player(data)
            elif option == 4:
                move_player(data)
            elif option == 5:
                edit_player_pos(data)
            elif option == 6:
                edit_player_stats(data)
            elif option == 7:
                break
            else:
                print("Not a valid option. Please try again.")
        except ValueError:
            print("Not a valid option. Please enter a number displayed on the list.")
            display_menu()
   
    print("Bye!")

if __name__ == "__main__":
    main()
