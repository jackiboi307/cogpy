"""
Cogpy 1.4.3
"""

import string
from time import sleep

import win32con
import win32console
from colorama import init
from skimage.draw import *

from color_names import color_names

init()


class _cogpyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def _err(msg):
    raise _cogpyError(msg)


def printnln(*args, **kwargs):
    kwargs["end"] = ""
    print(*args, **kwargs)


class color:
    class name:
        @classmethod
        def __getattr__(cls, item):
            return color_names[item.upper()]


class escape:
    class cursor:
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

    class clear:
        full = lambda: "\033[2J"
        line = lambda: "\033[K"


class _draw:
    def __init__(self, surface):
        self._surface = surface

    def pixel(self, pos, char, fg="", bg=""):
        if (0 <= pos[0] < self._surface._size[0]) and (0 <= pos[1] < self._surface._size[1]):
            if char is not None:
                self._surface._out[pos[1]][pos[0]][1] = char
            c = (fg, bg)
            for i in range(len(c)):
                if c[i] is not None:
                    self._surface._out[pos[1]][pos[0]][0][i] = c[i]

    def line(self, start_pos, end_pos, char, fg="", bg=""):
        for pos in zip(*line(*start_pos, *end_pos)):
            self._surface.draw.pixel(pos, char, fg, bg)

    def polygon(self, points, char, fg="", bg=""):
        def unzip(z):
            x = []
            y = []
            for i in range(len(z)):
                x.append(z[i][0])
                y.append(z[i][1])
            return x, y

        for pos in zip(*polygon(*unzip(points))):
            self._surface.draw.pixel(pos, char, fg, bg)

    def rect(self, start_pos, end_pos, char, fg="", bg=""):
        self._surface.draw.polygon((start_pos, (start_pos[0], end_pos[1]), end_pos, (end_pos[0], start_pos[1])), char, fg, bg)

    def put(self, pos, content, ignore=string.whitespace, fg="", bg=""):
        if type(content) not in (list, tuple):
            content = list(map(lambda x: list(x), content.splitlines()))
        for y in range(len(content)):
            for x in range(len(content[y])):
                if content[y][x] not in ignore:
                    if (0 <= x < self._surface._size[0]) and (0 <= y < self._surface._size[1]):
                        self._surface.draw.pixel((x + pos[0], y + pos[1]), content[y][x], fg, bg)


class misc:
    # TODO - ge denna sablans klass ett bättre namn!

    block_shade = "█▓▒░ "
    ascii_shade_1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    ascii_shade_2 = "@%#*+=-:. "

    @staticmethod
    def make_block(ul, ur, bl, br):
        return {"0000": " ", "0001": "▗", "0010": "▖", "0011": "▄", "0100": "▝", "0101": "▐", "0110": "▞", "0111": "▟",
                "1000": "▘", "1001": "▚", "1010": "▌", "1011": "▙", "1100": "▀", "1101": "▜", "1110": "▛", "1111": "█"}[
            str(int(ul)) + str(int(ur)) + str(int(bl)) + str(int(br))]


class Surface:
    def __init__(self, size):
        self._out = []
        for y in range(size[1]):
            self._out.append([])
            for x in range(size[0]):
                self._out[y].append([["", ""], " "])

        self._size = size

        self.draw = _draw(self)

    def fill(self, char=None, fg="", bg=""):
        c = (fg, bg)
        for y in range(len(self._out)):
            for x in range(len(self._out[y])):
                if char is not None:
                    self._out[y][x][1] = char
                for i in range(len(c)):
                    if c[i] is not None:
                        self._out[y][x][0][i] = c[i]


class Canvas(Surface):
    def __init__(self, size, surface=None):
        super().__init__(size)
        if surface is not None:
            self._out = surface._out

    def render(self, colored=True, give=False, text=True):
        out = ""
        for y in self._out:
            for x in range(len(y)):
                out += ("".join(y[x][0]) if colored else "") + (y[x][1] if text else "") + ("\033[0m" if colored else "")
            if y != len(y) - 1:
                out += "\n"
        if give:
            return out
        else:
            printnln(escape.cursor.up(len(self._out)) + out)

    def blit(self, surface, pos):
        for y in range(len(surface._out)):
            for x in range(len(surface._out[y])):
                self._out[pos[1] + y][pos[0] + x] = surface[pos[1] + y][pos[0] + x]

    @classmethod
    def render_canvasses(cls, *args):
        options = args[-1]
        canvasses = list(args)
        del args
        del canvasses[-1]

        for canvas in canvasses:
            if options is None:
                canvas.render()
            else:
                canvas.render(**options)


class DoubleBufferCanvas(Canvas):
    def __init__(self, size):
        super().__init__(size)

        printnln(escape.clear.full())

        # gamla linjen
        def draw_pixel(self_, pos, char, fg="", bg=""):
            self_.ns.WriteConsoleOutputCharacter(char, win32console.PyCOORDType(*pos))
            self_.ns.WriteConsoleOutputAttribute((fg, bg), win32console.PyCOORDType(*pos))
        self.draw.pixel = draw_pixel

        stdcon = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
        self.active_screen = 0
        self.screens = [
            win32console.CreateConsoleScreenBuffer(DesiredAccess=win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                                                   ShareMode=0, SecurityAttributes=None, Flags=1),
            win32console.CreateConsoleScreenBuffer(DesiredAccess=win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                                                   ShareMode=0, SecurityAttributes=None, Flags=1)
        ]

        self.screens[self.active_screen].SetConsoleActiveScreenBuffer()
        self.cursor_size, _ = stdcon.GetConsoleCursorInfo()
        self.next_screen = 1 - self.active_screen
        self.ns = self.screens[self.next_screen]
        self.ns.SetConsoleActiveScreenBuffer()

    def show_cursor(self):
        for it in self.screens:
            it.SetConsoleCursorInfo(self.cursor_size, True)

    def hide_cursor(self):
        for it in self.screens:
            it.SetConsoleCursorInfo(self.cursor_size, False)

    def flip(self):
        self.next_screen = 1 - self.active_screen
        self.ns = self.screens[self.next_screen]
        self.ns.SetConsoleActiveScreenBuffer()


class time:
    @staticmethod
    def tick(fps):
        sleep(1 / fps)
