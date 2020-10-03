import os
import time as _time


class _cogpyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def _err(msg):
    raise _cogpyError(msg)


class draw:
    def __init__(self, canvas):
        self._canvas = canvas

    def pixel(self, pos, char):
        self._canvas._out[pos[1]][pos[0]][1] = str(char)

    def blit(self, pos, string):
        ...


class ascii:
    ...


class unicode:
    block_shades = ["█", "▓", "▒", "░"]

    @staticmethod
    def make_block(ul, ur, bl, br):
        code = str(int(ul)) + str(int(ur)) + str(int(bl)) + str(int(br))
        nums = ("0000",
                "0001",
                "0010",
                "0011",
                "0100",
                "0101",
                "0110",
                "0111",
                "1000",
                "1001",
                "1010",
                "1011",
                "1100",
                "1101",
                "1110",
                "1111")
        num = nums.index(code)
        return {0: " ",
                1: "▗",
                2: "▖",
                3: "▄",
                4: "▝",
                5: "▐",
                6: "▞",
                7: "▟",
                8: "▘",
                9: "▚",
                10: "▌",
                11: "▙",
                12: "▀",
                13: "▜",
                14: "▛",
                15: "█"
                }[num]


class Canvas:
    def __init__(self, size, bg=" ", flags=()):
        self._out = []
        for y in range(size[1]):
            self._out.append([])
            for x in range(size[0]):
                self._out[y].append([[], bg])

        self._size = size
        self._flags = flags

        self.draw = draw(self)

    def print(self, colored=True, renderer="r"):
        out = ""
        if renderer == "r":
            for y in self._out:
                for x in range(len(y)):
                    if colored:
                        out += "".join(y[x][0]) + y[x][1] + "\033[0m"
                    else:
                        out += y[x][1]
                if y != len(y) - 1: out += "\n"
            print(out, end="\r")

        if renderer == "os":
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

            for y in self._out:
                for x in range(len(y)):
                    if colored:
                        out += "".join(y[x][0]) + y[x][1] + "\033[0m"
                    else:
                        out += y[x][1]
                if y != len(y) - 1:
                    out += "\n"
            print(out)

    def fill(self, char):
        for y in range(len(self._out)):
            for x in range(len(self._out[y])):
                self._out[y][x][1] = char


class time:
    @staticmethod
    def tick(fps):
        _time.sleep(1 / fps)
