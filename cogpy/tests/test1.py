import sys 
sys.path.append('..')
import cogpy as cog

console = cog.Console((60, 48))

while True:
    cog.time.tick(1)
    
    console.clear()
    
    console.draw.pixel((2, 2), "*")
    
    console.flip()
    
    break