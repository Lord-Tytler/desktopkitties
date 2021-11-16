import tkinter as tk
import time
from PIL import Image, ImageTk
import pygame.time
from enum import IntEnum

class States(IntEnum):
    IDLE=0
    LEFT=1
    RIGHT=2

gifs = [
    Image.open("idle.gif"),
    Image.open("run_left.gif"),
    Image.open("run_right.gif"),
]

#window setup
window = tk.Tk()
window.config(bg='') #sets background to transparent
window.overrideredirect(True) #hides top bar
window.wm_attributes('-transparentcolor','blue') #makes anything that is BLUE transparent

#main fps and animation frame setup
clock = pygame.time.Clock() #use to set program fps
gameFrames = 0; #counting frames to regulate animation speed.
animationFrame = -1 #default animation frame, when next frame is called
#gif = Image.open("run.gif")
activeGif = gifs[0]
activeState = States.IDLE
stateQueued = False
nextState = States.IDLE

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
    if animationFrame >= activeGif.n_frames - 1:
        if stateQueued and nextState != activeState:
            changeState(nextState)
        else:
            animationFrame = -1
    activeGif.seek(animationFrame + 1)
    rgba = activeGif.convert('RGBA')
    rgba = rgba.resize((200, 200), Image.BOX)
    frameImg = ImageTk.PhotoImage(rgba)
    showImage(frameImg)
    return animationFrame + 1

#Given a desired stateIndex, sets activeState = stateIndex and sets activeGif to corresponding gif
def changeState(stateIndex):
    global activeGif
    global activeState
    global stateQueued
    global animationFrame
    activeState = stateIndex
    activeGif = gifs[stateIndex]
    animationFrame = -1
    stateQueued = False

#saves a given stateIndex into nextState and sets stateQueued=true so that the state and active gif will be changed after the current animation has finished
def queueStateChange(stateIndex):
    global stateQueued
    global nextState
    nextState = stateIndex
    stateQueued = True

#declares dragging state and offsets to default values (to be used for moving the window/cat)
dragging = False; 
offsetx = 0;
offsety = 0;

#if dragging is true (see startMove() and stopMove()), sets the top level's position to a prerecorded offset of the cursors current position
def move():
    if dragging:
        x, y = window.winfo_pointerxy()
        x -= offsetx
        y -= offsety
        window.geometry(f"+{x}+{y}")

#saves top level xy offset from cursor and sets dragging to true so move() runs
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





