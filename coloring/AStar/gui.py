from state import State
import tkinter as tk
from time import sleep
from tkinter.constants import ACTIVE, BOTH, DISABLED, E, LEFT, RIGHT, TOP, W, X
from readFile import readFile
from AStar import AStar
from tkinter.filedialog import askopenfilename
from time import time

class Table:
    '''
    Square grid containing cells (color, number)
    '''

    def __init__(self,root, matrix):  
        # code for creating table
        self.table = []
        fixedSize = 500/len(matrix)
        for i in range(len(matrix)):
            line = []
            for j in range(len(matrix[i])):
                cell = tk.Canvas(root, width=fixedSize, height = fixedSize, highlightthickness=1, highlightbackground='black')
                cell.configure(bg='green')
                cellContent = str(matrix[i][j]) if matrix[i][j] != -1 else ''
                cell.create_text(int(fixedSize/2),int(fixedSize/2),font=('Arial',15), text = cellContent)
                line.append(cell)
            self.table.append(line)
    

    def grid_table(self, row, column):
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                self.table[i][j].grid(row = row + i, column = column + j)


    def fill_color(self, row, column, color):
        textColor = 'red' if color else 'green'
        self.table[row][column].configure(bg=textColor)
        self.table[row][column].update()


class GUI:


    def __init__(self, root):

        #The previous red position
        self.prevReds = []
        #The matrix loaded from the browsed file
        self.matrix = []

        #Design UI
        self.root = root
        self.title = tk.Label(root, text = "Coloring Solver",width= 30, height = 1, font=("Arial",20))
        self.title.grid(row=0,column=0)

        self.browseFile = tk.Button(root, text = "Browse file", font =("Arial", 10), command=self.browseFiles)
        self.browseFile.grid(row=1, column=0,sticky=W,padx=25)
        self.browseFileTextVar = tk.StringVar()
        self.browseFileShow = tk.Entry(root, width=80, textvariable=self.browseFileTextVar)
        self.browseFileShow.configure(state=DISABLED)
        self.browseFileTextVar.set("File path")
        self.browseFileShow.grid(row=2, column=0,sticky=W,padx=25)

        self.delayTime = 0.5
        self.delayButton = tk.Button(root, text = "Update delay time", font = ("Arial", 10), command=self.updateDelayTime)
        self.delayButton.grid(row = 3, column = 0, sticky=W,padx=25)
        self.delayTimeTextVar = tk.StringVar()
        self.delayTimeShow = tk.Entry(root, width = 30, textvariable=self.delayTimeTextVar)
        self.delayTimeTextVar.set('0.5')
        self.delayTimeShow.grid(row = 4, column = 0, sticky=W,padx=25)

        self.solveButton = tk.Button(root, text = "Solve", font =("Arial", 10), state=DISABLED, command=self._solve)
        self.solveButton.grid(row = 5, column = 0, sticky=W,padx=25)

        self.currentStepText = tk.StringVar()
        self.currentStep = tk.Entry(root, width =30, textvariable=self.currentStepText)
        self.currentStepText.set("Step: ")
        self.currentStep.configure(state=DISABLED)
        self.currentStep.grid(row = 6, column = 0, sticky=W,padx=25)

        self.currentHeuText = tk.StringVar()
        self.currentHeu = tk.Entry(root, width = 30, textvariable=self.currentHeuText)
        self.currentHeuText.set("Heuristic: ")
        self.currentHeu.configure(state=DISABLED)
        self.currentHeu.grid(row = 7, column = 0, sticky=W,padx=25)

        self.currentTimeVar = tk.StringVar()
        self.curentTime = tk.Entry(root, width = 30, textvariable=self.currentTimeVar)
        self.currentTimeVar.set('0')
        self.curentTime.configure(state=DISABLED)
        self.curentTime.grid(row = 8, column = 0, sticky=W,padx=25)

        self.tableFrame = tk.Frame(self.root, highlightthickness=1, highlightbackground="black", width=500, height = 500)


    def browseFiles(self):
        filename = askopenfilename(initialdir = "\\",
                                          title = "Select a File",
                                          filetypes = (("Text files","*.txt*"),("all files","*.*")))

        self.matrix.clear()
        self.matrix = readFile(filename)
    
        self.tableFrame.destroy()
        self.tableFrame = tk.Frame(self.root, highlightthickness=1, highlightbackground="black", width=500, height = 500)
        self.tableResult = Table(self.tableFrame,self.matrix)
        self.tableFrame.grid(row = 9, columnspan = 2, padx = 25, pady= 10)

        self.tableResult.grid_table(9,0)

        self.browseFileTextVar.set(filename)

        self.solveButton.config(state = ACTIVE)
    

    def updateDelayTime(self):

        try:
            float(self.delayTimeTextVar.get())
            self.delayTime = float(self.delayTimeTextVar.get())
        except:
            self.delayTimeTextVar.set(f"Time: {str(self.delayTime)}")


    def updatecurrentInfor(self, startTime, step, state: State):
        
        self.currentStepText.set(f"Step: {step}")
        self.currentHeuText.set(f"Heuristic: {state.getHeuristic()}")
        self.currentTimeVar.set(str(time() - startTime))
        #Clear the previous red
        for red in self.prevReds:
            self.tableResult.fill_color(red[0], red[1], False)

        for redSlot in state.getRedSlots().getSlots():
            self.tableResult.fill_color(redSlot[0], redSlot[1], True)


    def _solve(self):

        self.prevReds.clear()
        self.solveButton.config(state = DISABLED)
        self.browseFile.config(state = DISABLED)
        startTime = time()
        step = 0
        for state in AStar(self.matrix):
            self.updatecurrentInfor(startTime, step, state)
            self.prevReds = state.getRedSlots().getSlots()
            step += 1
            sleep(self.delayTime)
        self.solveButton.config(state=ACTIVE)
        self.browseFile.config(state=ACTIVE)