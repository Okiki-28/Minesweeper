import tkinter as tk
import random

def on_left_click(event):
    event.widget.config(bg="white")
    event.widget.config(text="1")

def on_right_click(event):
    event.widget.config(text="$")

root = tk.Tk()
root.title("Greeting App with Grid")
root.geometry("400x400")



class MineBoard():
    
    def __init__(self):
        self.__numRow = 16
        self.__mineNumber = 40
        self.__cellIndex = []
        self.__mineIndex = []
        self.__openingCells = []

        self.totalFlags = self.__mineNumber
        self.availableCells = (self.__numRow**2)-self.__mineNumber
        self.openedCells = 0
        self.flaggedCells = 0

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()        
        self.frameSize = self.__mineNumber*Cell(self, root, -1).getSize()
        self.frame = tk.Frame(root, width=self.frameSize, height=self.frameSize, background="red")
        self.frame.place(x=(screen_width-100)-(self.frameSize), y=50)
        
        #Array of mine indexes
        for i in range(self.__mineNumber):
            randIndex = random.randrange(1, self.__numRow**2)
            while randIndex in self.__mineIndex:
                randIndex = random.randrange(1, self.__numRow**2)
            self.__mineIndex.append(randIndex)
        self.placeCells()
        emptyCell = [cell for cell in self.__cellIndex if cell.mineCount == 0 and not isinstance(cell, MineCell)]
        firstCell = random.choice(emptyCell)
        firstCell.firstCell()
        print(sorted(self.__mineIndex))

    def placeCells(self):
        self.cellSize = Cell(self, self.frame, 0).getSize()

        #Arranging cells into array
        for i in range(self.__numRow**2):
            if i in self.__mineIndex:
                cellSquare = MineCell(self, self.frame, i)
            else:
                cellSquare = Cell(self, self.frame, i)
            self.__cellIndex.append(cellSquare)
            self.identifyCloseCells(i)

        self.assignNumbers()

        #Placing cells inside frame
        x_cood = 0
        y_cood = 0
        for j, cellSquare in enumerate(self.__cellIndex):
            cellSquare.cood = (x_cood, y_cood)
            cellSquare.placeCell(x_cood*self.cellSize, y_cood*self.cellSize)
            x_cood += 1
            if (j+1) % self.__numRow == 0:
                x_cood = 0
                y_cood += 1

    def identifyCloseCells(self, index):
        self.__closeCells = []
        row = index//self.__numRow
        column = index%self.__numRow

        if not column-1<0:
            self.__closeCells.append(((row-1)*self.__numRow)+(column-1))
            self.__closeCells.append(((row)*self.__numRow)+(column-1))
            self.__closeCells.append(((row+1)*self.__numRow)+(column-1))

        self.__closeCells.append(((row-1)*self.__numRow)+column)
        self.__closeCells.append(((row+1)*self.__numRow)+column)
        
        if not column+1 > (self.__numRow-1):
            self.__closeCells.append(((row-1)*self.__numRow)+(column+1))
            self.__closeCells.append(((row)*self.__numRow)+(column+1))
            self.__closeCells.append(((row+1)*self.__numRow)+(column+1))
        self.__closeCells = [i for i in self.__closeCells if 0<= i < (self.__numRow**2)]
        self.__cellIndex[index].closeCells = self.__closeCells
        return self.__closeCells

    def assignNumbers(self):
        for i in sorted(self.__mineIndex):
            self.__closeCells = self.__cellIndex[i].closeCells
            for j in self.__closeCells:
                if not type(self.__cellIndex[j]).__name__ == "MineCell":
                    self.__cellIndex[j].addMineCount()

    def win(self):
        pass
    
            

class Cell():
    def __init__(self, Board, Frame, i):
        self.__size = 25
        self.__color = "grey"
        self.__fontSize = 12
        self.__cell = tk.Button(Frame, bg="grey", text="", font=("Helvetica", 8), borderwidth=2, relief="raised")
        self.__eventFunctions()
        self.closeCells = []
        self.mineCount = 0
        self.cood = ()
        self.flag = "\U0001F3C1" 
        self.i = i
        self.Board = Board
        self.revealed = False
        self.flagged = False
        self.flagCount = 0

    def getSize(self):
        return self.__size

    def firstCell(self):
        self.__cell.config(bg="green")

    def placeCell(self, x_cood, y_cood):
        self.__cell.place(x=x_cood, y=y_cood, width=self.__size, height=self.__size)

    def revealCell(self, event=None):
        if self.revealed == True:
            if self.flagCount == self.mineCount:
                self.checkCell()
            elif self.flagCount > self.mineCount:
                return
            return
        self.revealed = True
        if self.mineCount == 0:
            cellText = ""
        else:
            cellText = str(self.mineCount)
        event.widget.config(bg="white", fg="black", text=cellText)
        self.__cell.bind("<Button-3>", self.emptyFunc)
        self.Board.openedCells += 1
        if self.mineCount == 0:
            self.checkCell()
        self.checkWin()
        return cellText

    def nonEventRevealCell(self):
        if self.flagged == True:
            return
        self.revealed = True
        cellText = str(self.mineCount)
        if self.mineCount == 0:
            cellText = ""
        else:
            cellText = str(self.mineCount)
        self.__cell.config(bg="white", fg="black", text=cellText, font=("Helvetica", 8))
        self.__cell.bind("<Button-3>", self.emptyFunc)
        self.Board.openedCells += 1
        if self.mineCount == 0:
            self.checkCell()

    def checkCell(self):
        for i in self.closeCells:
            cell = self.Board._MineBoard__cellIndex[i]
            if not isinstance(cell, MineCell) and not cell.revealed:
                cell.nonEventRevealCell()
            elif isinstance(cell, MineCell) and not cell.flagged:
                print("!!!")
                cell.endGame()
        self.checkWin()
        

    def flagCell(self, event):
        self.flagged = True
        self.Board.totalFlags -= 1
        for i in self.closeCells:
            cell = self.Board._MineBoard__cellIndex[i]
            cell.flagCount += 1
        event.widget.config(text=self.flag, fg="red", font=("Helvetica", 12))
        self._Cell__cell.bind("<Button-3>", self.unflagCell)
        

    def unflagCell(self, event):
        self.flagged = False
        self.Board.totalFlags += 1
        for i in self.closeCells:
            cell = self.Board._MineBoard__cellIndex[i]
            cell.flagCount -= 1
        event.widget.config(text="", fg="black", font=("Helvetica", 8))
        self._Cell__cell.bind("<Button-3>", self.flagCell)

    def openCells(self):
        pass


    def emptyFunc(self, event):
        return

    def getText(self):
        pass

    def addMineCount(self):
        if type(self.mineCount).__name__ == "str":
            self.mineCount = 0
        self.mineCount += 1

    def __eventFunctions(self):
        self.__cell.bind("<Button-1>", self.revealCell)
        self.__cell.bind("<Button-3>", self.flagCell)

    def checkWin(self):
        if self.Board.availableCells == self.Board.openedCells:
            self.Board.win()
        # print(f"Flagged: {self.Board.totalFlags}")
        # print(f"opened: {self.Board.openedCells}")


class MineCell(Cell):
    def __init__(self, Board, Frame, i):
        super().__init__(Board, Frame, i)

    def revealCell(self, event):
        self.endGame()

    def openCell(self):
        self._Cell__cell.config(bg="red", text=self.getText())
        self._Cell__cell.bind("<Button-3>", self.emptyFunc)

    def endGame(self):
        for i in self.Board._MineBoard__mineIndex:
            cell = self.Board._MineBoard__cellIndex[i]
            cell.openCell()

    def openCells(self, i):
        return

    def nonEventRevealCell(self):
        return

Board1 = MineBoard()
root.mainloop()
