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
    def __init__(self, color, dx, dy):
        self.color = color
        self.dx = dx
        self.dy = dy

class Sphere(Bullet):
    def __init__(self, color, x, y, dx, dy, r):
        super().__init__(color, dx, dy)
        self.x = x
        self.y = y
        self.r = r

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Polygon(Bullet):
    def __init__(self, color, vertice, dx, dy):
        super().__init__(color, dx, dy)
        self.vertice = vertice

def appStarted(app):
    app.width = 2560
    app.height = 1600
    app.bg = app.loadImage("bg1.png")
    app.bf = app.loadImage("bf1.jpg")
    app.spellcard = "Starfury!"
    app.bullets = []
    app.working = False
    app.time = 0
    app.doubleMode = False
    app.time = 0
    app.score = 0
    app.life = 5
    app.bomb = 3
    app.init = True
    app.player = Player(0,0,0,0,0,0)
    app.time = 0
    app.gg = False


def keyPressed(app, event):
    if(not app.gg):
        if (event.key == 'Up'):
            app.player.y -= 5
        elif (event.key == 'Down'): 
            app.player.y += 5
        elif (event.key == 'Left'):
            app.player.x -= 5
        elif (event.key == 'Right'):
            app.player.x += 5
        elif(event.key =="r"):
            appStarted(app)

def circleInBounds(app):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    newList = []
    for sets in app.bullets:
        newSet = []
        for bullet in sets:
            if ((bullet.x>40 and bullet.y>40 and bullet.x<40+bf_w
            and bullet.y<40+bf_h)):
                newSet.append(bullet)
        newList.append(newSet)
    app.bullets = newList

def polygonInBounds(app):
    pass

def circleCircleCollision(app):
    p = app.player
    for sets in app.bullets:
        for b in sets:
            if(((b.x-p.x)**2+(b.y-p.y)**2)**0.5<b.r+p.r):
                app.gg = True

def polygonCircleCollision(app):
    pass
    # p = app.player
    # nextVertice = 0
    # vertice = 0
    # for sets in app.bullets:
    #     for b in sets:
    #         if(isinstance(b, Polygon)):
    #             vertice = len(b.vertice)
    #         for current in range(vertice):
    #             next = current+1;
    #             if (next == vertice):
    #                 next = 0
    #             vc = b.
    #             PVector vc = vertices[current];
    #             PVector vn = vertices[next];

    #             boolean collision = lineCircle(vc.x,vc.y, vn.x,vn.y, cx,cy,r);
    #             if (collision) return true;

def polygonPolygonCollision(app):
    pass
    # pseudocode for tp1,
    # real code for tp2

def timerFired(app):
    if(not app.gg):
        app.time+=1
        if(app.init):
            app.player = Player(app.width/2.6, app.height-60,7,0,3,5)
            app.init = False
        # circleInBounds(app)
        # circleCircleCollision(app)
        if(app.time==10):
            not_the_bees(app)
        # elif(app.time==20):
        #     starfury_double(app)
        for sets in app.bullets:
            for b in sets:
                if(isinstance(b,Sphere)):
                    b.x+=b.dx
                    b.y+=b.dy
                elif(isinstance(b,Polygon)):
                    for point in b.vertice:
                        point.x+=b.dx
                        point.y+=b.dy


def starfury_help(app, sets, speed, color):
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

def starfury(app):
    circle1 = []
    app.bullets.append(circle1)
    starfury_help(app, circle1, 5, "pink")
    circle2 = []
    app.bullets.append(circle2)
    starfury_help(app, circle2, 7.5, "cyan")
    circle3 = []
    app.bullets.append(circle3)
    starfury_help(app, circle3, 10, "yellow")

def starfury_double(app):
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

def not_the_bees_help(app, sets, speed, color):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    cx, cy, r= (bf_w)/2, (bf_h)/2, min(bf_w, bf_h)/3
    r *= 0.1
    no = 10
    for i in range(no):
        gon = Polygon(color,[],0,0)
        angle = math.pi/2 - (2*math.pi)*(i/no)
        ox = cx + r * math.cos(angle)
        oy = cy + r * math.sin(angle)
        dx = speed*math.cos(angle)
        dy = speed*math.sin(angle)
        for i in range(6):
            cx, cy, r = ox, oy, 30
            angle = math.pi/2 - (2*math.pi)*(i/6)
            xx = cx + r * math.cos(angle)
            yy = cy + r * math.sin(angle)
            point = Point(xx,yy)
            gon.vertice.append(point)
        gon.dx = dx
        gon.dy = dy
        sets.append(gon)
    
def not_the_bees(app):
    hex1 = []
    app.bullets.append(hex1)
    not_the_bees_help(app, hex1, 7, "orange")
    hex2 = []
    app.bullets.append(hex2)
    not_the_bees_help(app, hex1, 10, "gold")

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
    canvas.create_text(ib_x0+30,ib_y0+110, text=f"Current Spellcard: {app.spellcard}",
                            font = "Ariel 20 bold", anchor = "w") 
    if(app.gg):
        canvas.create_text(ib_x0+30,ib_y0+130, text=f"GAME OVER!!! :P",
                            font = "Ariel 20 bold", anchor = "w") 

def redraw_UI(app, canvas):
    redraw_background(app, canvas)
    redraw_battlefield(app, canvas)
    redraw_infoboard(app, canvas)
def redraw_player(app, canvas):
    p = app.player
    canvas.create_oval(p.x-p.r,p.y-p.r,p.x+p.r,p.y+p.r,fill="Purple",
                        outline = "white", width = 5)
def redraw_bullets(app,canvas):
    for sets in app.bullets:
        for i in range(len(sets)):
            b = sets[i]
            if(isinstance(b, Sphere)):
                canvas.create_oval(b.x-b.r,b.y-b.r,b.x+b.r,b.y+b.r,
                                    fill = b.color)
            elif(isinstance(b, Polygon)):
                if(len(b.vertice)==6):
                    v = b.vertice
                canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,v[4].x,v[4].y,v[5].x,v[5].y,
                                    fill = b.color)
def redrawAll(app, canvas):
    redraw_UI(app,canvas)
    redraw_bullets(app,canvas)
    redraw_player(app,canvas)


runApp(width=2560, height=1600)