import tkinter as tk
import time
from PIL import Image, ImageTk
from PIL import GifImagePlugin
import pygame.time

window = tk.Tk()
window.config(bg='') #sets background to transparent
window.overrideredirect(True) #hides top bar
window.wm_attributes('-transparentcolor','blue') #makes anything that is BLUE transparent

clock = pygame.time.Clock() #use to set program fps
gameFrames = 0; #counting frames to regulate animation speed.
gif = Image.open("run.gif")
animationFrame = -1

#adds a passed iamge from nextFrame() to a label and places it on the top level
def showImage(frame):
    for widget in window.winfo_children():
       widget.destroy()
    frame2 = frame
    img = tk.Label(image = frame2)
    img.config(bg='blue')
    img.image = frame2
    img.place(x=0, y=0)
    img.pack()
    window.update()

#check which frame the animation should current be on, extracts and sends the next from to showImage() and returns updated frame number (previous + 1)
def nextFrame():
    global animationFrame
    if animationFrame >= gif.n_frames - 1:
        animationFrame = -1
    gif.seek(animationFrame + 1)
    rgba = gif.convert('RGBA')
    rgba = rgba.resize((200, 200), Image.BOX)
    frameImg = ImageTk.PhotoImage(rgba)
    showImage(frameImg)
    return animationFrame + 1


dragging = False;
offsetx = 0;
offsety = 0;

#when first clicked, saves windows offset from cursor, then sets the window to that same offset as cursor moves such that user can "grab" any spot on window
def move():
    #global dragging
    #global offsetx
    #global offsety
    if dragging:
        x, y = window.winfo_pointerxy()
        x -= offsetx
        y -= offsety
        window.geometry(f"+{x}+{y}")

def startMove(event):
    global dragging
    global offsetx
    global offsety
    if not dragging:
        x, y = window.winfo_pointerxy()
        offsetx = x - window.winfo_x()
        offsety = y - window.winfo_y()
        dragging = True

#resets cursor offset positions when button is released
def stopMove(event):
    global dragging
    global offsetx
    global offsety
    dragging = False;
    offsetx = 0;
    offsety = 0;

window.bind('<Button-1>',startMove)
window.bind('<ButtonRelease-1>', stopMove)

#main loop; updates window, iterates frame count, and iterates animation cycle every 1/10 of a second
while True:
    fps = 120
    window.update()
    gameFrames += 1
    move()
    if gameFrames % (fps / 10) == 0:
        animationFrame = nextFrame()
    clock.tick(fps) #uses pygame to maintain consistent fps.





