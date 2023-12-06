from dataclasses import dataclass
import tkinter as tk
from tkinter import Tk, ttk, messagebox
import sqldb

############
# MOD LOG -- SQLITE detail
# add class = Position
# add attributes to class_Player = playerID | batOrder
# Commented class Lineup
# Created class PlayerEditFrame
############

@dataclass
class Position:
    positionID: int = 0
    position: str = ""

@dataclass
class Player:
    playerID: int = 0
    batOrder: int = 0
    fname: str = ""
    lname: str = ""
    pos: str = ""
    ab: int = 0
    hits: int = 0

    def __str__(self):
        return f"{self.fname} {self.lname}"
    
    def getBattingAvg(self):
        return round(self.hits / self.ab, 3)
    
class PlayerEditFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        self.player = Player()
        self.message = ""
        self.pack()

        self.batOrder = tk.StringVar()
        self.fname = tk.StringVar()
        self.lname = tk.StringVar()
        self.pos = tk.StringVar()
        self.ab = tk.StringVar()
        self.hits = tk.StringVar()
        self.avg = tk.StringVar()

        ttk.Label(self, text="Player ID:").grid(column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=27, textvariable=self.batOrder).grid(column=1, row=0)
        ttk.Button(self, text="Get Player", command=self.grab_player).grid(column=2, row=0)

        ttk.Label(self, text="First name:").grid(column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=27, textvariable=self.fname).grid(column=1, row=1)

        ttk.Label(self, text="Last name:").grid(column=0, row=2, sticky=tk.E)
        ttk.Entry(self, width=27, textvariable=self.lname).grid(column=1, row=2)

        ttk.Label(self, text="Position:").grid(column=0, row=3, sticky=tk.E)
        ttk.Entry(self, width=27, textvariable=self.pos).grid(column=1, row=3)

        ttk.Label(self, text="At bats:").grid(column=0, row=4, sticky=tk.E)
        ttk.Entry(self, width=27, textvariable=self.ab).grid(column=1, row=4)

        ttk.Label(self, text="Hits:").grid(column=0, row=5, sticky=tk.E)
        ttk.Entry(self, width=27, textvariable=self.hits).grid(column=1, row=5)

        ttk.Label(self, text="Batting Avg:").grid(column=0, row=6, sticky=tk.E)
        ttk.Entry(self, width=27, textvariable=self.avg, state="readonly").grid(column=1, row=6)

        ttk.Button(self, text="Save Changes", command=self.save).grid(column=1, row=7, sticky=tk.W)
        ttk.Button(self, text="Cancel", command=self.reset).grid(column=1, row=7, sticky=tk.E)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=2)

    def get_int(self, val, fieldName):
        try:
            return int(val)
        except ValueError:
            self.message += f"{fieldName} must be a valid whole number.\n"

    def get_pos(self, val):
        pos_list = sqldb.get_positions()
        pos = val
        for x in pos_list:
            if pos.upper() == x.position:
                return pos.upper()
            
    def clear_entries(self):
        self.batOrder.set("")
        self.fname.set("")
        self.lname.set("")
        self.pos.set("")
        self.ab.set("")
        self.hits.set("")
        self.avg.set("")

    def grab_player(self):
        player_list = sqldb.get_players()
        self.message = ""
        self.player.batOrder = self.get_int(self.batOrder.get(), "Player ID") # type: ignore

        if self.message != "":
            messagebox.showerror("Error", self.message)
            self.clear_entries()
        elif self.player.batOrder < 1 or self.player.batOrder > len(player_list): # type: ignore
            messagebox.showerror("Error", f"Player ID ( {self.player.batOrder} ) doesn't exist.")  
            self.clear_entries() 
        else:
            player = sqldb.get_player(self.player.batOrder)
            self.fname.set(player.fname) # type: ignore
            self.lname.set(player.lname) # type: ignore
            self.pos.set(player.pos) # type: ignore
            self.ab.set(str(player.ab)) # type: ignore
            self.hits.set(str(player.hits)) # type: ignore
            self.avg.set(str(player.getBattingAvg())) # type: ignore
        return self.player.batOrder

    def save(self):
        pos = self.get_pos(self.pos.get())
        if pos == None:
            self.pos.set("")
        else:
            player = Player(fname=self.fname.get(), lname=self.lname.get(), pos=pos, ab=int(self.ab.get()), hits=int(self.hits.get()), batOrder=int(self.batOrder.get()))
            sqldb.update_player_data(player)
            self.clear_entries()
         

    def reset(self):
        if messagebox.askokcancel("Cancel", "Cancel all unsaved changes?"):
            current_player = int(self.player.batOrder)
            db_data = sqldb.get_player(current_player)
            self.batOrder.set(str(db_data.batOrder)) # type: ignore
            self.fname.set(db_data.fname) # type: ignore
            self.lname.set(db_data.lname) # type: ignore
            self.pos.set(db_data.pos) # type: ignore
            self.ab.set(str(db_data.ab)) # type: ignore
            self.hits.set(str(db_data.hits)) # type: ignore

def exit():
    if messagebox.askyesno("Exit", "Do you want to quit the application?"):
        sqldb.close()
        root.destroy()   

if __name__ == '__main__':
    sqldb.connect()
    root = tk.Tk()
    root.title("Player")
    PlayerEditFrame(root)
    root.protocol("WM_DELETE_WINDOW", exit)
    root.mainloop() 

# class Lineup:
#     def __init__(self):
#         self.__list = []

#     def __iter__(self):
#         for player in self.__list:
#             yield player

#     # function adds player
#     def addPlayer(self, player):
#         self.__list.append(player)
      
#     # function removes player
#     def removePlayer(self, player):
#         self.__list.remove(player)

#     # function moves player index on the list
#     def movePlayer(self, current, new):
#         self.__list.insert(new - 1, self.__list.pop(current - 1))   

#     # function gets the index of the player
#     def getPlayer(self, number):
#         index = number - 1
#         return self.__list[index]   

    # function sets new stats to the Player_object attr's
    # def editPlayerStats(self, player, ab, hits, avg):
    #     player.ab = ab
    #     player.hits = hits
    #     player.avg = avg
        
#     # function sets new pos to the Player_object attr
#     def editPlayerPos(self, player, pos):
#         player.pos = pos        

#     @property
#     def count(self):
#         return len(self.__list)
