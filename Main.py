import tkinter as tk
from tkinter import *
import Game
import Settings



def getFrameWidth(frame):
    width = frame.winfo_width()
    print(f"Frame width: {width}")

#Root Init
root = tk.Tk()
root.geometry("800x800")
root.config(background="#ceeddf")

#Splitting root into grid
root.columnconfigure((0, 1, 2, 3, 4), weight=1)

root.rowconfigure((0, 1, 2, 4, 5), weight=1)
root.rowconfigure(3, weight=15)

#Top bar
topBar = tk.Frame(root, height=50, background="teal")
topBar.grid(row=0, column=0, columnspan=5, sticky="new")

#Splitting top bar into grid
topBar.columnconfigure((0, 1, 2), weight=1)
topBar.rowconfigure(0, weight=1)

#High Score Label
highscoreLbl = tk.Label(topBar, text=f"High Score: 0000", fg="teal",\
                        font=("Tahoma", 12, "bold"), bg="white" )
highscoreLbl.grid(row=0, column=0, pady=10, padx=10, sticky="w")

#Connect button
connectBtn = tk.Button(topBar, text="Connect", fg="teal", font=("Tahoma", 12, "bold"),\
                       bg="white", bd=3, relief="raised",)
connectBtn.grid(row=0, column=2, pady=10, padx=10, sticky="e")

#Heading
header = tk.Label(root, text="MINESWEEPER", fg="teal", font=("Tahoma", 35, "bold"),\
                  bg="white", highlightbackground="teal", highlightthickness=3)
header.grid(row=1, column=2, rowspan=2, sticky="news", padx=50)

#Game options
optionsFrame = tk.Frame(root, background="white", highlightbackground="teal",\
                        highlightthickness=3)
optionsFrame.grid(row=3, column=1, columnspan=3, sticky="news",\
                  padx=100, pady=100)

#Game options frame into grid
optionsFrame.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")

optionsFrame.rowconfigure((0, 1, 2, 3, 4), weight=1)

#Play game function
Ongoing = False
def PlayGame():
    global Ongoing
    if Ongoing:
        print("Game in progress...")
        return
    else:
        Ongoing = True
        GameWindow = Game.Main()
        startGameBtn.config(state="disabled")

    def on_close():
        global Ongoing
        Ongoing = False
        startGameBtn.config(state="normal")
        GameWindow.destroy()

    GameWindow.protocol("WM_DELETE_WINDOW", on_close)

#StartGame button                        
startGameBtn = tk.Button(optionsFrame, text="PLAY", relief="groove",\
                         font=("Tahoma", 25, "bold"), fg="white", bg="teal", bd=3,\
                         command=PlayGame)
startGameBtn.grid(row=1, column=1, columnspan=2, ipadx=30)

#Achievements frame
def showAchievements():
    achievementsFrame = tk.Frame(root, background="teal", highlightbackground="teal",\
                         highlightthickness=3)
    achievementsFrame.columnconfigure((0, 1, 2), weight=1, uniform='a')
    achievementsFrame.rowconfigure((0, 1, 2), weight=1, uniform='a')
    
    def destroyAchievements():
        achievementsFrame.destroy()
        
    achievementsFrame.grid(row=3, column=1, columnspan=3, sticky="news",\
                  padx=50, pady=100)

    achievementsHeader = tk.Label(achievementsFrame, text="ACHIEVEMENTS", fg="teal", font=("Tahoma", 30, "bold"),\
                  bg="white", highlightbackground="teal", highlightthickness=1)
    achievementsHeader.grid(row=0, column=0, columnspan=3, sticky="ew", pady=25)

    achievementsCancelBtn = tk.Button(achievementsFrame, text="Cancel", fg="white", bd=0,\
                                  background="teal", command=destroyAchievements)
    achievementsCancelBtn.grid(row=2, column=2, sticky="se")

#Achievement button                        
achievementsBtn = tk.Button(optionsFrame, text="Achievements", relief="groove",\
                         font=("Tahoma", 25, "bold"), fg="white", bg="teal", bd=3,\
                            command=showAchievements)
achievementsBtn.grid(row=2, column=1, columnspan=2, ipadx=30)

#Settings frame
def showSettings():
    Settings.Display(root)
    
#Settings button                        
settingsBtn = tk.Button(optionsFrame, text="Game Settings", relief="groove",\
                         font=("Tahoma", 25, "bold"), fg="white", bg="teal", bd=3,\
                         command=showSettings)
settingsBtn.grid(row=3, column=1, columnspan=2, ipadx=30)


