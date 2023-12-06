###########
# MOD LOG
###########
# 12/2
# This file is not being used for recent chapter requirements
# added "type: ignore" to read_player_data()
# Lineup class unknown because it is commented out in objects.py

import csv
from objects import Lineup, Player

# assigning a variable to the file name for easy use
FILENAME = "baseball_mgr.csv"

# def write_player_data(lineup):
#     try:
#         with open(FILENAME, "w", encoding='utf8', newline="") as file:
#             writer = csv.writer(file)
#             for dictionary in lineup:
#                 writer.writerow(dictionary.values())  
#     except FileNotFoundError:
#         print("Could not find the file named ", FILENAME)
#     except OSError:
#         print("File found - Error writing to the file")
#     except Exception:
#         print("An unexpected error occurred writing to the file.")

def write_player_data(lineup):
    rows = []
    try:
        for player in lineup:
            row = []
            # row.update({"fname": player.fname})
            # row.update({"lname": player.lname})
            # row.update({"pos": player.pos})
            # row.update({"ab": player.ab})
            # row.update({"hits": player.hits})
            # row.update({"avg": player.avg})
            row.append(player.fname)
            row.append(player.lname)
            row.append(player.pos)
            row.append(player.ab)
            row.append(player.hits)
            row.append(player.avg)
            rows.append(row)

        with open(FILENAME, 'w', encoding='utf8', newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
            # for player in rows:
            #     writer.writerow(player.values())

    except FileNotFoundError:
        print("Could not find the file named ", FILENAME)
    except OSError:
        print("File found - Error writing to the file")
    except Exception:
        print("An unexpected error occurred writing to the file.")


def read_player_data():
    lineup = Lineup() 
    try: 
        with open(FILENAME, newline="") as file:
            for row in csv.reader(file):
                player = Player(row[0], row[1], row[2], int(row[3]), int(row[4]), float(row[5])) # type: ignore
                lineup.addPlayer(player)
            return lineup        
    except FileNotFoundError:
        print("Team data file could not be found.\nA new file will be created.")
        new_file = open(FILENAME, "w")
        new_file.close()
        return lineup
    except OSError:
        print("Error in reading the file. Please try again.")

# def read_player_data():
#     players = []
#     try: 
#         with open(FILENAME, "r", newline="") as file:
#             for row in csv.reader(file):
#                 player = {}
#                 player.update({'name': row[0]})
#                 player.update({'pos': row[1]})
#                 player.update({'ab': row[2]})
#                 player.update({'hits': row[3]})
#                 player.update({'avg': row[4]})
#                 players.append(player)
#             return players        
#     except FileNotFoundError:
#         print("Team data file could not be found.\nA new file will be created.")
#         players = []
#         new_file = open(FILENAME, "w")
#         new_file.close()
#         return players
#     except OSError:
#         print("Error in reading the file. Please try again.")