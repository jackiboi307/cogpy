import sys
sys.path.append('..')
sys.path.append("C:\\Users\\jackj\\Documents\\python\\anaconda\\anaconda3\\Lib\\site-packages")
sys.path.append("c:\\users\\jackj\\appdata\\local\\programs\\python\\python38\\lib\\site-packages")
import cogpy

from random import randint

from colorama import Fore, Back, Style

canvas = cogpy.Canvas((100, 50))

print(end=cogpy.Escape.clear.full())

while True:
    cogpy.time.tick(60)
    
    canvas.fill(".", fg=Fore.BLUE, bg=Back.GREEN)

    canvas.draw.line((12, 5), (27, 43), "\\", st=Style.BRIGHT)

    canvas.draw.blit((10, 10), """hhhhhhhhhhh
thats a
good letter
dadadadadadadda
""", st=Style.NORMAL)

    canvas.draw.polygon(((30, 30), (40, 30), (40, 50), (40, 50)), cogpy.library.block_shades[0], fg=Fore.GREEN)

    canvas.render(True)
