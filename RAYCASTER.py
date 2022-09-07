import time
import random
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
display.set_backlight(1.0)

HEIGHT, WIDTH = display.get_bounds() # flipped as we use it horizontally

BLACK = display.create_pen(0,0,0)
WHITE = display.create_pen(255,255,255)

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

SQRT = {0:0.0,1:1.0,2:1.41,3:1.73,4:2.0,5:2.24,6:2.45,7:2.65,8:2.83,9:3.0,10:3.16,11:3.32,12:3.46,13:3.61,14:3.74,15:3.87,16:4.0,17:4.12,18:4.24,19:4.36,20:4.47,21:4.58,22:4.69,23:4.8,24:4.9,25:5.0,26:5.1,27:5.2,28:5.29,29:5.39,30:5.48,31:5.57,32:5.66,33:5.74,34:5.83,35:5.92,36:6.0,37:6.08,38:6.16,39:6.24,40:6.32,41:6.4,42:6.48,43:6.56,44:6.63,45:6.71,46:6.78,47:6.86,48:6.93,49:7.0,50:7.07,51:7.14,52:7.21,53:7.28,54:7.35,55:7.42,56:7.48,57:7.55,58:7.62,59:7.68,60:7.75,61:7.81,62:7.87,63:7.94,64:8.0,65:8.06,66:8.12,67:8.19,68:8.25,69:8.31,70:8.37,71:8.43,72:8.49,73:8.54,74:8.6,75:8.66,76:8.72,77:8.77,78:8.83,79:8.89,80:8.94,81:9.0,82:9.06,83:9.11,84:9.17,85:9.22,86:9.27,87:9.33,88:9.38,89:9.43,90:9.49,91:9.54,92:9.59,93:9.64,94:9.7,95:9.75,96:9.8,97:9.85,98:9.9,99:9.95,100:10.0,101:10.05,102:10.1,103:10.15,104:10.2,105:10.25,106:10.3,107:10.34,108:10.39,109:10.44,110:10.49,111:10.54,112:10.58,113:10.63,114:10.68,115:10.72,116:10.77,117:10.82,118:10.86,119:10.91,120:10.95,121:11.0,122:11.05,123:11.09,124:11.14,125:11.18,126:11.22,127:11.27,128:11.31,129:11.36,130:11.4,131:11.45,132:11.49,133:11.53,134:11.58,135:11.62,136:11.66,137:11.7,138:11.75,139:11.79,140:11.83,141:11.87,142:11.92,143:11.96,144:12.0,145:12.04,146:12.08,147:12.12,148:12.17,149:12.21,150:12.25,151:12.29,152:12.33,153:12.37,154:12.41,155:12.45,156:12.49,157:12.53,158:12.57,159:12.61,160:12.65,161:12.69,162:12.73,163:12.77,164:12.81,165:12.85,166:12.88,167:12.92,168:12.96,169:13.0,170:13.04,171:13.08,172:13.11,173:13.15,174:13.19,175:13.23,176:13.27,177:13.3,178:13.34,179:13.38,180:13.42,181:13.45,182:13.49,183:13.53,184:13.56,185:13.6,186:13.64,187:13.67,188:13.71,189:13.75,190:13.78,191:13.82,192:13.86,193:13.89,194:13.93,195:13.96,196:14.0,197:14.04,198:14.07,199:14.11,200:14.14,201:14.18,202:14.21,203:14.25,204:14.28,205:14.32,206:14.35,207:14.39,208:14.42,209:14.46,210:14.49,211:14.53,212:14.56,213:14.59,214:14.63,215:14.66,216:14.7,217:14.73,218:14.76,219:14.8,220:14.83,221:14.87,222:14.9,223:14.93,224:14.97,225:15.0,226:15.03,227:15.07,228:15.1,229:15.13,230:15.17,231:15.2,232:15.23,233:15.26,234:15.3,235:15.33,236:15.36,237:15.39,238:15.43,239:15.46,240:15.49,241:15.52,242:15.56,243:15.59,244:15.62,245:15.65,246:15.68,247:15.72,248:15.75,249:15.78,250:15.81,251:15.84,252:15.87,253:15.91,254:15.94,255:15.97,256:16.0,257:16.03,258:16.06,259:16.09,260:16.12,261:16.16,262:16.19,263:16.22,264:16.25,265:16.28,266:16.31,267:16.34,268:16.37,269:16.4,270:16.43,271:16.46,272:16.49,273:16.52,274:16.55,275:16.58,276:16.61,277:16.64,278:16.67,279:16.7,280:16.73,281:16.76,282:16.79,283:16.82,284:16.85,285:16.88,286:16.91,287:16.94,288:16.97,289:17.0,290:17.03,291:17.06,292:17.09,293:17.12,294:17.15,295:17.18,296:17.2,297:17.23,298:17.26,299:17.29,}

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
def acos(x):
    # print(x)
    min_dist = 1000
    winner = None
    for key,val in COS_X.items():
        d = modulus(x-val)
        if d < min_dist:
            min_dist = d
            winner = key
    return winner
    
# rotate a vertex by an angle upon a point
# as we use the point to find the radius,
# if many vertices use the same radius,
# that can be passed in instead to save computation
def rotate(v,a,p,r=None):
    if r: rad = r
    else: rad = SQRT[round( (v[0]-p[0])**2 + (v[1]-p[1])**2 )]
    a = round(a)
    while a%15:
        a+=1
    # using trigonometry to find the new position (SOHCAHTOA)
    inv = (v[0] - p[0])/rad
    current_angle = acos(inv)
    if v[1] < p[1]:
        current_angle += 90 * ((2 * (inv > 0)) -1)
    nang = (a+current_angle) % 360
    
    # print(nang)
    new_x = rad * COS_X[nang] + p[0]
    new_y = rad * SIN_X[nang] + p[1]
    return (new_x,new_y)
# draw a rectangle with left-top corner at x,y with
# width w and height h, rotated by angle a
# note: rotated rects (squares) are not filled
def draw_rect(x,y,w,h,a=0):
    if not a:
        display.rectangle(y,x,h,w)
        return
    overtices = [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
    center = (x+w/2, y + w/2)
    # MicroPython does not include list comprehension
    # vertices = [rotate(v,a,center) for v in vertices]
    vertices = []
    for v in overtices:
        vertices.append(rotate(v,a,center))
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
class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.a = 0
    def move(self,dx,dy):
        self.x += dx
        self.y += dy
    def rotate(self,ang):
        self.a += ang
    def draw(self):
        draw_rect(self.x,self.y,5,5,self.a)

while True:
    display.set_pen(BLACK)
    display.clear()

    display.set_pen(WHITE)
    #draw_vline(0, 0, HEIGHT, 5);
    #draw_vline(50, 15, HEIGHT-15, 5);
    
    # draw_rect(100,50,5,5)
    draw_rect(100,50,5,5,45)

    display.update()
    time.sleep(0.01)
