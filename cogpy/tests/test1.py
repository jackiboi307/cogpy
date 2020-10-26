import sys
sys.path.append('..')
sys.path.append("C:\\Users\\jackj\\Documents\\python\\anaconda\\anaconda3\\Lib\\site-packages")
sys.path.append("c:\\users\\jackj\\appdata\\local\\programs\\python\\python38\\lib\\site-packages")
import cogpy

from random import randint

canvas = cogpy.Canvas((100, 50), bg=".")

print(end=cogpy.Escape.clear.full())

while True:
    cogpy.time.tick(60)
    
    canvas.fill(".")

    canvas.draw.line((12, 5), (27, 43), "\\")

    canvas.draw.blit((10, 10), """hhhhhhhhhhh
thats a
good letter
dadadadadadadda
""")

    canvas.draw.polygon(((30, 30), (40, 30), (40, 50), (40, 50)), cogpy.library.block_shades[0])

    canvas.render(False)
