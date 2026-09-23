import tkinter as tk

import Config
import Game
import Settings

# Root Init
root = tk.Tk()
root.title("Minesweeper")
root.geometry("800x800")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

menu = None          # frame holding the whole menu, so it can be rebuilt with a new theme
panel = None         # the Settings / Achievements panel currently showing
gameWindow = None    # the game window currently open, if any
startGameBtn = None


def closePanel():
    global panel
    if panel is not None and panel.winfo_exists():
        panel.destroy()
    panel = None


# Play game
def playGame():
    global gameWindow
    if gameWindow is not None:
        return
    gameWindow = Game.openGame(root, onClose=gameClosed)
    startGameBtn.config(state="disabled")


def gameClosed():
    global gameWindow
    gameWindow = None
    startGameBtn.config(state="normal")


# Achievements panel
def showAchievements():
    global panel
    closePanel()
    theme = Config.getTheme()
    main = theme["main"]

    achievementsFrame = tk.Frame(menu, background=main, highlightbackground=main,
                                 highlightthickness=3)
    achievementsFrame.columnconfigure((0, 1, 2), weight=1, uniform='a')
    achievementsFrame.rowconfigure((0, 1, 2), weight=1, uniform='a')
    achievementsFrame.grid(row=3, column=1, columnspan=3, sticky="news", padx=50, pady=100)

    achievementsHeader = tk.Label(achievementsFrame, text="ACHIEVEMENTS", fg=main,
                                  font=("Tahoma", 30, "bold"), bg="white",
                                  highlightbackground=main, highlightthickness=1)
    achievementsHeader.grid(row=0, column=0, columnspan=3, sticky="ew", pady=25)

    achievementsCancelBtn = tk.Button(achievementsFrame, text="Cancel", fg="white", bd=0,
                                      background=main, command=achievementsFrame.destroy)
    achievementsCancelBtn.grid(row=2, column=2, sticky="se")
    panel = achievementsFrame


# Settings panel
def showSettings():
    global panel
    closePanel()
    panel = Settings.Display(menu, onSaved=buildMenu)


def buildMenu():
    """Draw the whole menu using the current theme and username.
    Called at start-up and again whenever settings are saved."""
    global menu, panel, startGameBtn
    if menu is not None:
        menu.destroy()
    panel = None

    theme = Config.getTheme()
    main, light = theme["main"], theme["light"]
    root.config(background=light)

    menu = tk.Frame(root, background=light)
    menu.grid(row=0, column=0, sticky="news")

    # Splitting the menu into grid
    menu.columnconfigure((0, 1, 2, 3, 4), weight=1)
    menu.rowconfigure((0, 1, 2, 4, 5), weight=1)
    menu.rowconfigure(3, weight=15)

    # Top bar
    topBar = tk.Frame(menu, height=50, background=main)
    topBar.grid(row=0, column=0, columnspan=5, sticky="new")
    topBar.columnconfigure((0, 1, 2), weight=1)
    topBar.rowconfigure(0, weight=1)

    highscoreLbl = tk.Label(topBar, text="High Score: 0000", fg=main,
                            font=("Tahoma", 12, "bold"), bg="white")
    highscoreLbl.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    usernameLbl = tk.Label(topBar, text=f"Player: {Config.get('username')}", fg=main,
                           font=("Tahoma", 12, "bold"), bg="white")
    usernameLbl.grid(row=0, column=2, pady=10, padx=10, sticky="e")

    # Heading
    header = tk.Label(menu, text="MINESWEEPER", fg=main, font=("Tahoma", 35, "bold"),
                      bg="white", highlightbackground=main, highlightthickness=3)
    header.grid(row=1, column=2, rowspan=2, sticky="news", padx=50)

    # Game options
    optionsFrame = tk.Frame(menu, background="white", highlightbackground=main,
                            highlightthickness=3)
    optionsFrame.grid(row=3, column=1, columnspan=3, sticky="news", padx=100, pady=100)
    optionsFrame.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
    optionsFrame.rowconfigure((0, 1, 2, 3, 4), weight=1)

    def makeButton(text, row, command, state="normal"):
        button = tk.Button(optionsFrame, text=text, relief="groove",
                           font=("Tahoma", 25, "bold"), fg="white", bg=main, bd=3,
                           command=command, state=state)
        button.grid(row=row, column=1, columnspan=2, ipadx=30)
        return button

    startGameBtn = makeButton("PLAY", 1, playGame,
                              state="disabled" if gameWindow is not None else "normal")
    makeButton("Achievements", 2, showAchievements)
    makeButton("Game Settings", 3, showSettings)


buildMenu()
root.mainloop()
