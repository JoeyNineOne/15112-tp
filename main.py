from cmu_112_graphics import *
import math, time
class Player():
    def __init__(self, x, y, r, shape, cx, cy):
        self.x = x
        self.y = y
        self.r = r
        self.shape = shape
        self.cx = cx
        self.cy = cy

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
    # Image from:
    # https://www.pexels.com/photo/scenic-view-of-mountains-during-dawn-1261728/
    app.bg = app.loadImage("bg1.png")
    # Image from:
    # https://cdn.mos.cms.futurecdn.net/KZjRDpe6uy9gB2jt7CgKWN.jpg
    # I have cropped this image so it is a little different from its 
    # original dimensions
    app.bf = app.loadImage("bf1.jpg")
    app.spellcard = "Starfury!"
    app.bullets = []
    app.working = False
    app.time = 0
    app.doubleMode = False
    app.score = 0
    app.life = 5
    app.bomb = 3
    app.init = True
    app.player = Player(0,0,0,Sphere("white",0,0,0,0,0),0,0)
    app.gg = False
    app.hasBomb = False

def keyPressed(app, event):
    if(not app.gg):
        print(app.player.cx,app.player.cy)
        if (event.key == 'Up'):
            for i in range(len(app.player.shape.vertice)):
                app.player.shape.vertice[i].y -= 15
            app.player.cy -= 15
        elif (event.key == 'Down'): 
            for i in range(len(app.player.shape.vertice)):
                app.player.shape.vertice[i].y += 15
            app.player.cy += 15
        elif (event.key == 'Left'):
            for i in range(len(app.player.shape.vertice)):
                app.player.shape.vertice[i].x -= 15
            app.player.cx -= 15
        elif (event.key == 'Right'):
            for i in range(len(app.player.shape.vertice)):
                app.player.shape.vertice[i].x += 15
            app.player.cx += 15
        elif(event.key =="r"):
            appStarted(app)
        elif(event.key=="f" and app.bomb>0):
            app.hasBomb = True
            app.bomb-=1

def circleInBounds(app):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    newList = []
    for sets in app.bullets:
        newSet = []
        for bullet in sets:
            ((bullet.x-app.player.x)**2+(bullet.y-app.player.y)**2)**0.5
            if (((bullet.x>40 and bullet.y>40 and bullet.x<40+bf_w
            and bullet.y<40+bf_h))):
                if(not app.hasBomb):
                    newSet.append(bullet)
                elif(isinstance(app.player.shape, Sphere) and app.hasBomb and ((bullet.x-app.player.x)**2+(bullet.y-app.player.y)**2)**0.5>100):
                    newSet.append(bullet)
                elif(isinstance(app.player.shape, Polygon) and app.hasBomb and ((bullet.x-app.player.cx)**2+(bullet.y-app.player.cy)**2)**0.5>100):
                    newSet.append(bullet)
        newList.append(newSet)
    app.bullets = newList
    app.hasBomb = False

def polygonInBounds(app):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    newList = []
    for sets in app.bullets:
        newSet = []
        for bullet in sets:
            flag = False
            for vertice in bullet.vertice:
                if ((vertice.x<40 or vertice.y<40 or vertice.x>40+bf_w
                or vertice.y>40+bf_h)):
                    flag = True
                elif(app.hasBomb):
                    if(isinstance(app.player.shape, Sphere) and ((vertice.x-app.player.x)**2+(vertice.y-app.player.y)**2)**0.5<app.player.r+30):
                        flag = True
                    elif(isinstance(app.player.shape, Polygon) and ((vertice.x-app.player.cx)**2+(vertice.y-app.player.cy)**2)**0.5<app.player.r+30):
                        flag = True
            if(not flag):
                newSet.append(bullet)
        newList.append(newSet)
    app.bullets = newList
    app.hasBomb = False

def bestRoute(app):
    pass
    # This will be my feature that tells the user where to go so
    # they have a higher chance of surviving (a.k.a, not being
    # hit by the bullets).

    # Winning condition of the game: successfully survive all rounds of
    # bullets.

    # Pseudocode: modified BFS is our best choice given the winning condition above.
    # We turn the map into grids, go from one cell to a neighboring one,
    # check if one second later as well as two seconds later, if there will 
    # be a bullet in that cell. If there won't be a bullet for the next two 
    # consecutive seconds, that place is declared safe.

    # more distance = less weight on the graph.

    # location of boss factored in


# Below are my collision functions.
# thanks very much to Jeffery Thompson for sharing how he did it;
# this helped me tremendously.
# http://www.jeffreythompson.org/collision-detection/

def lineLineCollision_helper(x1, y1, x2, y2, x3, y3, x4, y4):
    uA = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/((y4-y3)*(x2-x1)-(x4-x3)*(y2-y1))
    uB = ((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/((y4-y3)*(x2-x1)-(x4-x3)*(y2-y1))
    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
        return True
    return False

def linePolygonCollision_helper(v, x1, y1, x2, y2):
    nextv = 0
    vertice = len(v)
    for current in range(vertice):
        nextv = current+1
        if (nextv == vertice):
            nextv = 0
        x3 = v[current].x
        y3 = v[current].y
        x4 = v[nextv].x
        y4 = v[nextv].y
        if(lineLineCollision_helper(x1, y1, x2, y2, x3, y3, x4, y4)):
            return True
    return False

def lineCircleCollision_helper(x1, y1, x2, y2, cx, cy, r):
    # Before we do anything else, the easiest thing we can do is to
    # test if any of the two ends of the line are already inside 
    # the circle.
    if (((x1-cx)**2+(y1-cy)**2)**0.5 <= r or ((x2-cx)**2+(y2-cy)**2)**0.5 <= r):
        return True
    # If the above is not true, our second step is to get the closest 
    # point on the line to our circle. First we get the length of the 
    # line using pythag, and then use the dot product to find the closest point.
    # https://en.wikipedia.org/wiki/Dot_product
    length = (((x1-x2)**2)+((y1-y2)**2))**0.5
    dotProduct=(((cx-x1)*(x2-x1))+((cy-y1)*(y2-y1)))/(length**2)
    closestX = x1 + (dotProduct * (x2-x1))
    closestY = y1 + (dotProduct * (y2-y1))
    d1 = ((closestX-x1)**2+(closestY-y1)**2)**0.5
    d2 = ((closestX-x2)**2+(closestY-y2)**2)**0.5
    d1+d2>=length-0.1 and d1+d2<=length+0.1
    # The dot product method actually assumes that our segment is a 
    # line (that extends to infinity) and not a segment. So we 
    # need to make sure that the point we found is actually on the segment itself. 
    # If it isn't, we just return false because, well, the closest point is
    # literally not on our segment :)
    onLine = d1+d2>=length-0.1 and d1+d2<=length+0.1
    if (not onLine):
        return False
    # At last, with pythag again, we calculate the distance from the 
    # circle to the closest point on the line that we just calculated 
    # with the dot product. If this distance is smaller than the radius,
    # the line and the circle do meet.
    distance = ((closestX-cx)**2+(closestY-cy)**2)**0.5
    if (distance <= r):
        return True
    else:
        return False
    
def circleCircleCollision(app):
    p = app.player
    for sets in app.bullets:
        for b in sets:
            if(((b.x-p.x)**2+(b.y-p.y)**2)**0.5<b.r+p.r):
                app.hasBomb = True
                app.life-=1

def polygonCircleCollision(app):
    #  "To test if a circle has collided with a polygon, we can simplify
    #  the problem to a series of line and circle collisions, one for each
    #  side of the polygon." ----Jeffery Thompson
    nextv = 0
    vertice = 0
    for sets in app.bullets:
        for b in sets:
            vertice = len(b.vertice)
            for current in range(vertice):
                nextv = current+1
                # This goes through each vertice and the next one, also
                # note how if this is the last vertice, the next vertice
                # is set to the first vertice :)
                if (nextv == vertice):
                    nextv = 0
                vc = b.vertice[current]
                vn = b.vertice[nextv]
                # This checks for collision between the circle
                # and the line that can be created by connecting the 
                # two vertices that we've previously selected
                collision = lineCircleCollision_helper(vc.x,vc.y,vn.x,vn.y,app.player.x,app.player.y,app.player.r)
                if(collision):
                    app.hasBomb = True
                    app.life-=1

def polygonPolygonCollision(app):
    # ill annotate it this afternoon, its 8 am and i need to sleep hehe
    nextv = 0
    vertice = 0
    for sets in app.bullets:
        for b in sets:
            vertice = len(b.vertice)
            for current in range(vertice):
                nextv = current+1;
                if (nextv == vertice):
                    nextv = 0
                vc = b.vertice[current]
                vn = b.vertice[nextv]
                if(linePolygonCollision_helper(app.player.shape.vertice,vc.x,vc.y,vn.x,vn.y)):
                    app.hasBomb = True
                    app.life-=1

def timerFired(app):
    if(app.life<=0):
        app.gg = True
    if(not app.gg):
        app.time+=1
        if(app.init):
            gon = Polygon("purple",[],0,0)
            bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
            bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
            cx, cy, r= (bf_w)/2, (bf_h)-40, 10
            for i in range(4):
                angle = math.pi/2 - (2*math.pi)*(i/4)
                xx = cx + r * math.cos(angle)
                yy = cy + r * math.sin(angle)
                point = Point(xx,yy)
                gon.vertice.append(point)
            app.player = Player(app.width/2.6,app.height-60,10,gon, cx, cy)
            app.init = False
        # circleInBounds(app)
        # circleCircleCollision(app)
        # polygonCircleCollision(app)
        polygonPolygonCollision(app)
        polygonInBounds(app)
        if(app.time==10):
            # starfury(app)
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

def not_the_bees_help(app, sets, speed, color, no):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    cx, cy, r= (bf_w)/2, (bf_h)/2, min(bf_w, bf_h)/3
    r *= 0.1
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
    not_the_bees_help(app, hex1, 10, "orange", 30)
    hex2 = []
    app.bullets.append(hex2)
    not_the_bees_help(app, hex2, 15, "gold", 25)
    hex3 = []
    app.bullets.append(hex3)
    not_the_bees_help(app, hex3, 20, "khaki", 20)
    hex4 = []
    app.bullets.append(hex4)
    not_the_bees_help(app, hex4, 25, "light yellow", 15)

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
    if(app.bomb==1):
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
    if(isinstance(p.shape, Polygon)):
        if(len(p.shape.vertice)==4):
            v = p.shape.vertice
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,
                                    fill = p.shape.color, outline = "white", width = 5)
    else:
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