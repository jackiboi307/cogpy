from cogpy import *
from colorama import Fore, Back

screen = Canvas((50, 25))

while True:
    time.tick(30)  # FPS

    # update

    screen.fill(" ")

    # draw

    screen.draw.rect((5, 5), (45, 20), "'", fg=Fore.BLUE, bg=Back.BLUE)
    screen.draw.line((23, 5), (23, 18), "|", fg=Fore.YELLOW, bg=Back.YELLOW)
    screen.draw.line((24, 5), (24, 18), "|", fg=Fore.YELLOW, bg=Back.YELLOW)
    screen.draw.put((23, 19), "\\/", fg=Fore.YELLOW, bg=Back.YELLOW)
    screen.draw.line((5, 12), (43, 12), "-", fg=Fore.YELLOW, bg=Back.YELLOW)
    screen.draw.line((5, 11), (43, 11), "-", fg=Fore.YELLOW, bg=Back.YELLOW)
    screen.draw.put((44, 11), "|\n|", fg=Fore.YELLOW, bg=Back.YELLOW)

    # render

    screen.render(colored=True)
