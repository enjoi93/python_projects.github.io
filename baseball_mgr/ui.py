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
# ### GAP in mod log
# Failed to keep updates on my road to learning class structures and instantiating objects
# - I did manage to learn how to apply the KISS method when creating class methods/properties
#
# 11/7
# * The fun begins
# Begin replacement of .csv file to SQLite DB
# Disconnect DB.PY | Connect SQLDB.PY
#
# 11/12
# Established add_player() as "functional"
#  --- I created a Player object to be submitted to the sqliteDB. The -batOrder- integer is standalone 
#  --- based on length of list returned from -get_players()- (sqldb.py)
#
# 11/16
# General update:
# Added -update_batting_order()- to -add_player()- & -del_player()- || updating the batting order on each entry keeps the program from losing track of the batting order mid-session
# --- add/delete/display/edit/update players all functional
# --- Begin adaptation of 'POSITION' table into validation
# Removed POSITION tuple. Program relies on sqldb table to validate and display correct position abbreviations
# Updated -validate_pos()- with sqldb method in order to validate
# Added -get_positions()- (sqldb.py) to -display_title()- (ui.py)
# Begin implementing a GUI as the final step
#
# 11/18
# GUI success
# --- GUI runs in objects.py
#
# 12/2
# Final draft review --
# -- Updating comments
# -- Established "commented out code" to demonstrate previous chapter requirements only
# -- introduced "type: ignore" to all values affected by the connection string bug (connection is not established unless program is running, therefore sees all related values as type "None")



import sqldb
from objects import Player
from datetime import date, datetime

# function accepts a date value and displays a counter from today's date to game date
def get_game_date():
    while True:
        game_date_str = input(f"{'GAME DATE:':17}")   
        if game_date_str == "":
            break
        try:
            dt = datetime.strptime(game_date_str, "%Y-%m-%d")
        except ValueError:
            print('Incorrect date format. Try entering the date in "YYYY-MM-DD" format.')
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

# function validates name being only of string type and greater than 0 and less than/equal to 40
def validate_fname():
    while True:
        fname = input("First name: ")
        if any(char.isdigit() for char in fname):
            print("Please do not include digits in your name.")
        elif len(fname) <= 0 or len(fname) >= 40:         
            print("Please keep your name between 1-40 characters")
        else: 
            return fname
        
def validate_lname():
    while True:
        lname = input("Last name: ")
        if any(char.isdigit() for char in lname):                  
            print("Please do not include digits in your name.")
        elif len(lname) <= 0 or len(lname) >= 40:                  
            print("Please keep your name between 1-40 characters")
        else: 
            return lname

# function validates the lineup number from length of Player table in sqldb.py
def validate_lineup(prompt):
    player_list = sqldb.get_players()
    while True:
        try:
            number = int(input(prompt))
            if number < 1 or number > len(player_list):
                print("*ERROR*. Choose a valid lineup number or select * option 1 * to view the lineup.")
                continue
            else:
                return number
        except ValueError as e:
            print(type(e), "The lineup number must be a positive integer. Please try again.")
        
# function validates correct position from Position table in sqldb.py
def validate_pos():
    pos_list = sqldb.get_positions()
    while True:
        pos = input("Position: ")
        for x in pos_list:
            if pos.upper() == x.position:
                return pos.upper()            
        print("Invalid position. Try again.")
        print("POSITIONS")
        items = ', '.join(f"{pos.position}" for pos in pos_list)
        print(f"({items})")

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
def validate_hit(high):           
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
def add_player():
    fname = validate_fname()
    lname = validate_lname()
    pos = validate_pos()
    ab = validate_ab()
    hits = validate_hit(ab)

    player_list = sqldb.get_players()
    player = Player(batOrder=len(player_list) + 1, fname=fname, lname=lname, pos=pos, ab=ab, hits=hits)
    sqldb.add_player(player)
    sqldb.update_batting_order() 
    print(f"{fname} {lname} was added.")

# function removes player
def del_player():
    lineup_no = validate_lineup("Enter the lineup number you want to remove: ")
    player = sqldb.get_player(lineup_no)
    sqldb.delete_player(lineup_no)
    sqldb.update_batting_order()
    print(f"{player.fname} {player.lname} was removed") # type: ignore

# THREE FUNCTIONS COMMENTED OUT. USED FOR db.py
# --------------------------------------------------------> 
# # function moves player index on the list
# def move_player():
#     current_lineup = validate_lineup("Enter the lineup number you want to move: ")  
#     current_player = lineup.getPlayer(current_lineup)
#     print(f"{current_player} was selected.")                            
#     new_lineup = validate_lineup("Enter the new lineup number: ")
#     lineup.movePlayer(current_lineup, new_lineup)                              
#     write_player_data(lineup)
#     new_player = lineup.getPlayer(new_lineup)
#     print(f"{new_player} was moved successfully.")       

# # function edits player stats
# def edit_player_stats(lineup):
#     lineup_no = validate_lineup("Enter the lineup number you want to edit [Stats]: ")
#     player = lineup.getPlayer(lineup_no)
#     print(f"You selected {player} AB=[{player.ab}] H=[{player.hits}]")
#     new_ab = validate_ab()
#     new_hits = validate_hit(new_ab)
#     new_avg = Player().getBattingAvg(new_hits, new_ab)
#     lineup.editPlayerStats(player, new_ab, new_hits, new_avg)
#     write_player_data(lineup)
#     print(f"{player.fname}'s stats were updated.")

# # function edits player position
# def edit_player_pos(lineup):
#     lineup_no = validate_lineup("Enter the lineup number you want to edit [Position]: ", lineup.count)
#     player = lineup.getPlayer(lineup_no)
#     print(f"{player} was selected. Current position: {player.pos}")    
#     new_pos = validate_pos()
#     lineup.editPlayerPos(player, new_pos)
#     write_player_data(lineup)
#     print(f"{player.fname}'s position was updated.")

# function edits player position, at bats, and hits. Takes new values and creates a new Player object replacing the older object
def edit_player_details():
    lineup_no = validate_lineup("Enter the lineup number you want to edit: ")
    player = sqldb.get_player(lineup_no)
    print(f"{player.fname} {player.lname} has been selected. Position: [{player.pos}] || At Bats: [{player.ab}] || Hits: [{player.hits}]") # type: ignore
    print()
    new_pos = validate_pos()
    new_ab = validate_ab()
    new_hit = validate_hit(new_ab)
    player_details = Player(fname=player.fname, lname=player.lname, pos=new_pos, ab=new_ab, hits=new_hit, batOrder=lineup_no) # type: ignore
    sqldb.update_player_data(player_details)
    print(f"{player.fname} {player.lname} has been updated.") # type: ignore

# function creates the lineup format
def lineup_format(lineup):
    print(f"{'Player':>10} {'POS':>26} {'AB':>8} {'H':>8} {'AVG':>8}")
    print("-" * 64)      
    if lineup is None or len(lineup) == 0:
        print("No players added. Please select * option 2 * to add players to the lineup.")
    else:            
        for player in lineup:
            print(f"{player.batOrder:<4}{str(player):<30}{player.pos:<6}{player.ab:>6}{player.hits:>9}{player.getBattingAvg():>9}")

# function displays lineup
def display_lineup():
    lineup = sqldb.get_players()
    lineup_format(lineup)
   
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
    print("4 - Edit player position/stats")
    print("5 - Exit program")
    print()
    print("POSITIONS")
    pos_list = sqldb.get_positions()
    items = ', '.join(f"{pos.position}" for pos in pos_list)
    print(items)
    print("=" * 64)

def display_menu(): 
    print()
    print("MENU OPTIONS")
    print("1 - Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Edit player position/stats")
    print("5 - Exit program")
    print()

def main():
    sqldb.connect()
    display_title()
    while True:
        try:
            option = int(input("Menu option: "))
            if option == 1:
                display_lineup()
            elif option == 2:
                add_player()
            elif option == 3:
                del_player()
            elif option == 4:
                edit_player_details()
            elif option == 5:
                break
            else:
                print("Not a valid option. Please try again.")
                display_menu()
        except ValueError:
            print("Not a valid option. Please enter a number displayed on the list.")
            display_menu()
   
    sqldb.close()
    print("Bye!") 

if __name__ == "__main__":
    main() 
