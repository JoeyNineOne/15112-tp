# This demos loadImage and scaleImage from a local file

from cmu_112_graphics import *
import math, time
class Player():
    def __init__(self, x, y, r, score, bomb, life):
        self.x = x
        self.y = y
        self.r = r
        self.score = score
        self.bomb = bomb
        self.life = life
class Bullet():
    def __init__(self, color, x, y, dx, dy):
        self.color = color
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

class Sphere(Bullet):
    def __init__(self, color, x, y, dx, dy, r):
        super().__init__(color, x, y, dx, dy)
        self.r = r

def appStarted(app):
    app.width = 2560
    app.height = 1600
    app.bg = app.loadImage("bg1.png")
    app.bf = app.loadImage("bf1.jpg")
    app.spellcards = True
    app.bullets = []
    app.timerDelay = 1
    app.working = False
    app.time = 0
    app.doubleMode = False
    app.time = 0
    app.score = 0
    app.life = 5
    app.bomb = 3
    app.init = True
    app.player = Player(0,0,0,0,0,0)
    
def checkInBounds(app):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    for sets in app.bullets:
        i = 0
        while (i < len(sets)):
            if ((sets[i].x<40 or sets[i].y<40 or sets[i].x>40+bf_w
            or sets[i].y>40+bf_h)):
                sets.pop(i)
            else:
                i += 1

def timerFired(app):
    if(app.init):
        app.player = Player(app.width/2.6, app.height-60,5,0,3,5)
        app.init = False
    app.time+=1
    checkInBounds(app)
    if(app.time==1):
        spellcard(app)
    if(app.time==20):
        spellcard_double(app)
    for sets in app.bullets:
        for b in sets:
            b.x+=b.dx
            b.y+=b.dy

def spellcard_help(app, sets, speed, color):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    cx, cy, r= (bf_w)/2, (bf_h)/2, min(bf_w, bf_h)/3
    r *= 0.1
    no = 50
    for i in range(no):
        angle = math.pi/2 - (2*math.pi)*(i/no)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        dx = speed*math.cos(angle)
        dy = speed*math.sin(angle)
        sets.append(Sphere(color,x,y,dx,dy,7.5))
def spellcard(app):
    circle1 = []
    app.bullets.append(circle1)
    spellcard_help(app, circle1, 5, "pink")
    circle2 = []
    app.bullets.append(circle2)
    spellcard_help(app, circle2, 7.5, "cyan")
    circle3 = []
    app.bullets.append(circle3)
    spellcard_help(app, circle3, 10, "yellow")

def spellcard_double(app):
    for i in range(2):
        for i in range(len(app.bullets)):
            sets = app.bullets[i]
            app.bullets.append(copy.deepcopy(sets))
    for i in range(len(app.bullets)):
        sets = app.bullets[i]
        if(i<=len(app.bullets)//4-1):
            for b in sets:
                b.dx -=10
                b.dy -=10
        elif(i<=len(app.bullets)//4*2-1):
            for b in sets:
                b.dx +=10
                b.dy +=10
        elif(i<=len(app.bullets)//4*3-1):
            for b in sets:
                b.dx -=10
                b.dy +=10
        elif(i<=len(app.bullets)-1):
            for b in sets:
                b.dx +=10
                b.dy -=10

def redraw_background(app, canvas):
    canvas.create_image(200, 200, image=ImageTk.PhotoImage(app.bg))

def redraw_battlefield(app, canvas):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40

    canvas.create_image((bf_x1-bf_x0)/2+40,(bf_y1-bf_y0)/2+40, image=ImageTk.PhotoImage(app.bf))

def redraw_infoboard(app,canvas):
    ib_x0, ib_y0, ib_x1, ib_y1 = app.width/1.3, 40, app.width-40, app.height/3+40
    canvas.create_rectangle(ib_x0,ib_y0,ib_x1,ib_y1,
                            fill = "white") 
    canvas.create_text(ib_x0+30,ib_y0+20, text=f"Score = {app.score}",
                            font = "Ariel 20 bold", anchor = "w") 
    if(app.bomb<=1):
        canvas.create_text(ib_x0+30,ib_y0+50, text=f"You have {app.bomb} bomb left!",
                            font = "Ariel 20 bold", anchor = "w") 
    else:
        canvas.create_text(ib_x0+30,ib_y0+50, text=f"You have {app.bomb} bombs left!",
                            font = "Ariel 20 bold", anchor = "w") 
    canvas.create_text(ib_x0+30,ib_y0+80, text=f"Life = {app.life}",
                            font = "Ariel 20 bold", anchor = "w") 
def redraw_UI(app, canvas):
    redraw_background(app, canvas)
    redraw_battlefield(app, canvas)
    redraw_infoboard(app, canvas)
def redraw_player(app, canvas):
    p = app.player
    canvas.create_oval(p.x-p.r,p.y-p.r,p.x+p.r,p.y+p.r,fill="Purple")
def redraw_bullets(app,canvas):
    for sets in app.bullets:
        for i in range(len(sets)):
            b = sets[i]
            canvas.create_oval(b.x-b.r,b.y-b.r,b.x+b.r,b.y+b.r,
                                    fill = b.color)
def redrawAll(app, canvas):
    redraw_UI(app,canvas)
    redraw_bullets(app,canvas)
    redraw_player(app,canvas)


runApp(width=2560, height=1600)