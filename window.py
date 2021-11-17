import tkinter as tk
from PIL import Image, ImageTk
import pygame.time
from enum import IntEnum

class Window:
    def __init__(self):
        self.window.bind('<B1-Motion>',self.dragClicked)
        self.window.bind('<ButtonRelease-1>', self.dragReleased)
    gifs = [
        Image.open("idle.gif"),
        Image.open("run_left.gif"),
        Image.open("run_right.gif"),
        Image.open("falling.gif"),
        Image.open("landing.gif"), #TODO landing animation looks like it is floating. fix.
    ]
    activeGif = gifs[0]
    animationFrame = -1 #default animation frame, when next frame is called

    #declares dragging state and offsets to default values (to be used for moving the window/cat)
    dragButtonClicked = False;
   

    #window setup
    window = tk.Tk()
    window.config(bg='') #sets background to transparent
    window.overrideredirect(True) #hides top bar
    window.wm_attributes('-transparentcolor','blue') #makes anything that is BLUE transparent
    

    

    #adds a passed iamge from nextFrame() to a label and places it on the top level
    def showImage(self, frame):
        for widget in self.window.winfo_children():
            widget.destroy()
        frame2 = frame
        img = tk.Label(image = frame2)
        img.config(bg='blue')
        img.image = frame2
        img.place(x=0, y=0)
        img.pack()
        self.window.update()

    #check which frame the animation should current be on, extracts and sends the next from to showImage() and returns updated frame number (previous + 1)
    def nextFrame(self):
        self.activeGif.seek(self.animationFrame + 1)
        rgba = self.activeGif.convert('RGBA')
        rgba = rgba.resize((200, 200), Image.BOX)
        frameImg = ImageTk.PhotoImage(rgba)
        self.showImage(frameImg)
        self.animationFrame += 1
    
    
    def dragClicked(self, event=None):
        self.dragButtonClicked = True
    def dragReleased(self, event=None):
        self.dragButtonClicked = False
    

    def setActiveGif(self, stateIndex):
        self.activeGif = self.gifs[stateIndex]

    def setWindowPos(self, x, y):
        self.window.geometry(f"+{x}+{y}")

    def update(self,x, y):
        #print(self.getDragButtonClicked())
        self.window.update()
        self.setWindowPos(int(x), int(y))
        