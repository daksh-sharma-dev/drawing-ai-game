import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os
import time
from data_prep import convert_images
import joblib

class Root(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode('Light')
        self.configure(fg_color='#DADADA')

        self.title('Drawing App')
        self.geometry('600x400')
        self.resizable(False, False)

        self.canvas = Canvas(self, background='white', bd=2, relief='groove')
        self.options = Options(self, self.canvas, fg_color='transparent', height=300)
        
        self.canvas.pack(expand=True, fill='both')

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

class Options(ctk.CTkFrame):
    def __init__(self, master, canvas, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.canvas = canvas

        self.start_pos = 0
        self.end_pos = -0.1
        self.pos = self.start_pos
        self.visible = True

        self.save_button_image = ctk.CTkImage(light_image=Image.open(os.path.join('images', 'save_image.png')), size=(30,30))
        self.save_button = ctk.CTkButton(self, text='', height=0, width=0, image=self.save_button_image, fg_color='transparent', hover=False, border_color=None, command=lambda:self.save_image(('saved', 'drawing.png')))
        self.save_button.pack(side='left')

        self.clear_image = ctk.CTkImage(light_image=Image.open(os.path.join('images', 'clear.png')), size=(30,30))
        self.clear_button = ctk.CTkButton(self, text='', height=0, width=0, image=self.clear_image, fg_color='transparent', hover=False, border_color=None, command=lambda:self.clear_canvas())
        self.clear_button.pack(side='left')

        self.predict_button_image = ctk.CTkImage(light_image=Image.open(os.path.join('images', 'predict_image.png')), size=(30,30))
        self.predict_button = ctk.CTkButton(self, height=0, width=0, text='Predict', text_color='black', image=self.predict_button_image, fg_color='transparent', hover=False, border_color=None, command=lambda:self.predict_image())
        self.predict_button.pack(side='right')

        self.label = ctk.CTkLabel(self, text='')
        self.label.pack(side='bottom')

        self.place(relx=0, rely=self.pos, relwidth=1, relheight=0.1)

        self.menu_image = ctk.CTkImage(light_image=Image.open(os.path.join('images', 'up.png')), size=(10,10))
        self.menu_button = ctk.CTkButton(self.master, text='', image=self.menu_image, text_color='black', fg_color="transparent", bg_color='transparent', hover_color="#A3A2A2",
                                         command=lambda: self.animate())
        self.menu_button.place(relx=0.5, rely=0.1, anchor='n')


    def animate(self):
        if self.visible:
            self.move_up()
        else:
            self.move_down()

    def move_up(self):
        if self.pos >= self.end_pos:
            self.pos -= 0.005
            self.place(relx=0, rely=self.pos, relwidth=1)
            self.menu_button.place(relx=0.5, rely=0.1+self.pos, anchor='n')
            self.after(10, self.move_up)
        self.visible = False

    def move_down(self):
        if self.pos <= self.start_pos:
            self.pos += 0.005
            self.place(relx=0, rely=self.pos, relwidth=1)
            self.menu_button.place(relx=0.5, rely=0.1+self.pos, anchor='n')
            self.after(10, self.move_down)
        self.visible = True

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
        self.create_notification(y)

    def create_notification(self, text):
        self.notification_pos = 0.9
        self.notification_end_pos = 1.1
        self.notification = ctk.CTkLabel(self.master, text=text[0], text_color='red', width=100, height=25, fg_color='#e1dee3', bg_color='#ffffff', corner_radius=10)
        self.notification.place(relx=0.1, rely=self.notification_pos, anchor='center')
        #self.after(5000, self.remove_notification)
        self.after(1000, self.notification.destroy)

    def remove_notification(self):
        if self.notification_pos < self.notification_end_pos:
            self.notification_pos += 0.005
            self.notification.place(relx=0.1, rely=self.notification_pos, anchor='center')
            self.after(10, self.remove_notification)
        else:
            self.notification.destroy()

root = Root()
root.mainloop()
