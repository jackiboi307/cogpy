import sys 
sys.path.append('..')
import cogpy as cog

canvas = cog.Canvas((100, 100), bg=".")

while True:
    cog.time.tick(1)
    
    canvas.fill(".")

    canvas.print(False, "r")

    pos[0] -= 1
    pos[1] -= 1