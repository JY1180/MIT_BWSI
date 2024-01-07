import random
import tkinter as tk


class Paramedic(object):
    def __init__(self, root):
        self.serum_count = 3
        self.serum_canvas = tk.Canvas(root, width=175, height=100)
        self.serum_canvas.place(x=100, y=600)
        self.serum = []
        self.serum_size = 40
        self.serum_canvas.update()

    def update_serum(self):
        if self.serum_count > 0:
            self.serum_count -= 1
        chance = round(random.random(), 2)
        return chance

    def render_serum(self):
        tk.Label(self.serum_canvas, text="Paramedic", font=("Arial", 15)).place(x=50, y=10)

        x = 10
        y = 50
        for i in range(3):
            self.serum.append(create_serum_unit(self.serum_canvas, x, y, self.serum_size))
            x += self.serum_size * 1.5

    def update_fill(self, index):
        self.serum_canvas.itemconfig(self.serum[index], fill="", stipple="")  # removes serum


def create_serum_unit(canvas, x, y, size):
    return canvas.create_rectangle(x, y, x + size, y + size, fill="lightgreen", stipple="gray25")
