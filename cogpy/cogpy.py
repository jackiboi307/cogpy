import os
from time import sleep
import string
from colorama import init
from math import sin, cos
from skimage.draw import *

init()


class _cogpyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def _err(msg):
    raise _cogpyError(msg)


class Escape:
    class _cursor:
        move = lambda x=0, y=0: f"\033[{y};{x}H"
        move1 = lambda x=0, y=0: f"\033[{y};{x}H"
        move2 = lambda x=0, y=0: f"\033[{y};{x}f"

        up = lambda value=1: f"\033[{value}A"
        down = lambda value=1: f"\033[{value}B"
        right = lambda value=1: f"\033[{value}C"
        left = lambda value=1: f"\033[{value}D"

        save = lambda: "\033[s"
        restore = lambda: "\033[u"

    class _clear:
        full = lambda: "\033[2J"
        line = lambda: "\033[K"

    cursor = _cursor
    clear = _clear


class _draw:
    def __init__(self, canvas):
        self._canvas = canvas

    # TODO - Implement a method for almost all functions in scikit_image._draw

    def pixel(self, pos, char):
        self._canvas._out[pos[1]][pos[0]][1] = str(char)

    @staticmethod
    def _convert(output):
        output = list(output)
        rr, cc = output[0], output[1]
        rr, cc = list(rr), list(cc)
        indexes = []
        for i in range(len(rr)):
            indexes.append((rr[i], cc[i]))
        return indexes

    def line(self, start_pos, end_pos, char):
        for i in self._convert(line(*start_pos, *end_pos)):
            self._canvas.draw.pixel(i, char)

    def polygon(self, points, char):
        def somefuncthathelpsme(z):
            x = []
            y = []
            for i in range(len(z)):
                x.append(z[i][0])
                y.append(z[i][1])
            return (x, y)

        for i in self._convert(polygon(*somefuncthathelpsme(points))):
            self._canvas.draw.pixel(i, char)

    def rect(self, start_pos, end_pos, char):
        # TODO - skimage._draw.rectangle acts wierd and i cant get it to work, use skimage._draw.polygon until it works
        pass

    def blit(self, pos, string, ignore=string.whitespace):
        string = list(map(lambda x: list(x), string.splitlines()))
        for y in range(len(string)):
            for x in range(len(string[y])):
                if string[y][x] not in ignore:
                    self._canvas.draw.pixel((x + pos[0], y + pos[1]), string[y][x])


class library:
    # TODO - ge denna sablans klass ett bättre namn!

    block_shades = ["█", "▓", "▒", "░"]

    @staticmethod
    def make_block(ul, ur, bl, br):
        return {"0000": " ",
                "0001": "▗",
                "0010": "▖",
                "0011": "▄",
                "0100": "▝",
                "0101": "▐",
                "0110": "▞",
                "0111": "▟",
                "1000": "▘",
                "1001": "▚",
                "1010": "▌",
                "1011": "▙",
                "1100": "▀",
                "1101": "▜",
                "1110": "▛",
                "1111": "█"
                }[str(int(ul)) + str(int(ur)) + str(int(bl)) + str(int(br))]


class Canvas:
    def __init__(self, size, bg=" ", flags=()):
        self._out = []
        for y in range(size[1]):
            self._out.append([])
            for x in range(size[0]):
                self._out[y].append([[], bg])

        self._size = size
        self._flags = flags

        self.draw = _draw(self)

    def render(self, colored=True, return_=False):
        out = ""
        for y in self._out:
            for x in range(len(y)):
                if colored:
                    out += "".join(y[x][0]) + y[x][1] + "\033[0m"
                else:
                    out += y[x][1]
            if y != len(y) - 1:
                out += "\n"
        if return_:
            return out
        else:
            print(Escape.cursor.up()*(len(self._out)), end=out)

    def fill(self, char):
        for y in range(len(self._out)):
            for x in range(len(self._out[y])):
                self._out[y][x][1] = char


class time:
    @staticmethod
    def tick(fps):
        sleep(1 / fps)
