import tkinter as tk
from tkinter import *
import Game

def Empty():
    pass

def Display(root):
    SettingsFrame = tk.Frame(root, background="teal", highlightbackground="teal",\
                         highlightthickness=3)
    SettingsFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
    SettingsFrame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
    
    def destroySettings():
        SettingsFrame.destroy()
        
    SettingsFrame.grid(row=3, column=1, columnspan=3, sticky="news",\
                  padx=50, pady=100)

    SettingsHeader = tk.Label(SettingsFrame, text="Settings", fg="teal", font=("Tahoma", 30, "bold"),\
                  bg="white", highlightbackground="teal", highlightthickness=1)
    SettingsHeader.grid(row=0, column=0, columnspan=7, sticky="we")

    SettingsCancelBtn = tk.Button(SettingsFrame, text="Cancel", fg="white", bd=0,\
                                  background="teal", command=destroySettings)
    SettingsCancelBtn.grid(row=5, column=6, sticky="se")

    # Grid Size
    initialGridVal = Game.getGridSize()
    GridVar = tk.StringVar(value=initialGridVal)
    GridLabel = tk.Label(SettingsFrame, text="Grid Size", font=("Tahoma", 10), relief="raised", borderwidth=2)
    GridLabel.grid(row=1, column=1, sticky="sew", padx=3)
    GridOptions = ["8x8", "16x16", "25x20"]
    GridDropdown = tk.OptionMenu(SettingsFrame, GridVar, *GridOptions)
    GridDropdown.grid(row=1, column=3, sticky="sew", columnspan=3, padx=3)

    #No of mines
    initialMineVal = Game.getMineLevel()
    MineVar = tk.StringVar(value=initialMineVal)
    MineLabel = tk.Label(SettingsFrame, text="Mine Count", font=("Tahoma", 10), relief="raised", borderwidth=2)
    MineLabel.grid(row=2, column=1, sticky="sew", padx=3)
    MineOptions = ["Easy", "Medium", "Hard"]
    MineDropdown = tk.OptionMenu(SettingsFrame, MineVar, *MineOptions)
    MineDropdown.grid(row=2, column=3, sticky="sew", columnspan=3, padx=3)

    #Flag
    initialFlagVal = Game.getFlagStatus()
    FlagVar = tk.StringVar(value=initialFlagVal)  
    FlagLabel = tk.Label(SettingsFrame, text="Flags", font=("Tahoma", 10), relief="raised", borderwidth=2)
    FlagLabel.grid(row=3, column=1, sticky="sew", padx=3)
    FlagOptions = ["On", "Off"]
    FlagDropdown = tk.OptionMenu(SettingsFrame, FlagVar, *FlagOptions)
    FlagDropdown.grid(row=3, column=3, sticky="sew", columnspan=3, padx=3)

    ###
    def UpdateSettings():
        print("Settings updated...")
        Game.UpdateSettings(GridVar=GridVar.get(),
                            MineVar=MineVar.get(),
                            FlagVar=FlagVar.get())
        SettingsFrame.destroy()

    #Save Button
    SaveBtn = tk.Button(SettingsFrame, text="Save", relief="groove",\
                         font=("Tahoma", 10, "bold"), bg="white", bd=3,\
                         command=UpdateSettings)
    SaveBtn.grid(row=4, column=3, sticky="sew")
