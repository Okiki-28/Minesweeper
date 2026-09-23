import random
import sys
import time
import tkinter as tk

import Config

CELL_SIZE = 28
PADDING = 10

# Right click is Button-3 on Windows/Linux but Button-2 on macOS
RIGHT_CLICK = "<Button-2>" if sys.platform == "darwin" else "<Button-3>"

# (columns, rows). "25x20" is 25 wide and 20 tall so it fits a landscape screen.
GRID_SIZES = {"8x8": (8, 8), "16x16": (16, 16), "25x20": (25, 20)}
MINE_DENSITY = {"Easy": 0.156, "Medium": 0.25, "Hard": 0.387}

HIDDEN_COLOUR = "grey"
REVEALED_COLOUR = "white"
MINE_COLOUR = "red"
START_COLOUR = "green"
FLAG_SYMBOL = "🏁"

# The mine animation always takes about 2 seconds however many mines there are
MAX_ANIMATION_MS = 2000
MAX_STEP_MS = 200


class MineField:

    def __init__(self, parent):
        self.parent = parent
        self.theme = Config.getTheme()
        self.numColumn, self.numRow = GRID_SIZES.get(Config.get("gridSize"), GRID_SIZES["16x16"])
        self.totalCells = self.numRow * self.numColumn
        self.flagsEnabled = Config.get("flags") == "On"
        density = MINE_DENSITY.get(Config.get("mineLevel"), MINE_DENSITY["Medium"])
        self.mineNumber = round(self.totalCells * density)

        self.cells = []
        self.minesIndex = []
        self.revealedCells = 0
        self.gameOver = False
        self.hasWon = False

        self.timerRunning = False
        self.startTime = 0
        self.finalTime = 0
        self.timerId = None
        self.animationId = None

        # Display
        self.frame = tk.Frame(parent, background=self.theme["light"])
        self.frame.grid(row=0, column=0, sticky="news", padx=PADDING, pady=PADDING)
        for i in range(self.numRow + 1):
            self.frame.rowconfigure(i, weight=1, uniform="a")
        for j in range(self.numColumn):
            self.frame.columnconfigure(j, weight=1, uniform="a")
        self.window = parent.winfo_toplevel()
        self.baseTitle = self.window.title()

        self.buildBoard()
        self.nonMineCells = self.totalCells - self.mineNumber
        self.flagsLeft = self.mineNumber
        self.topBar()

    # ---------- building the board ----------
    def neighbourIndexes(self, index):
        """Indexes of the (up to 8) cells touching this one."""
        row, column = divmod(index, self.numColumn)
        found = []
        for r in range(max(0, row - 1), min(self.numRow, row + 2)):
            for c in range(max(0, column - 1), min(self.numColumn, column + 2)):
                if (r, c) != (row, column):
                    found.append(r * self.numColumn + c)
        return found

    def buildBoard(self):
        # Pick the green starting cell first, then keep it and its neighbours
        # mine-free. That guarantees the start cell is a "0" that opens up
        # some space, however many mines there are.
        startIndex = random.randrange(self.totalCells)
        safeZone = set(self.neighbourIndexes(startIndex))
        safeZone.add(startIndex)
        candidates = [i for i in range(self.totalCells) if i not in safeZone]
        self.mineNumber = min(self.mineNumber, len(candidates))
        self.minesIndex = random.sample(candidates, self.mineNumber)
        mineSet = set(self.minesIndex)

        for i in range(self.totalCells):
            row, column = divmod(i, self.numColumn)
            cellClass = MineCell if i in mineSet else Cell
            cell = cellClass(self, self.frame, i, row, column)
            cell.placeCell()
            self.cells.append(cell)

        for cell in self.cells:
            cell.neighbours = [self.cells[j] for j in self.neighbourIndexes(cell.index)]

        for i in self.minesIndex:
            for neighbour in self.cells[i].neighbours:
                if not neighbour.isMine:
                    neighbour.mineCount += 1

        self.cells[startIndex].markAsStart()

    def topBar(self):
        half = self.numColumn // 2
        self.flagLabel = tk.Label(self.frame, font=("Tahoma", 10), relief="raised",
                                  borderwidth=2, fg=self.theme["main"])
        self.flagLabel.grid(row=0, column=0, sticky="news", columnspan=half)
        self.updateFlagLabel()

        self.timeLabel = tk.Label(self.frame, text="Time: 0000", font=("Tahoma", 10),
                                  relief="raised", borderwidth=2, fg=self.theme["main"])
        self.timeLabel.grid(row=0, column=half, sticky="news", columnspan=self.numColumn - half)

    def updateFlagLabel(self):
        word = "Flags" if self.flagsEnabled else "Mines"
        self.flagLabel.config(text=f"{word}: {self.flagsLeft}")

    # ---------- timer ----------
    def startTimer(self):
        if self.timerRunning or self.gameOver:
            return
        self.timerRunning = True
        self.startTime = time.time()
        self.tick()

    def tick(self):
        if not self.timerRunning:
            return
        seconds = int(time.time() - self.startTime)
        self.timeLabel.config(text=f"Time: {seconds:04d}")
        self.timerId = self.frame.after(200, self.tick)

    def endTimer(self):
        if self.timerRunning:
            self.finalTime = int(time.time() - self.startTime)
            self.timeLabel.config(text=f"Time: {self.finalTime:04d}")
        self.timerRunning = False
        if self.timerId is not None:
            self.frame.after_cancel(self.timerId)
            self.timerId = None
        return self.finalTime

    def stop(self):
        """Call before the window closes so no timer or animation is left running."""
        self.gameOver = True
        try:
            self.endTimer()
            if self.animationId is not None:
                self.frame.after_cancel(self.animationId)
                self.animationId = None
        except tk.TclError:
            pass

    # ---------- player actions ----------
    def leftClick(self, cell):
        if self.gameOver or cell.flagged:
            return
        self.startTimer()
        if cell.revealed:
            self.chord(cell)
        else:
            self.revealFrom(cell)

    def toggleFlag(self, cell):
        if self.gameOver or not self.flagsEnabled or cell.revealed:
            return
        change = -1 if cell.flagged else 1
        cell.setFlag(not cell.flagged)
        self.flagsLeft -= change
        for neighbour in cell.neighbours:
            neighbour.flaggedNeighbours += change
        self.updateFlagLabel()

    def revealFrom(self, start):
        """Reveal a cell, and keep opening neighbours while cells are 0.
        Uses a stack instead of recursion, so a big open area can never hit
        Python's recursion limit."""
        stack = [start]
        while stack:
            cell = stack.pop()
            if cell.revealed or cell.flagged:
                continue
            if not cell.reveal():          # it was a mine
                self.loseGame(cell)
                return
            self.revealedCells += 1
            if cell.mineCount == 0:
                stack.extend(cell.neighbours)
        self.checkWin()

    def chord(self, cell):
        """Clicking a number that already has enough flags around it opens the rest."""
        if cell.mineCount == 0 or cell.flaggedNeighbours != cell.mineCount:
            return
        for neighbour in cell.neighbours:
            if self.gameOver:
                return
            if not neighbour.revealed and not neighbour.flagged:
                self.revealFrom(neighbour)

    # ---------- end of game ----------
    def setResult(self, text):
        self.window.title(f"{self.baseTitle} - {text}")

    def checkWin(self):
        if not self.gameOver and self.revealedCells == self.nonMineCells:
            self.hasWon = True
            self.gameOver = True
            self.endTimer()
            self.setResult("You won!")
            self.animateMines(self.theme["main"])

    def loseGame(self, hitCell):
        if self.gameOver:
            return
        self.gameOver = True
        self.endTimer()
        hitCell.setColour(MINE_COLOUR)
        self.setResult("Game over")
        self.animateMines(MINE_COLOUR)

    def animateMines(self, colour, i=0):
        """Colour the mines one by one, using a single chain of timers."""
        if i >= len(self.minesIndex) or not self.frame.winfo_exists():
            return
        self.cells[self.minesIndex[i]].setColour(colour)
        delay = max(10, min(MAX_STEP_MS, MAX_ANIMATION_MS // len(self.minesIndex)))
        self.animationId = self.frame.after(delay, lambda: self.animateMines(colour, i + 1))


class Cell:
    isMine = False

    def __init__(self, board, parent, index, row, column):
        self.board = board
        self.index = index
        self.row = row
        self.column = column
        self.mineCount = 0            # mines touching this cell
        self.flaggedNeighbours = 0    # flags touching this cell
        self.revealed = False
        self.flagged = False
        self.neighbours = []

        self.button = tk.Button(parent, bg=HIDDEN_COLOUR, text="", font=("Helvetica", 8),
                                borderwidth=2, relief="raised")
        self.button.bind("<Button-1>", self.onLeftClick)
        self.button.bind(RIGHT_CLICK, self.onRightClick)

    def onLeftClick(self, event):
        self.board.leftClick(self)

    def onRightClick(self, event):
        self.board.toggleFlag(self)

    def placeCell(self):
        self.button.grid(row=self.row + 1, column=self.column, sticky="news")

    def reveal(self):
        """Show the number. Returns True because this cell was safe."""
        self.revealed = True
        text = str(self.mineCount) if self.mineCount else ""
        self.button.config(bg=REVEALED_COLOUR, fg="black", text=text, font=("Helvetica", 8))
        return True

    def setFlag(self, flagged):
        self.flagged = flagged
        if flagged:
            self.button.config(fg="red", text=FLAG_SYMBOL, font=("Helvetica", 12))
        else:
            self.button.config(fg="black", text="", font=("Helvetica", 8))

    def markAsStart(self):
        self.button.config(bg=START_COLOUR)

    def setColour(self, colour):
        self.button.config(bg=colour)


class MineCell(Cell):
    isMine = True

    def reveal(self):
        """Returns False because this cell was a mine."""
        return False


def openGame(parent=None, onClose=None):
    """Open a game window using the current settings.
    With a parent it is a child window of the menu; without one it is standalone."""
    theme = Config.getTheme()
    columns, rows = GRID_SIZES.get(Config.get("gridSize"), GRID_SIZES["16x16"])

    window = tk.Tk() if parent is None else tk.Toplevel(parent)
    window.title(f"Minesweeper - {Config.get('username')}")
    window.config(background=theme["light"])
    window.geometry(f"{columns * CELL_SIZE + 2 * PADDING}x{(rows + 1) * CELL_SIZE + 2 * PADDING}")
    window.resizable(False, False)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    field = MineField(window)

    def close():
        field.stop()
        window.destroy()
        if onClose:
            onClose()

    window.protocol("WM_DELETE_WINDOW", close)
    window.field = field
    return window


if __name__ == "__main__":
    openGame().mainloop()
