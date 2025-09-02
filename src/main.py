import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Drawing App')
        
        self.canvas = tk.Canvas(self, width=600, height=400, background='white')
        self.pen_x = None
        self.pen_y = None

        self.canvas.bind('<Button-1>', lambda mouse: self.get_start(mouse))
        self.canvas.bind('<B1-Motion>', lambda mouse: self.paint(mouse))
        
        self.canvas.pack(fill='both')

    def get_start(self, mouse):
        self.pen_x = mouse.x
        self.pen_y = mouse.y

    def paint(self, mouse):
        self.canvas.create_line(self.pen_x, self.pen_y, mouse.x, mouse.y, capstyle='round', smooth=True, width=2)
        self.get_start(mouse)

root = Root()
root.mainloop()
