import tkinter as tk
from PIL import Image, ImageTk
import pygame.time
from enum import IntEnum

class States(IntEnum):
    IDLE=0
    LEFT=1
    RIGHT=2
    FALLING=3
    LANDING=4

gifs = [
    Image.open("idle.gif"),
    Image.open("run_left.gif"),
    Image.open("run_right.gif"),
    Image.open("falling.gif"),
    Image.open("landing.gif"), #TODO landing animation looks like it is floating. fix.
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
        if activeState == States.FALLING or (activeState == States.LANDING and not stateQueued):
            animationFrame = activeGif.n_frames - 2
            print("looping animation")
        elif stateQueued and nextState != activeState:
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
velocity_x = 0;
velocity_y = 0;

#if dragging is true (see startMove() and stopMove()), sets the top level's position to a prerecorded offset of the cursors current position
def dragWindow():
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
def tempStateChange(event):
    queueStateChange(States.RIGHT)
def tempStateChange2(event):
    queueStateChange(States.FALLING)    

window.bind('<Button-1>',startMove)
window.bind('<Button-2>',tempStateChange2)
window.bind('<Button-3>',tempStateChange)
window.bind('<ButtonRelease-1>', stopMove)

def checkCollision():
    screen_height = window.winfo_screenheight()
    x = window.winfo_x()
    y = window.winfo_y()
    h = window.winfo_height()
    if y + h < screen_height - 1 and activeState != States.FALLING: #checks bottom of screen collision
        changeState(States.FALLING)
    if y + h >= screen_height - 1 and activeState == States.FALLING: #checks if cat hits bottom of screen while falling
        y = screen_height - 1 - h #sets cats y position to bottom of screen
        changeState(States.LANDING)
        window.geometry(f"+{x}+{y}")


def moveCat(dt):
    global velocity_x
    global velocity_y
    checkCollision()
    match activeState:
        case States.IDLE:
            velocity_x = 0
        case States.LEFT:
            velocity_x = -10
        case States.RIGHT:
            velocity_x = 10
        case States.FALLING:
            velocity_y = 0.1 #TODO maybe gravity acceleration instead
        case States.LANDING:
            velocity_y = 0
            velocity_x = 0
    if not dragging:
        x = window.winfo_x()
        y = window.winfo_y()
        x += int(velocity_x * dt)
        y += int(velocity_y * dt)
        window.geometry(f"+{x}+{y}")



#main loop; updates window, iterates frame count, and iterates animation cycle every 1/10 of a second
while True:
    fps = 120 #TODO set fps to display refresh rate
    dt = 1000 / fps
    window.update()
    gameFrames += 1
    dragWindow()
    moveCat(dt)
    if gameFrames % (fps / 10) == 0: #TODO maybe incorporate different animation fps per gif. would be easy to attach an fps to each state, just will have to do some rounding
        animationFrame = nextFrame()
    window.update()
    clock.tick(fps) #uses pygame to maintain consistent fps.





