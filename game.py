#! /usr/local/bin/python3

import cv2
import itertools
import numpy as np
import os
import random
import tkinter as tk
import tkinter.messagebox as mb

###############################################################################

pad = 10
imsize = 600

###############################################################################

class puzzle(tk.Frame): # class puzzle inherit from tk.Frame
    '''
    Display a sliding puzzle using a square image. Said square image is divided
    into smaller square sub-images, according to the argument provided to the
    constructor. All sub-images are then resized so that the final puzzle is
    `imsize' wide and `imsize' high. They are then saved to the disk, so that they
    can be used the next time this program is run. The input image must be square
    in shape for this to work as expected.

    Each sub-image is put on a button, which, when clicked, will move to the empty
    slot if possible. The spacing between the sub-images can be controlled by
    changing `pad'.

    All sub-images must be bound to a class member variable (`images') before
    putting them on the buttons. Otherwise, the garbage collector deletes them
    before they can be used.

    Attributes:
        N: int (maximum number of sub-images per row or column)
        images: list (list of sub-images)
        buttons: list (list of buttons the sub-images are drawn on)
        vacant: tuple (indicates which location is currently vacant)
        monitor_status: bool (whether or not to show success message on completion)
        moves: int (how many moves the user has made)

    Methods:
        __init__    This is like the constructor in Java or C++
        move:       move the indicated sub-image to the vacant slot if possible
        randomise:  randomly call `move' a large number of times
    '''

    def __init__(self, parent, N = 3, image = 'crysis2.png'):   # N and image are arguments with default values
        tk.Frame.__init__(self, parent)
        self.grid(padx = pad, pady = pad)
        self.N = N
        self.images = []
        self.buttons = []
        self.vacant = (self.N - 1, self.N - 1)
        self.monitor_status = False
        self.moves = 0
        self.count_label = tk.Label(self)

        parent.title('Sliding Puzzle')
        parent.resizable(False, False)

        # check if images are already available
        # if not, create the images and save them for future use
        try:
            for i in range(self.N ** 2 - 1):
                # 'with' statement will automatically release files once its usage is complete
                # {i:03d} means to add leading 0s to number i, total three digits
                # f'img{i:03d}.png' is the f-strings syntax in Python
                with open(f'img{i:03d}.png'):
                    pass    # same as do nothing
        except FileNotFoundError:
            # cv2.imread() return image matrix in the form of numpy.ndarray class
            img = cv2.imread(image)
            # itertools.product() is used to find the cartesian product of two sets
            # [: -1] all elements except the last one. -1 is the negative indexing, which means the last element
            for i, (r, c) in enumerate(list(itertools.product(range(self.N), range(self.N)))[: -1]):
                h_step = img.shape[0] // self.N     # img.shape[0] is the height of the image
                v_step = img.shape[1] // self.N     # img.shape[1] is the width of the image
                # slicing the original image into N x N grid, and resize the cropped piece to fit the window
                img_crop = img[r * h_step : (r + 1) * h_step, c * v_step : (c + 1) * v_step]
                img_crop = cv2.resize(img_crop, (imsize // self.N, imsize // self.N))
                cv2.imwrite(f'img{i:03d}.png', img_crop)
        finally:
            for i, (r, c) in enumerate(list(itertools.product(range(self.N), range(self.N)))[: -1]):
                # use tk.PhotoImage() to get image object
                self.images.append(tk.PhotoImage(file = f'img{i:03d}.png'))
                # use tk.Button() to add image on button
                button = tk.Button(self, image = self.images[i])
                # button['command'] assigns a command to the 'command' attribute of a button widget
                # 'Lambda _button = button' This is a lambda function whic is a anonymous function in Python
                # '_button = button' initializes the local variable _button with the current value of 'button'
                # 'self.move(_button)' is the function that will be executed when the buttuon is clicked
                button['command'] = lambda _button = button: self.move(_button)
                # button.grid() arrange button into specified row and column
                button.grid(row = r, column = c)
                self.buttons.append(button)

        randomise_button = tk.Button(self, text = 'Start', command = self.randomise)
        #randomise_button.grid(row = self.N, columnspan = self.N, pady = (4 * pad, pad))
        randomise_button.grid(row = self.N, column = 0, pady = (2 * pad, pad))

        self.count_label = tk.Label(self, text = "moves: 0")
        self.count_label.grid(row = self.N, column = 1, pady = (2 * pad, pad))

        reset_button = tk.Button(self, text = 'Reset', command = self.reset)
        reset_button.grid(row = self.N, column = 2, pady = (2 * pad, pad))

    ########################################

    def move(self, _button):
        '''
        Compare the position of the sub-image to be moved with the position of the
        vacant slot. If they are adjacent to each other, interchange their positions.

        Args:
        _button: tkinter.Button (the sub-image to be moved)
        '''

        vacant_row, vacant_column = self.vacant     # the vacant spot is initialized at (2, 2)
        # get row and column value of clicked button
        button_row, button_column = tuple(map(_button.grid_info().get, ('row', 'column')))
        if set((abs(vacant_row - button_row), abs(vacant_column - button_column))) == {0, 1}: # adjacent to each other
            _button.grid(row = vacant_row, column = vacant_column)
            self.vacant = (button_row, button_column)

        # increment counter only if the game is being monitored
        # show the move counts in count_label
        if self.monitor_status:
            self.moves += 1
            count_text = "moves: " + str(self.moves)
            self.count_label.configure(text = count_text)

            # upon completion, stop monitoring
            # The expression inside all() is called python generator expression used to generate interable object
            # which is passed as parameter into function all()
            if all(i == button.grid_info().get('row') * self.N + button.grid_info().get('column') for i, button in enumerate(self.buttons)):
                self.monitor_status = False
                mb.showinfo(title = 'Puzzle Solved!', message = f'You have solved the puzzle in {self.moves} moves!')

    ########################################

    def randomise(self):
        '''
        Move the sub-images randomly.
        '''

        # start monitoring the game only after this function is called
        # i.e. after the user clicks the button to randomise the sub-images
        self.monitor_status = False
        for button in random.choices(self.buttons, k = 1000 * self.N):
            self.move(button)
        self.monitor_status = True
        self.moves = 0
        self.count_label.configure(text = "moves: 0")

    def reset(self):
        """
        Reset the puzzle to its initial configuration.
        """
        for i, button in enumerate(self.buttons):
            #row, column = divmod(i, self.N)
            row = i // self.N
            column = i % self.N
            button.grid(row=row, column=column)
        self.vacant = (self.N - 1, self.N - 1)
        self.monitor_status = False
        self.moves = 0
        self.count_label.configure(text = "moves: 0")

