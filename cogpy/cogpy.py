"""
Cogpy 0.2.1
"""

from os import name
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


def printnln(*args, **kwargs):
    kwargs["end"] = ""
    print(*args, **kwargs)


def ready(check=True):
    if name == "posix" and check:
        printnln(Escape.cursor.hide())
        printnln(Escape.clear.full())


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

        hide = lambda: "\033[?25l"
        show = lambda: "\033[?25h"

    class _clear:
        full = lambda: "\033[2J"
        line = lambda: "\033[K"

    cursor = _cursor
    clear = _clear


class _getindexes:
    # TODO - Implement a method for almost all functions in scikit_image._draw

    @classmethod
    def _convert(cls, output):
        output = list(output)
        rr, cc = output[0], output[1]
        rr, cc = list(rr), list(cc)
        indexes = []
        for i in range(len(rr)):
            indexes.append((rr[i], cc[i]))
        return indexes

    @classmethod
    def line(cls, start_pos, end_pos):
        return cls._convert(line(*start_pos, *end_pos))

    @classmethod
    def polygon(cls, points):
        def rc_to_2d(z):
            x = []
            y = []
            for i in range(len(z)):
                x.append(z[i][0])
                y.append(z[i][1])
            return (x, y)

        return cls._convert(polygon(*rc_to_2d(points)))

    @classmethod
    def rect(cls, start_pos, end_pos):
        return cls.polygon((start_pos, (start_pos[0], end_pos[1]), end_pos, (end_pos[0], start_pos[1])))


class _draw:
    def __init__(self, canvas):
        self._canvas = canvas

    def pixel(self, pos, char, fg="", bg="", st=""):
        self._canvas._out[pos[1]][pos[0]][1] = char
        self._canvas.paint.pixel(pos, fg, bg, st)

    def line(self, start_pos, end_pos, char, fg="", bg="", st=""):
        for i in _getindexes.line(start_pos, end_pos):
            self._canvas.draw.pixel(i, char, fg, bg, st)

    def polygon(self, points, char, fg="", bg="", st=""):
        for i in _getindexes.polygon(points):
            self._canvas.draw.pixel(i, char, fg, bg, st)

    def rect(self, start_pos, end_pos, char, fg="", bg="", st=""):
        for i in _getindexes.rect(start_pos, end_pos):
            self._canvas.draw.pixel(i, char, fg, bg, st)

    def blit(self, pos, string, ignore=string.whitespace, fg="", bg="", st=""):
        string = list(map(lambda x: list(x), string.splitlines()))
        for y in range(len(string)):
            for x in range(len(string[y])):
                if string[y][x] not in ignore:
                    self._canvas.draw.pixel((x + pos[0], y + pos[1]), string[y][x], fg, bg, st)


class _paint:
    def __init__(self, canvas):
        self._canvas = canvas

    def pixel(self, pos, fg="", bg="", st=""):
        c = (fg, bg, st)
        for i in range(len(c)):
            if c[i] != "":
                self._canvas._out[pos[1]][pos[0]][0][i] = c[i]

    def line(self, start_pos, end_pos, fg="", bg="", st=""):
        for i in _getindexes.line(start_pos, end_pos):
            self._canvas.paint.pixel(i, fg, bg, st)

    def rect(self, start_pos, end_pos, fg="", bg="", st=""):
        for i in _getindexes.rect(start_pos, end_pos):
            self._canvas.paint.pixel(i, fg, bg, st)

    def polygon(self, points, fg="", bg="", st=""):
        for i in _getindexes.polygon(points):
            self._canvas.paint.pixel(i, fg, bg, st)


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
    def __init__(self, size, flags=()):
        self._out = []
        for y in range(size[1]):
            self._out.append([])
            for x in range(size[0]):
                self._out[y].append([["", "", ""], " "])

        self._size = size
        self._flags = flags

        self.draw = _draw(self)
        self.paint = _paint(self)

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
            printnln(Escape.cursor.up()*len(self._out))
            printnln(out)

    def fill(self, char=None, fg="", bg="", st=""):
        c = (fg, bg, st)
        for y in range(len(self._out)):
            for x in range(len(self._out[y])):
                if char is not None:
                    self._out[y][x][1] = char
                for i in range(len(c)):
                    if c[i] != "":
                        self._out[y][x][0][i] = c[i]


class time:
    @staticmethod
    def tick(fps):
        sleep(1 / fps)
