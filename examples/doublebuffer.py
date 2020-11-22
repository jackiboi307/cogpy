from cogpy import *
from math import sin, cos  # circle animation
from random import choice

screen = DoubleBufferCanvas((50, 25))

i = 0

while True:
    # screen.fill(" ")

    coords = (int(25 * (1 + sin(i))),
              int(12 * (1 + cos(i))))

    screen.draw.pixel(coords, choice(misc.ascii_shade_1))

    screen.render(False)

    i += .01
