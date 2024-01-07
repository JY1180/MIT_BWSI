import tkinter as tk

class Protector():
    def __init__(self, root):
        self.health = 3
        self.lives_canvas = tk.Canvas(root, width=175, height=100)
        self.lives_canvas.place(x=100, y=500)
        self.lives_canvas.update()
        self.lives_size = 40
        self.lives = []
        
    def kill(self):
        if self.health > 0:
            self.health = self.health - 1
        return self.health

    def render_lives(self):
        tk.Label(self.lives_canvas, text="Protector", font=("Arial", 15)).place(x=50, y=10)

        x = 10
        y = 50
        for i in range(3):
            self.lives.append(create_lives(self.lives_canvas, x, y, self.lives_size))
            x += self.lives_size * 1.5

    def update_fill(self, index):
        self.lives_canvas.itemconfig(self.lives[index], fill="black", stipple="")  


def create_lives(canvas, x, y, size):
    return canvas.create_rectangle(x, y, x + size, y + size, fill="green", stipple="")