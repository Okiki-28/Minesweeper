import tkinter as tk
from tkinter import colorchooser

import Config


def Display(parent, onSaved=None):
    """Draw the settings panel inside parent and return it.
    onSaved is called after the settings have been saved."""
    theme = Config.getTheme()
    main = theme["main"]

    SettingsFrame = tk.Frame(parent, background=main, highlightbackground=main,
                             highlightthickness=3)
    SettingsFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
    SettingsFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')
    SettingsFrame.grid(row=3, column=1, columnspan=3, sticky="news", padx=50, pady=100)

    SettingsHeader = tk.Label(SettingsFrame, text="Settings", fg=main,
                              font=("Tahoma", 30, "bold"), bg="white",
                              highlightbackground=main, highlightthickness=1)
    SettingsHeader.grid(row=0, column=0, columnspan=7, sticky="we")

    def addLabel(text, row):
        label = tk.Label(SettingsFrame, text=text, font=("Tahoma", 10),
                         relief="raised", borderwidth=2)
        label.grid(row=row, column=1, sticky="sew", padx=3)

    def addDropdown(variable, options, row):
        dropdown = tk.OptionMenu(SettingsFrame, variable, *options)
        dropdown.grid(row=row, column=3, sticky="sew", columnspan=3, padx=3)
        return dropdown

    # Username
    UsernameVar = tk.StringVar(value=Config.get("username"))
    addLabel("Username", 1)
    UsernameEntry = tk.Entry(SettingsFrame, textvariable=UsernameVar, font=("Tahoma", 10))
    UsernameEntry.grid(row=1, column=3, sticky="sew", columnspan=3, padx=3)

    # Theme colour
    ThemeVar = tk.StringVar(value=Config.get("theme"))
    customColour = {"value": Config.get("customColor")}
    addLabel("Theme", 2)
    ThemeDropdown = tk.OptionMenu(SettingsFrame, ThemeVar, *Config.THEMES, Config.CUSTOM)
    ThemeDropdown.grid(row=2, column=3, sticky="sew", columnspan=2, padx=3)

    MessageVar = tk.StringVar(value="")

    def pickColour():
        result = colorchooser.askcolor(color=customColour["value"],
                                       title="Choose a theme colour", parent=parent)
        chosen = result[1]
        if chosen is None:               # the user cancelled
            return
        if Config.isTooLight(chosen):
            MessageVar.set("That colour is too light to read. Pick a darker one.")
            return
        customColour["value"] = chosen.lower()
        ThemeVar.set(Config.CUSTOM)
        MessageVar.set("")

    PickBtn = tk.Button(SettingsFrame, text="Pick colour", font=("Tahoma", 10),
                        relief="groove", command=pickColour)
    PickBtn.grid(row=2, column=5, sticky="sew", padx=3)

    # Grid size
    GridVar = tk.StringVar(value=Config.get("gridSize"))
    addLabel("Grid Size", 3)
    addDropdown(GridVar, Config.GRID_OPTIONS, 3)

    # Number of mines
    MineVar = tk.StringVar(value=Config.get("mineLevel"))
    addLabel("Mine Count", 4)
    addDropdown(MineVar, Config.MINE_OPTIONS, 4)

    # Flags
    FlagVar = tk.StringVar(value=Config.get("flags"))
    addLabel("Flags", 5)
    addDropdown(FlagVar, Config.FLAG_OPTIONS, 5)

    # Message line (shows problems such as an invalid username)
    MessageLabel = tk.Label(SettingsFrame, textvariable=MessageVar, fg="white", bg=main,
                            font=("Tahoma", 10, "bold"))
    MessageLabel.grid(row=6, column=1, columnspan=5, sticky="ew")

    def UpdateSettings():
        name = UsernameVar.get().strip()
        error = Config.usernameError(name)
        if error:
            MessageVar.set(error)
            return
        Config.update(username=name,
                      theme=ThemeVar.get(),
                      customColor=customColour["value"],
                      gridSize=GridVar.get(),
                      mineLevel=MineVar.get(),
                      flags=FlagVar.get())
        Config.save()
        SettingsFrame.destroy()
        if onSaved:
            onSaved()

    SaveBtn = tk.Button(SettingsFrame, text="Save", relief="groove",
                        font=("Tahoma", 10, "bold"), bg="white", bd=3,
                        command=UpdateSettings)
    SaveBtn.grid(row=7, column=3, sticky="sew")

    SettingsCancelBtn = tk.Button(SettingsFrame, text="Cancel", fg="white", bd=0,
                                  background=main, command=SettingsFrame.destroy)
    SettingsCancelBtn.grid(row=7, column=6, sticky="se")

    return SettingsFrame
