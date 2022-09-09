# TODO: collision detection with walls
import time
from math import sin, cos, pi, tan, sqrt, floor
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
from pimoroni import Button

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
display.set_backlight(1.0)

# 240X135
HEIGHT, WIDTH = display.get_bounds() # flipped as we use it horizontally

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

BLACK = display.create_pen(0,0,0)
WHITE = display.create_pen(255,255,255)
GREEN = display.create_pen(0,255,0)
RED = display.create_pen(255,0,0)
BLOCK_SIZE = 10
LEVEL = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
[1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
def draw_level():
    for  i,row in enumerate(LEVEL):
        for j,e in enumerate(row):
            if e: display.rectangle(i*BLOCK_SIZE,j*BLOCK_SIZE,BLOCK_SIZE-1,BLOCK_SIZE-1)
class Player:
    def __init__(self,x,y,sz=5):
        self.x = x
        self.y = y
        self.dx = cos(0)
        self.dy = sin(0)
        self.a = 0
        self.sz = sz
        self.hsz = sz/2
    def draw(self):
        display.rectangle(int(self.y-self.hsz),int(self.x-self.hsz),self.sz,self.sz)
        display.set_pen(GREEN)
        display.line(int(self.y),int(self.x),int(self.y+self.sz*2*self.dy),int(self.x+self.sz*2*self.dx))
    def move(self,k):
        self.x += k * self.dx
        self.y += k * self.dy
    def rotate(self,a):
        self.a += a
        if self.a < 0: self.a += 2*pi
        elif self.a > 2*pi: self.a -= 2*pi
        self.dx = cos(self.a)
        self.dy = sin(self.a)
    def draw_ray(self,rela):
        # vertical lines:
        # Taking o = dy and a = dx
        # then dividing both by dx
        # and multiplying by constant k,
        # we get a triangle where a = k,
        # o = dy/dx. Thanks to tan a = o/a,
        # dy/dx = o/a = tan a, so we can use
        # the angle to know how far a ray moves
        # upwards for k x-distance (where k is the
        # distance to the next vertical line in the grid)
        # as such we can move in a k increment first,
        # then move the ray in increments of block_size
        a = self.a + rela
        print(a/pi * 180,a,tan(a))
        vline = int(self.x / BLOCK_SIZE) + (a < pi/2 or a > 3*pi/2) # closest vertical line we are pointing at
                                                                    # i.e., if our angle is pointing right, add one
                                                                    # to floored value to get the vline to our right
                                                                    # else keep floored value as it is vline to our left
        k = (vline - self.x/BLOCK_SIZE) # distance to closest vertical line
        rx,ry = vline,int(self.y/BLOCK_SIZE) + (a < pi)
        if a == 0 or a == pi: m = 0
        else:m = tan(a) # tangent of angle = dy/dx
        dx,dy = k,k*m
        rx += dx
        ry += dy
        distance = sqrt(dx**2+dy**2)
        #print(rx,ry,self.x,self.y)
        k = 1 # now we are in a line, move x by blocksize
        if a == 0 or a == pi: dx,dy = k,0
        elif a > pi/2 and a < pi*3/2:dx,dy = -k,-k*m
        else: dx,dy = k,k*m
        dd = sqrt(dx**2+dy**2) # change in distance now constant as well
        print("RX/RY:",rx,ry,"M:",m,"DX/DY:",dx,dy)
        if ry > len(LEVEL) or rx > len(LEVEL[0]) or rx < 0 or ry < 0: collided = True
        else: collided = LEVEL[int(ry)][int(rx)]
        while not collided:
            rx += dx
            ry += dy
            print("RX/RY:",rx,ry,"M:",m,"DX/DY:",dx,dy)
            distance += dd
            if ry > len(LEVEL) or rx > len(LEVEL[0]) or rx < 0 or ry < 0: break
            collided = LEVEL[int(ry)][int(rx)]
        display.line(int(self.y),int(self.x),int(ry*BLOCK_SIZE),int(rx*BLOCK_SIZE))
            
        
player = Player(50,40)
while True:
    display.set_pen(BLACK)
    display.clear()

    display.set_pen(WHITE)
    draw_level()
    player.draw()
    player.draw_ray(0)
    if button_y.read():
        player.move(5)
    if button_x.read():
        player.move(-5)
    if button_b.read():
        player.rotate(-0.1)
    if button_a.read():
        player.rotate(0.1)
    display.update()
    time.sleep(0.01)