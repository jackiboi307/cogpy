import sys
sys.path.append('..')
sys.path.append("C:\\Users\\jackj\\Documents\\python\\anaconda\\anaconda3\\Lib\\site-packages")
sys.path.append("c:\\users\\jackj\\appdata\\local\\programs\\python\\python38\\lib\\site-packages")

import cogpy

from random import randint

from colorama import Fore, Back, Style

canvas = cogpy.Canvas((100, 50))

cogpy.ready(True)

while True:
    cogpy.time.tick(60)
    
    canvas.fill(".", fg=Fore.YELLOW, bg=Back.BLUE, st=Style.BRIGHT)

    canvas.draw.line((12, 5), (27, 43), "\\", st=Style.BRIGHT)

    canvas.draw.blit((10, 10), """hhhhhhhhhhh
thats a
good letter
dadadadadadadda
""", fg=Fore.YELLOW, st=Style.BRIGHT)

    canvas.draw.polygon(((35, 30), (45, 30), (40, 50), (45, 40)), cogpy.library.block_shades[0], fg=Fore.BLUE, st=Style.BRIGHT)
    
    canvas.draw.rect((2, 2), (10, 10), "r", fg=Fore.YELLOW)

    canvas.render(True)
