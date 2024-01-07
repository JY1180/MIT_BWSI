import tkinter as tk
from tkinter import *
from tkinter.ttk import *


class Instructions(object):
    def __init__(self, root, items):
        self.canvas = tk.Canvas(root, width=500, height=80)
        self.canvas.place(x=550, y=25)
        self.buttons = create_buttons(self.canvas, items)
        create_menu(self.buttons)


def create_buttons(canvas, items):
    (text, action) = items
    button = tk.Button(canvas, text=text, height=2, width=15,
                       command=action)
    return button


def create_menu(buttons):
    buttons.pack(side=tk.LEFT, padx=10)
