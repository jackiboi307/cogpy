from cogpy import *

screen = Canvas((50, 25))

while True:
    time.tick(30)  # FPS

    # update

    screen.fill(" ")

    # draw

    screen.render()
