import tkinter as tk
import random
import math
import time

class MineField:

    #class attributes
    _gridSize = "16x16"
    _mineLevel = "Medium"
    _isFlag = "On"
    _cellSize = 25
    
    def __init__(self, root):
        self.root = root
        match self._gridSize:
            case "8x8":
                self.__numRow = 8
                self.__numColumn = 8
            case "16x16":
                self.__numRow = 16
                self.__numColumn = 16
            case "25x20":
                self.__numRow = 25
                self.__numColumn = 20
            case _:
                self.__numRow = 16
                self.__numColumn = 16

        match self._mineLevel:
            case "Easy":
                self.__mineNumber = round(self.__numRow*self.__numColumn*0.156)
            case "Medium":
                self.__mineNumber = round(self.__numRow*self.__numColumn*0.25)
            case "Hard":
                self.__mineNumber = round(self.__numRow*self.__numColumn*0.387)
            case _:
                pass

        match self._isFlag:
            case "On":
                pass
            case "Off":
                pass
            case _:
                pass

        self.__cells = []
        self.__minesIndex = []
        self.__revealCells = []

        self.flagCount = self.__mineNumber
        self.totalCells = self.__numRow*self.__numColumn
        self.nonMineCells = (self.__numRow*self.__numColumn)-self.__mineNumber
        self.revealedCells = 0
        self.state = True
        self.hasWon = False
        

        #Display attributes
        self.frameSize = self.__mineNumber*self._cellSize
        self.frame = tk.Frame(self.root, background="#ceeddf")
        self.frame.grid(row=0, column=0, sticky="news")
        for i in range(self.__numRow+1):
            self.frame.rowconfigure(i, weight=1, uniform="a")
        for j in range(self.__numColumn):
            self.frame.columnconfigure(j, weight=1, uniform="a")
        ###
        self.topBar()
        self.__arrangeCells()
        #self.startTimer()
        
        
    def __arrangeCells(self):
        for i in range(self.__mineNumber):
            mineIndex = random.randrange(1, self.totalCells)
            while mineIndex in self.__minesIndex:
                mineIndex = random.randrange(1, self.totalCells)
            self.__minesIndex.append(mineIndex)

        self.placeCells()
        self.pickFirstCell()

    def decreaseFlags(self):
        self.flagCount -= 1
        self.flagLabel.config(text=f"Flags: {self.flagCount}")

    def increaseFlags(self):
        self.flagCount += 1
        self.flagLabel.config(text=f"Flags: {self.flagCount}")

    def topBar(self):
        self.flagLabel = tk.Label(self.frame, text=f"Flags: {self.flagCount}",\
                             font=("Tahoma", 10), relief="raised", borderwidth=2)
        self.flagLabel.grid(row=0, column=0, sticky="news", columnspan=self.__numColumn//2)

        self.timeLabel = tk.Label(self.frame, text=f"Time: 0000",\
                             font=("Tahoma", 10), relief="raised", borderwidth=2)
        self.timeLabel.grid(row=0, column=8, sticky="news", columnspan=self.__numColumn//2)

    def startTimer(self):
        self.timer = True
        self.startTime = time.time()
        self.after_id = self.root.after(1000, self.updateTimer)

    def updateTimer(self):
        if not self.timer:
            return
        self.newTime = str(int(time.time()-self.startTime))
        while len(self.newTime) < 4:
            self.newTime = "0"+self.newTime
        self.timeLabel.config(text=f"Time: {self.newTime}")
        self.after_id = self.root.after(1000, self.updateTimer)

    def endTimer(self):
        self.timer = False
        if hasattr(self, "after_id"):
            self.root.after_cancel(self.after_id)

    def placeCells(self):
        for i in range(self.totalCells):
            if i in self.__minesIndex:
                cell = MineCell(Board=self,
                                Frame=self.frame,
                                size=self._cellSize,
                                index=i)
            else:
                cell = Cell(Board=self,
                            Frame=self.frame,
                            size=self._cellSize,
                            index=i)
            cell.co_od = [(i//self.__numRow), (i%self.__numColumn)]
            cell.placeCell()
            self.__cells.append(cell)
            self.identifyNeighbouringCells(cell)
        self.findMineNumbers()

    def pickFirstCell(self):
        cell = random.choice(self.__cells)
        if cell.mineCount == 0:
            cell.isFirstCell()
            return cell
        else:
            return self.pickFirstCell()

    def addMineCount(self, cell):
        cell.mineCount += 1

    def identifyNeighbouringCells(self, cell):
        closeCells = []
        row = cell.co_od[0]
        column = cell.co_od[1]
        
        if column > 0:
            closeCells.append(((row-1)*self.__numRow)+(column-1))
            closeCells.append(((row)*self.__numRow)+(column-1))
            closeCells.append(((row+1)*self.__numRow)+(column-1))
        closeCells.append(((row-1)*self.__numRow)+column)
        closeCells.append(((row+1)*self.__numRow)+column)
        if column + 1 < self.__numColumn:
            closeCells.append(((row-1)*self.__numRow)+(column+1))
            closeCells.append(((row)*self.__numRow)+(column+1))
            closeCells.append(((row+1)*self.__numRow)+(column+1))
        closeCells = [i for i in closeCells if (0 <= i < self.totalCells)]
        cell.closeCells = closeCells
        closeCells, row, column = [], -1, -1

    def findMineNumbers(self):
        closeCells = []
        for i in self.__minesIndex:
            cell = self.__cells[i]
            closeCells = cell.closeCells

            for j in closeCells:
                tempCell = self.__cells[j]
                if not tempCell.__class__.__name__ == "MineCell":
                    self.addMineCount(tempCell)
    #Getters
    @classmethod      
    def getGridSize(self):
        return self._gridSize

    @classmethod      
    def getMineLevel(self):
        return self._mineLevel

    @classmethod      
    def getFlagStatus(self):
        return self._isFlag

    #Setters
    @classmethod      
    def setGridSize(self, GridVar):
        self._gridSize = GridVar

    @classmethod      
    def setMineLevel(self, MineVar):
        self._mineLevel = MineVar

    @classmethod      
    def setFlagStatus(self, FlagVar):
        self._isFlag = FlagVar
                    
    def getCell(self, index):
        return self.__cells[index]

    def getMinesIndex(self):
        return self.__minesIndex

    def getMineNumber(self):
        return self.__mineNumber

    def checkState(self):
        if self.state == False:
            self.frame.destroy()
        if self.revealedCells == self.nonMineCells:
            self.hasWon = True
            self.__hasWonEvent(0)
            
    def __hasWonEvent(self, i):
        if i >= self.__mineNumber:
            return
        mineIndex = self.__minesIndex[i]
        cell = self.getCell(mineIndex)
        cell.changeColor("teal")
        self.frame.after(200, lambda: self.__hasWonEvent(i+1))
            

    def emptyFunc(self):
        return

def getGridSize():
    return MineField.getGridSize()

def getMineLevel():
    return MineField.getMineLevel()

def getFlagStatus():
    return MineField.getFlagStatus()

def UpdateSettings(**kwargs):
    GridVar = kwargs['GridVar']
    MineVar = kwargs['MineVar']
    FlagVar = kwargs['FlagVar']
    
    MineField.setGridSize(GridVar)
    MineField.setMineLevel(MineVar)
    MineField.setFlagStatus(FlagVar)
                
class Cell():
    def __init__(self, Board, Frame, size,  index):
        self.size = size
        self.index = index
        self.mineCount = 0
        self.flagCount = 0
        self.co_od = [-1, -1]
        self.Board = Board
        
        self.revealed = False
        self.flagged = False
        self.closeCells = []
        
        # Display attributes
        self.color  = "grey"
        self.fontSize = 12
        self.flag = "🏁"
        self.__cell = tk.Button(Frame, bg="grey", text="", font=("Helvetica", 8), borderwidth=2, relief="raised")
        self.__cell.bind("<Button-1>", self.revealCell)
        self.__cell.bind("<Button-3>", self.flagCell)
        
    def changeColor(self):
        pass ###

    def revealCell(self, event):
        if self.Board.revealedCells == 0:
            self.Board.startTimer()
        if self.revealed == True:
            if self.flagCount == self.mineCount:
                self.clearSpace()
            return
        else:
            self.revealed = True
            self.Flagged = False
            
        if self.mineCount == 0:
            cellText = ""
        else:
             cellText = str(self.mineCount)
             
        self.__cell.config(bg="white",
                            fg="black",
                            text=cellText,
                           font = ("Helvetica", 8))
        self.Board.revealedCells += 1
        if self.mineCount == 0:
            self.clearSpace()
        self.Board.checkState()

    def placeCell(self):
        self.__cell.grid(row=self.co_od[0]+1,
                         column=self.co_od[1],
                         sticky="news")

    def flagCell(self, event):
        if self.revealed == True:
            return
        if self.flagged == True:
            self.unflagCell()
            return
        self.flagged = True
        self.Board.decreaseFlags()
        for i in self.closeCells:
            cell = self.Board.getCell(i)
            cell.flagCount += 1
        self.__cell.config(fg="red",
                           text=self.flag,
                           font=("Helvetica", 12))

    def unflagCell(self):
        self.flagged = False
        self.Board.increaseFlags()
        for i in self.closeCells:
            cell = self.Board.getCell(i)
            cell.flagCount -= 1
        self.__cell.config(fg="black",
                           text="",
                           font=("Helvetica", 8))

    def clearSpace(self):
        for i in self.closeCells:
            cell = self.Board.getCell(i)
            if cell.__class__.__name__ == "Cell" and not cell.revealed:
                cell.revealCell(None)
            elif cell.__class__.__name__ == "MineCell" and not cell.flagged:
                cell.endGame()
                

    def isFirstCell(self):
        self.__cell.config(bg="green")

    def changeColor(self, color):
        self.__cell.config(bg=color)   

        
class MineCell(Cell):
    def __init__(self, Board, Frame, size, index):
        super().__init__(Board, Frame, size,  index)
        self.mineCount = -1

    def revealCell(self, event):
        self.changeColor("red")
        self.endGameEvent()
        self.Board.state = True
        self.Board.checkState()

    def endGame(self):
        self.Board.endTimer()
        minesIndex = self.Board.getMinesIndex()
        for i in minesIndex:
            cell = self.Board.getCell(i)
            cell.endGameEvent()
            
    def endGameEvent(self, i=0):
        timeSpent = self.Board.endTimer()
        if i >= self.Board.getMineNumber():
            return
        minesIndex = self.Board.getMinesIndex()
        mineIndex = minesIndex[i]
        cell = self.Board.getCell(mineIndex)
        cell.changeColor("red")
        self.Board.frame.after(200, lambda: self.endGameEvent(i+1))

def Main(*args):
    numRow = 16
    numColumn = 16
    
    root = tk.Tk()
    root.title("Greeting App with Grid")
    root.config(background="#ceeddf")
    root.geometry("560x560")
    root.resizable(False, False)

    root.rowconfigure((0, 2), weight=1, uniform="a")
    root.rowconfigure(1, weight=10, uniform="a")
    root.columnconfigure((0, 2), weight=1,  uniform="a")
    root.columnconfigure(1, weight=10, uniform="a")


    MainFrame = tk.Frame(root)
    MainFrame.grid(row=1, column=1, sticky="news")
    MainFrame.rowconfigure(0, weight=1, uniform="a")
    MainFrame.columnconfigure(0, weight=1, uniform="a")
    
    mineField = MineField(root=MainFrame)
    return root

if __name__ == "__main__":
    Main()
