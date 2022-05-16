from AStar import AStar
from readFile import readFile
import tkinter as tk
from gui import GUI 
from time import time


def main():
    root = tk.Tk()
    root.geometry('600x800')
    root.wm_minsize(600, 800)
    root.wm_maxsize(600, 800)
    GUI(root)
    root.mainloop()


def mainTest():
    nodes = readFile('input.txt')
    start = time()
    with open("output.txt", 'w') as writer:
        for s in AStar(nodes):
            writer.write(str(s.getRedSlots().getSlots()) + '\n')
        print(f"Time: {time() - start}")


main()
