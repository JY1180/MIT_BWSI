import math
import tkinter as tk

from os.path import join
from PIL import ImageTk, Image

#from gameplay.scorekeeper import ScoreKeeper

class GameViewer(object):
    def __init__(self, root, filter_count, w, h, data_fp, humanoid):
        self.canvas = tk.Canvas(root, width=math.floor(0.5 * w), height=math.floor(0.75 * h))
        self.canvas.place(x=300, y=100)
        self.canvas.update()
        self.count = filter_count  # amount of people killed
        self.photo = None
        self.create_photo(join(data_fp, humanoid.fp))

    def delete_photo(self, event=None):
        self.canvas.delete('photo')

    def create_photo(self, fp):
        self.canvas.delete('photo')
        self.photo = display_photo(fp, self.count, self.canvas.winfo_width(), self.canvas.winfo_height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo, tags='photo')

    def display_score(self, score, scorekeeper):
        tk.Label(self.canvas, text="Game Stats", font=("Arial", 30)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Entities Killed: {}".format(score["killed"]), font=("Arial", 15)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Injured Humans Saved: {}".format(score["injured humans saved"]),
                 font=("Arial", 15)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Healthy Humans Saved: {}".format(score["healthy humans saved"]),
                 font=("Arial", 15)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Efficiency %: {}".format(round((score["correct moves"] / score["total moves"] * 100), 2)),
                 font=("Arial", 15)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Morality Score: {}".format(round(scorekeeper.display_morality(), 2)),
                 font=("Arial", 15)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Game Results", font=("Arial", 30)).pack(anchor=tk.NW)
        if score["squish count"] > score["skip count"]:
            tk.Label(self.canvas, text="You prefer to squish corpses instead of skipping.", font=("Arial", 15)).pack(anchor=tk.NW)
        if score["skip count"] > score["squish count"]:
            tk.Label(self.canvas, text="You prefer to skip corpses instead of squishing.", font=("Arial", 15)).pack(anchor=tk.NW)
        if score["act count"] > score["info count"] & score["suggest count"]:
            tk.Label(self.canvas, text="You prefer to use the act button rather than the info or suggest buttons.", font=("Arial", 15)).pack(anchor=tk.NW)
        if score["suggest count"] > score["act count"] & score["info count"]:
            tk.Label(self.canvas, text="You prefer to use the suggest button rather than the act or info buttons.", font=("Arial", 15)).pack(anchor=tk.NW)
        if score["info count"] > score["act count"] & score["suggest count"]:
            tk.Label(self.canvas, text="You prefer to use the info button rather than the act or suggest buttons.", font=("Arial", 15)).pack(anchor=tk.NW)
        if score["scram at high"] > score["scram at low"]:
            tk.Label(self.canvas, text="You prefer to scram at a high capacity rather than a low capacity.", font=("Arial", 15)).pack(anchor=tk.NW)
        if score["scram at low"] > score["scram at high"]:
            tk.Label(self.canvas, text="You prefer to scram at a low capacity rather than a high capacity.", font=("Arial", 15)).pack(anchor=tk.NW)
        if score["if paramedic"] > score["if protector"]:
            tk.Label(self.canvas, text="You prefer to save the threat rather than eliminating it.", font=("Arial", 15)).pack(anchor=tk.NW)
        if score["if paramedic"] < score["if protector"]:
            tk.Label(self.canvas, text="You prefer to eliminate the threat rather than saving it.", font=("Arial", 15)).pack(anchor=tk.NW)

def display_photo(img_path, inc, w, h):
    img = Image.open(img_path)
    if inc > 0:
        [xs, ys] = img.size
        for x in range(xs):
            for y in range(ys):
                [r, g, b] = img.getpixel((x, y))
                r = r + inc * 30  # the more kills, the more "bloody" the screen
                g = g - inc * 30
                b = b - inc * 30
                if r >= 255:  # max red value
                    r = 255
                if g <= 0:  # max g value
                    g = 0
                if b <= 0:  # max b value
                    b = 0
                value = (r, g, b)
                img.putpixel((x, y), value)  # changes image
    resized = img.resize((w, h), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(resized)
    return tk_img
