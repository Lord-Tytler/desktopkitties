import tkinter as tk
import time
from PIL import Image, ImageTk

window = tk.Tk()
window.config(highlightbackground='black')
window.overrideredirect(True) #hides top bar
window.wm_attributes('-transparentcolor','black') #makes top bar unusable

label = tk.Label(window,bd=0,bg='black')
label.pack()

greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()

load = Image.open("testcat.jpg")
render = ImageTk.PhotoImage(load)

img = tk.Label(image=render)
img.image = render
img.place(x=0, y=0)
img.pack()

dragging = False;
offsetx = 0;
offsety = 0;

def move(event):
    global dragging
    global offsetx
    global offsety
    if not dragging:
        x, y = window.winfo_pointerxy()
        offsetx = x - window.winfo_x()
        offsety = y - window.winfo_y()
        dragging = True
    
    if dragging:
        x, y = window.winfo_pointerxy()
        x -= offsetx
        y -= offsety
        window.geometry(f"+{x}+{y}")

def stopMove(event):
    global dragging
    global offsetx
    global offsety
    dragging = False;
    offsetx = 0;
    offsety = 0;

window.bind('<B1-Motion>',move)
window.bind('<ButtonRelease-1>', stopMove)
window.mainloop()





