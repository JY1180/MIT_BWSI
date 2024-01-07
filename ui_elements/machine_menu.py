import tkinter as tk


class MachineMenu(object):
    def __init__(self, root, items):
        self.canvas = tk.Canvas(root, width=500, height=80)
        self.canvas.place(x=450, y=720)
        self.buttons = create_buttons(self.canvas, items)
        create_menu(self.buttons)

    def disable_buttons(self, remaining_time, at_capacity, too_many_zombies, filter_on=True):
        if filter_on:
            self.buttons[2].config(state="normal")
        else:
            self.buttons[2].config(state="disabled")
        if at_capacity or remaining_time <= 0 or too_many_zombies:
            self.buttons[0].config(state="disabled")
            self.buttons[1].config(state="disabled")
            self.buttons[2].config(state="disabled")
        else:
            self.buttons[0].config(state="normal")
            self.buttons[1].config(state="normal")


def create_buttons(canvas, items):
    buttons = []
    for item in items:
        (text, action) = item
        buttons.append(tk.Button(canvas, text=text, height=2, width=15,
                                 command=action))
    return buttons


def create_menu(buttons):
    for button in buttons:
        button.pack(side=tk.LEFT, padx=10)
