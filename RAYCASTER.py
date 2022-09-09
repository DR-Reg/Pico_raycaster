# TODO: work fully in radians
# remove commented out code that is useless
# optimize collisions by only searching close blocks
import time
import math
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
LEVEL = """
########################
#      ###  #     #    #
####    ##    #####    #
#                      #
#                      #
#                      #
#                      #
#                      #
#                      #
#                      #
#                      #
########################"""

clamp = lambda x,min,max: min if x < min else (max if x > max else x)
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
COS_X = {
    0:1.0,5:1.0,10:0.98,15:0.97,20:0.94,25:0.91,30:0.87,35:0.82,40:0.77,45:0.71,50:0.64,55:0.57,60:0.5,65:0.42,70:0.34,75:0.26,80:0.17,85:0.09,90:0.0,95:-0.09,100:-0.17,105:-0.26,110:-0.34,115:-0.42,120:-0.5,125:-0.57,130:-0.64,135:-0.71,140:-0.77,145:-0.82,150:-0.87,155:-0.91,160:-0.94,165:-0.97,170:-0.98,175:-1.0,180:-1.0,185:-1.0,190:-0.98,195:-0.97,200:-0.94,205:-0.91,210:-0.87,215:-0.82,220:-0.77,225:-0.71,230:-0.64,235:-0.57,240:-0.5,245:-0.42,250:-0.34,255:-0.26,260:-0.17,265:-0.09,270:-0.0,275:0.09,280:0.17,285:0.26,290:0.34,295:0.42,300:0.5,305:0.57,310:0.64,315:0.71,320:0.77,325:0.82,330:0.87,335:0.91,340:0.94,345:0.97,350:0.98,355:1.0
}
SIN_X = {
    0:0.0,5:0.09,10:0.17,15:0.26,20:0.34,25:0.42,30:0.5,35:0.57,40:0.64,45:0.71,50:0.77,55:0.82,60:0.87,65:0.91,70:0.94,75:0.97,80:0.98,85:1.0,90:1.0,95:1.0,100:0.98,105:0.97,110:0.94,115:0.91,120:0.87,125:0.82,130:0.77,135:0.71,140:0.64,145:0.57,150:0.5,155:0.42,160:0.34,165:0.26,170:0.17,175:0.09,180:0.0,185:-0.09,190:-0.17,195:-0.26,200:-0.34,205:-0.42,210:-0.5,215:-0.57,220:-0.64,225:-0.71,230:-0.77,235:-0.82,240:-0.87,245:-0.91,250:-0.94,255:-0.97,260:-0.98,265:-1.0,270:-1.0,275:-1.0,280:-0.98,285:-0.97,290:-0.94,295:-0.91,300:-0.87,305:-0.82,310:-0.77,315:-0.71,320:-0.64,325:-0.57,330:-0.5,335:-0.42,340:-0.34,345:-0.26,350:-0.17,355:-0.09
}
def cos(x):
    return COS_X[x]
    # return math.cos(math.radians(x))
def sin(x):
    return SIN_X[x]
    # return math.sin(math.radians(x))
def acos(x):
    return math.degrees(math.acos(x))




# rotate a vertex by an angle upon a point
# as we use the point to find the radius,
# if many vertices use the same radius,
# that can be passed in instead to save computation
def rotate(v,a,p,r=None):
    if r: rad = r
    else: rad = math.sqrt(round( (v[0]-p[0])**2 + (v[1]-p[1])**2 ))
    # using trigonometry to find the new position (SOHCAHTOA)
    inv = clamp((v[0] - p[0])/rad,-1,1)
    current_angle = acos(inv)
    # current_angle = math.degrees(math.acos(inv))
    if v[1] < p[1]:
        current_angle += 90 * ((2 * (inv < 0)) -1) # note if using tables to invert gt/lt
    nang = (a+current_angle) % 360
    nang = nang - (nang%5)
    # print(nang)
    #new_x = rad * COS_X[nang] + p[0]
    #new_y = rad * SIN_X[nang] + p[1]
    new_x = rad * cos(nang) + p[0]
    new_y = rad * sin(nang) + p[1]
    return (new_x,new_y)
# draw a rectangle with left-top corner at x,y with
# width w and height h, rotated by angle a
# note: rotated rects (squares) are not filled
def draw_rect(x,y,w,h,a=0,draw=True):
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
    if not draw:
        return vertices
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
def colliding(v,x,y):
    # bounds = [x+BLOCK_SIZE/2,x-BLOCK_SIZE/2,y+BLOCK_SIZE/2,y-BLOCK_SIZE/2]
    bounds = [x,y,x+BLOCK_SIZE,y+BLOCK_SIZE]
    # DEBUG LINES:
    # display.set_pen(GREEN)
    # display.rectangle(y,x,BLOCK_SIZE,BLOCK_SIZE)
    for s in v:
        # display.rectangle(int(s[1]),int(s[0]),1,1)
        # display.set_pen(WHITE)
        if s[0] >= bounds[0] and s[0] <= bounds[2] and s[1] >= bounds[1] and s[1] <= bounds[3]:
            return True
    return False
class Player:
    def __init__(self,x,y,sz):
        self.x = x
        self.y = y
        self.size = sz
        self.a = 0
        self.hsz = round(self.size/2)
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
        oldx,oldy = self.x,self.y
        self.x = nx
        self.y = ny
        # collision detection, one step forward
        # overtices = [(self.x,self.y),(self.x+self.size,self.y),(self.x+self.size,self.y+self.size),(self.x,self.y+self.size)]
        # vertices = []
        # for v in overtices:
          #  vertices.append(rotate(v,self.a,(self.x+self.hsz,self.y+self.hsz)))
        # if not self.a:
         #   vertices = overtices
        vertices = draw_rect(self.x - self.hsz, self.y - self.hsz,self.size,self.size,self.a,False)
        ok = True
        for i,line in enumerate(LEVEL.split('\n')):
            for j,char in enumerate(line):
                bx,by = j*BLOCK_SIZE,i*BLOCK_SIZE
                if char == "#" and colliding(vertices,bx,by):
                    ok = False
                    break
            if not ok: break
        if not ok:
            print("COLLISION!")
            # mod = (2 * (power < 0)) - 1
            # nx,ny = rotate((self.x + mod*5,self.y),self.a,(self.x,self.y),mod*5)
            self.x = oldx
            self.y = oldy
            return
    def rotate(self,ang):
        self.a += ang
    def draw(self):
        draw_rect(self.x-self.hsz,self.y-self.hsz,self.size,self.size,self.a)
    def get_ray(self,rel_ang):
        ray_dist = BLOCK_SIZE/2
        # calculate curr angle only once as it doesn't change
        v = (self.x + ray_dist,self.y)
        p = (self.x,self.y)
        inv = clamp((v[0] - p[0])/ray_dist,-1,1)
        current_angle = acos(inv)
        if v[1] < p[1]:
            current_angle += 90 * ((2 * (inv < 0)) -1) # note if using tables to invert gt/lt
        nang = (self.a+current_angle+rel_ang) % 360
        nang = nang - (nang%5)
        while True:
            rx = ray_dist * cos(nang) + p[0]
            ry = ray_dist * sin(nang) + p[1]
            ray_dist += BLOCK_SIZE
            for i,line in enumerate(LEVEL.split('\n')):
                for j,char in enumerate(line):
                    bx,by = j*BLOCK_SIZE,i*BLOCK_SIZE
                    if char == "#" and colliding([(rx,ry)],bx,by):
                        return (rx,ry)
    def draw_ray(self):
        
        # farg is arbitrary as it is used as ref point
        i = -3
        while i < 3:
            lx,ly = self.get_ray(i*3)
            display.line(round(self.y),round(self.x),round(ly),round(lx))
            i += 1
#class Block:
 #   def __init__(self,x,y,sz):
player = Player(50,50,BLOCK_SIZE)
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
        
    for i,line in enumerate(LEVEL.split('\n')):
        for j,char in enumerate(line):
            if char == "#":
                display.rectangle(i*BLOCK_SIZE ,j*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE)
                
    display.set_pen(GREEN)
    player.draw_ray()
    display.update()
    time.sleep(0.01)