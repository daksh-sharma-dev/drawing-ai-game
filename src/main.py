import tkinter as tk
from PIL import Image
import os
import time
from data_prep import convert_images
import joblib

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Drawing App')
        self.geometry('600x400')

        self.canvas = Canvas(self, background='white')
        self.options = Options(self, self.canvas)

        self.options.pack(side='top', fill='both')
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

        self.save_button = tk.Button(self, text='Save', command=lambda:self.save_image(('saved', 'drawing.png')))
        self.save_button.pack(side='left')

        self.clear_button = tk.Button(self, text='Clear', command=lambda:self.clear_canvas())
        self.clear_button.pack(side='left')

        self.predict_button = tk.Button(self, text='Predict', command=lambda:self.predict_image())
        self.predict_button.pack(side='left')

        self.label = tk.Label(self, text='')
        self.label.pack(side='bottom')

    def save_image(self, destination):
        ps_file = 'temp_canvas.ps'
        self.canvas.postscript(file=ps_file, colormode='color')
        # filepath = os.path.join('data', 'triangle', f'triangle_{int(time.time())}.png')
        filepath = os.path.join('data', destination[0], destination[1])
        with Image.open(ps_file) as img: img.save(filepath, 'png')
        os.remove(ps_file)

    def clear_canvas(self):
        self.canvas.delete('all')

    def predict_image(self):
        self.save_image(('temporary', 'temp.png'))
        X, y = convert_images((28,28), ['temporary'])
        model = joblib.load(os.path.join('models', 'knn_model.pkl'))
        y = model.predict(X)
        self.label.configure(text=y)

root = Root()
root.mainloop()
