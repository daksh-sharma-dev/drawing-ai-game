import tkinter as tk
from PIL import Image
import os

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Drawing App')
        self.geometry('600x400')

        self.canvas = Canvas(self, background='white')
        self.options = Options(self, self.canvas)

        self.options.pack(side='top', fill='x')
        self.canvas.pack(fill='both')
    

class Canvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.pen_x = None
        self.pen_y = None

        self.bind('<Button-1>', lambda mouse: self.get_start(mouse))
        self.bind('<B1-Motion>', lambda mouse: self.paint(mouse))

    def get_start(self, mouse):
        self.pen_x = mouse.x
        self.pen_y = mouse.y

    def paint(self, mouse):
        self.create_line(self.pen_x, self.pen_y, mouse.x, mouse.y, capstyle='round', smooth=True, width=2)
        self.get_start(mouse)

class Options(tk.Frame):
    def __init__(self, master, canvas, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.canvas = canvas

        self.save_button = tk.Button(self, text='Save', command=lambda:self.save_image())
        self.save_button.pack(side='left')

    def save_image(self):
        ps_file = 'temp_canvas.ps'
        self.canvas.postscript(file=ps_file, colormode='color')
        with Image.open(ps_file) as img: img.save('drawing.png', 'png')
        os.remove(ps_file)


root = Root()
root.mainloop()
