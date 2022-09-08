# TODO: work fully in radians
# remove commented out code that is useless

import time
import math
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
from pimoroni import Button

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
display.set_backlight(1.0)

HEIGHT, WIDTH = display.get_bounds() # flipped as we use it horizontally

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

BLACK = display.create_pen(0,0,0)
WHITE = display.create_pen(255,255,255)

clamp = lambda x,min,max: min if x < min else (max if x > max else x)
'''
COS_X = {
    0:1.0,
    15:0.97,
    30:0.87,
    45:0.71,
    60:0.5,
    75:0.26,
    90:0.0,
    105:-0.26,
    120:-0.5,
    135:-0.71,
    150:-0.87,
    165:-0.97,
    180:-1.0,
    195:-0.97,
    210:-0.87,
    225:-0.71,
    240:-0.5,
    255:-0.26,
    270:-0.0,
    285:0.26,
    300:0.5,
    315:0.71,
    330:0.87,
    345:0.97
}

SIN_X = {
    0:0.0,
    15:0.26,
    30:0.5,
    45:0.71,
    60:0.87,
    75:0.97,
    90:1.0,
    105:0.97,
    120:0.87,
    135:0.71,
    150:0.5,
    165:0.26,
    180:0.0,
    195:-0.26,
    210:-0.5,
    225:-0.71,
    240:-0.87,
    255:-0.97,
    270:-1.0,
    285:-0.97,
    300:-0.87,
    315:-0.71,
    330:-0.5,
    345:-0.26
}
'''
# this function takes the screen as follows:
# 0,0 ____________________________
#  A |                            | X
#    |                            | 
#    |                            | 
#    |                            | 
#  B |                            | Y
#     ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯240, 135
def draw_vline(x, y1, y2, thickness):
    display.rectangle(y1,x,y2-y1,thickness)
    
# |x|
def modulus(x):
    if x < 0: return x*-1
    return x
# this function uses the values in COS_X table
# and finds the closest match
'''def acos(x):
    # print(x)
    min_dist = 1000
    winner = None
    for key,val in COS_X.items():
        d = modulus(x-val)
        if d < min_dist:
            min_dist = d
            winner = key
    return winner'''
    
# rotate a vertex by an angle upon a point
# as we use the point to find the radius,
# if many vertices use the same radius,
# that can be passed in instead to save computation
def rotate(v,a,p,r=None):
    if r: rad = r
    else: rad = math.sqrt(round( (v[0]-p[0])**2 + (v[1]-p[1])**2 ))
    a = round(a)
    while a%15:
        a+=1
    # using trigonometry to find the new position (SOHCAHTOA)
    inv = clamp((v[0] - p[0])/rad,-1,1)
    # current_angle = acos(inv)
    current_angle = math.degrees(math.acos(inv))
    if v[1] < p[1]:
        current_angle += 90 * ((2 * (inv < 0)) -1) # note if using tables to invert gt/lt
    nang = (a+current_angle) % 360
    nang = round(nang)
    while nang%15:
        nang+=1
    # print(nang)
    #new_x = rad * COS_X[nang] + p[0]
    #new_y = rad * SIN_X[nang] + p[1]
    new_x = rad * math.cos(math.radians(nang)) + p[0]
    new_y = rad * math.sin(math.radians(nang)) + p[1]
    return (new_x,new_y)
# draw a rectangle with left-top corner at x,y with
# width w and height h, rotated by angle a
# note: rotated rects (squares) are not filled
def draw_rect(x,y,w,h,a=0):
    overtices = [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
    center = (x+w/2, y + w/2)
    # MicroPython does not include list comprehension
    # vertices = [rotate(v,a,center) for v in vertices]
    vertices = []
    for v in overtices:
        vertices.append(rotate(v,a,center))
    if not a:
        vertices = overtices
    #c = 48
    #for v in vertices:
     #   display.character(c,int(v[1]),int(v[0]),1)
      #  c+=1
    for i in range(0,len(vertices)):
        if i: l = i-1
        else: l = len(vertices)-1
        display.line(
            int(vertices[i][1]),
            int(vertices[i][0]),
            int(vertices[l][1]),
            int(vertices[l][0])
            )
    return vertices
class Player:
    def __init__(self,x,y,sz):
        self.x = x
        self.y = y
        self.size = sz
        self.a = 0
        self.hsz = round(self.size/2)
        # self.vertices = [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
        # precomputing radius to not waste power
        # note that, as it is a square with equal side lengths,
        # we can take the original
        # math.sqrt(round( (v[0]-p[0])**2 + (v[1]-p[1])**2 ))
        # and simplify to self.size/2 * math.sqrt(2) = self.size/2 * 1.4142
        # self.r = self.size/2 * 1.4142
        # unused for now
    def move(self,power):
        # farg is arbitrary as it is used as ref point
        nx,ny = rotate((self.x + power,self.y),self.a,(self.x,self.y),power)
        self.x = nx
        self.y = ny
    def rotate(self,ang):
        self.a += ang
    def draw(self):
        draw_rect(self.x-self.hsz,self.y-self.hsz,self.size,self.size,self.a)
        # farg is arbitrary as it is used as ref point
        lx,ly = rotate((self.x + self.size*1.2,self.y),self.a,(self.x,self.y),self.size*1.2)
        display.line(round(self.y),round(self.x),round(ly),round(lx))
player = Player(50,50,10)
while True:
    display.set_pen(BLACK)
    display.clear()

    display.set_pen(WHITE)
    #draw_vline(0, 0, HEIGHT, 5);
    #draw_vline(50, 15, HEIGHT-15, 5);
    
    # draw_rect(100,50,5,5)
    # display.character(2+48,60,125,2)
    # display.character(5+48,70,125,2)
    player.draw()
    if button_a.read():
        player.move(5)
    if button_b.read():
        player.move(-5)
    if button_x.read():
        player.rotate(-5)
    if button_y.read():
        player.rotate(5)
    display.update()
    time.sleep(0.01)