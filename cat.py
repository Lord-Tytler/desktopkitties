from enum import IntEnum

from window import Window

class States(IntEnum):
    IDLE=0
    LEFT=1
    RIGHT=2
    FALLING=3
    LANDING=4

class Cat:
    activeState = States.IDLE
    stateQueued = False
    nextState = States.IDLE
    win = Window()
    width = win.window.winfo_width()
    height = win.window.winfo_height()
    x, y = 0, 0
    velocity_x, velocity_y = 0, 0

    def nextFrame(self):
        if self.win.animationFrame >= self.win.activeGif.n_frames - 1:
            if self.activeState == States.FALLING or (self.activeState == States.LANDING and not self.stateQueued): #if landing with no state queued or falling, keep displaying last frame of gif
                self.win.animationFrame = self.win.activeGif.n_frames - 2
            elif self.stateQueued and self.nextState != self.activeState:
                self.changeState(self.nextState)
            else:
                self.win.animationFrame = -1
                print("resetting animation frame")
        self.win.nextFrame()
        
    
    def changeState(self, stateIndex):
        self.activeState = stateIndex
        self.win.setActiveGif(stateIndex)
        self.win.animationFrame = -1
        self.stateQueued = False
    
    def queueStateChange(self, stateIndex):
        self.nextState = stateIndex
        self.stateQueued = True

    def checkCollision(self):
        self.height = self.win.window.winfo_height()
        screen_height = self.win.window.winfo_screenheight()
        if self.y + self.height < screen_height and self.activeState != States.FALLING: #checks bottom of screen collision
            print("begin falling")
            self.changeState(States.FALLING)
        if self.y + self.height >= screen_height and self.activeState == States.FALLING: #checks if cat hits bottom of screen while falling
            a = self.y
            self.y = screen_height - self.height #sets cats y position to bottom of screen
            print("y before:", a, "y after", self.y, "height", self.height)
            self.changeState(States.LANDING)

    offsetx = 0;
    offsety = 0;
    dragging = False; 
    def moveCat(self, dt):
        if not self.win.dragButtonClicked:
            self.dragging = False
            self.checkCollision()
            match self.activeState:
                case States.IDLE:
                    self.velocity_x = 0
                case States.LEFT:
                    self.velocity_x = -10
                case States.RIGHT:
                    self.velocity_x = 10
                case States.FALLING:
                    self.velocity_y = 0.5 #TODO maybe gravity acceleration instead
                case States.LANDING:
                    self.velocity_y = 0
                    self.velocity_x = 0
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt
        elif self.win.dragButtonClicked and not self.dragging:
            px, py = self.win.window.winfo_pointerxy()
            self.offsetx = px - self.x
            self.offsety = py - self.y
        else:
            px, py = self.win.window.winfo_pointerxy()
            self.x = px - self.offsetx
            self.y = py - self.offsety

    
    def update(self, fps, frameCount, dt):
        self.moveCat(dt)
        if frameCount % (fps / 10) == 0: #TODO maybe incorporate different animation fps per gif. would be easy to attach an fps to each state, just will have to do some rounding
            self.nextFrame()
        self.win.update(self.x, self.y)

