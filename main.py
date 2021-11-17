import pygame.time

from cat import Cat

cat1 = Cat()
#main fps and animation frame setup
clock = pygame.time.Clock() #use to set program fps
frameCount = 0; #counting frames to regulate animation speed.

#main loop; updates window, iterates frame count, and iterates animation cycle every 1/10 of a second
while True:
    fps = 120 #TODO set fps to display refresh rate
    dt = 1000 / fps
    frameCount += 1
    cat1.update(fps, frameCount, dt)
    clock.tick(fps) #uses pygame to maintain consistent fps.
