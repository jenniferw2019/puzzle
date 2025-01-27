#! /usr/local/bin/python3

import sys
import tkinter as tk

import game

###############################################################################

def main():

    try:
        N = int(sys.argv[1])
        assert N > 2
    except (AssertionError, IndexError, ValueError):
        N = 3

    try:
        image = sys.argv[2]
    except IndexError:
        image = 'crysis2.png'

    # tk.Tk() is the main window
    mypuzzle = game.puzzle(tk.Tk(), N, image)
    mypuzzle.mainloop()

###############################################################################

# calling main function here
if __name__ == '__main__':
    main()

