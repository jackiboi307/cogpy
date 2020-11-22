from cogpy import *
from math import sin, cos  # circle animation
from random import choice

screen = Canvas((50, 25))
double_buffer = console.DoubleBuffer()

i = 0

while True:
    double_buffer.update()

    # screen.fill(" ")

    coords = (int(25 * (1 + sin(i))),
              int(12 * (1 + cos(i))))

    screen.draw.pixel(coords, choice(misc.ascii_shade_1))

    screen.render(False, double_buffer=double_buffer)

    i += .01
