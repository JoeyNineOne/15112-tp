# Andrew ID: jiayid
# Name: Jiayi (Joey) Dong
# Term Project for 15-112 N21

from cmu_112_graphics import *
import math, time, random
class Player():
    def __init__(self,r, shape, cx, cy):
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
    # I drew this background myself hehe, no citing needed
    app.bg = app.loadImage("bg1.png")
    # Image from:
    # https://cdn.mos.cms.futurecdn.net/KZjRDpe6uy9gB2jt7CgKWN.jpg
    # I have cropped this image so it is a little different from its 
    # original dimensions
    app.bf = app.loadImage("bf1.jpg")
    # I drew her myself hehe, no citing needed
    app.k = app.loadImage("kaleido.jpeg")
    app.kaleido = app.scaleImage(app.k, 7/15)
    app.kaleido2 = app.scaleImage(app.k, 1/3)
    variablesInit(app)

def variablesInit(app):
    app.bullets = []
    app.time = 0
    app.life = 30
    app.bomb = 5
    app.init = True
    app.player = Player(0,Sphere("white",0,0,0,0,0),0,0)
    app.gg = False
    app.help = False
    app.grid = []
    app.row = 20
    app.col = 20
    app.safe = -999,-999
    app.startscreen = True
    app.directions = False
    app.countdown = 0
    app.endtime = 0
    app.currwave = 0
    app.rest = False
    app.firstHelp = True
    app.win = False

def keyPressed(app, event):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    avoid = 10
    if(not app.gg):
        if (event.key == 'Up'):
            if(isinstance(app.player.shape,Polygon)):
                for i in range(len(app.player.shape.vertice)):
                    newPos = app.player.shape.vertice[i].y-15
                    if(not (newPos>40+avoid and newPos<40+bf_h-avoid)):
                        return
                for i in range(len(app.player.shape.vertice)):
                    app.player.shape.vertice[i].y -= 15
            else:
                newPos = app.player.cy-15
                if((newPos>40+avoid and newPos<40+bf_h-avoid)):
                    app.player.cy -= 15
        elif (event.key == 'Down'): 
            if(isinstance(app.player.shape,Polygon)):
                for i in range(len(app.player.shape.vertice)):
                    newPos = app.player.shape.vertice[i].y+15
                    if(not (newPos>40+avoid and newPos<40+bf_h-avoid)):
                        return
                for i in range(len(app.player.shape.vertice)):
                    app.player.shape.vertice[i].y += 15
            else:
                newPos = app.player.cy+15
                if((newPos>40+avoid and newPos<40+bf_h-avoid)):
                    app.player.cy += 15
        elif (event.key == 'Left'):
            if(isinstance(app.player.shape,Polygon)):
                for i in range(len(app.player.shape.vertice)):
                    newPos = app.player.shape.vertice[i].x-15
                    if(not (newPos>40+avoid and newPos<40+bf_w-avoid)):
                        return
                for i in range(len(app.player.shape.vertice)):
                    app.player.shape.vertice[i].x -= 15
            else:
                newPos = app.player.cx-15
                if((newPos>40+avoid and newPos<40+bf_w-avoid)):
                    app.player.cx -= 15
        elif (event.key == 'Right'):
            if(isinstance(app.player.shape,Polygon)):
                for i in range(len(app.player.shape.vertice)):
                    newPos = app.player.shape.vertice[i].x+15
                    if(not (newPos>40+avoid and newPos<40+bf_w-avoid)):
                        return
                for i in range(len(app.player.shape.vertice)):
                    app.player.shape.vertice[i].x += 15
            else:
                newPos = app.player.cx+15
                if((newPos>40+avoid and newPos<40+bf_w-avoid)):
                    app.player.cx += 15
        elif(event.key =="r"):
            variablesInit(app)
        elif(event.key=="f" and app.bomb>0):
            app.bomb-=1
            bomb(app)
        elif(event.key=="d"):
            app.help = not app.help
        elif(event.key=="Space" and app.startscreen):
            app.directions = True
            app.startscreen = False
        elif(event.key=="Space" and app.directions):
            app.directions = False
    else:
        if(event.key=="Space"):
            variablesInit(app)

def bomb(app):
    newList = []
    for sets in app.bullets:
        newSet = []
        for b in sets:
            if(isinstance(b,Sphere) and isinstance(app.player.shape,Sphere)):
                if(((b.x-app.player.cx)**2+(b.y-app.player.cy)**2)**0.5>
                100):
                    newSet.append(b)
            elif(isinstance(b,Polygon) and isinstance(app.player.shape,Sphere)):
                if(((b.vertice[0].x-app.player.cx)**2+(b.vertice[0].y-app.player.cy)**2)**0.5>
                100):
                    newSet.append(b)
            elif(isinstance(b,Polygon) and isinstance(app.player.shape,Polygon)):
                if(((b.vertice[0].x-app.player.shape.vertice[0].x)**2+(b.vertice[0].y-app.player.shape.vertice[0].y)**2)**0.5>
                100):
                    newSet.append(b)
            elif(isinstance(b,Sphere) and isinstance(app.player.shape,Polygon)):
                if(((b.x-app.player.shape.vertice[0].x)**2+(b.y-app.player.shape.vertice[0].y)**2)**0.5>
                100):
                    newSet.append(b)
        newList.append(newSet)
    app.bullets = newList


def circleInBounds(app,bullet):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    if (((bullet.x>40 and bullet.y>40 and bullet.x<40+bf_w
    and bullet.y<40+bf_h))):
        return True
    return False

def polygonInBounds(app,bullet):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    for vertice in bullet.vertice:
        if ((vertice.x<40 or vertice.y<40 or vertice.x>40+bf_w
        or vertice.y>40+bf_h)):
            return False
    return True

def getCell(app, x, y):
    # modified from the function here:
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    cellWidth = bf_w / app.col
    cellHeight = bf_h / app.row
    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - bf_y0) / cellHeight)
    col = int((x - bf_x0) / cellWidth)
    return (row, col)

def getCellBounds(app, row, col):
    # modified from the function here:
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    cellWidth = bf_w / app.col
    cellHeight = bf_h / app.row
    x0 = bf_x0 + col * cellWidth
    x1 = bf_x0 + (col+1) * cellWidth
    y0 = bf_y0 + row * cellHeight
    y1 = bf_y0 + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def bestRoute(app):
    simulation = copy.deepcopy(app.bullets)
    grid = []
    for i in range(app.row):
        grid += [[0]*app.col]
    # grid add pattern from 0th second
    addToGrid(app, simulation, grid)
    # 0th second -> 1st second
    increaseTime(app, simulation)
    # grid add pattern from 1th second
    addToGrid(app, simulation, grid)
    # 1st bfs
    if(isinstance(app.player.shape,Sphere)):
        startx, starty = getCell(app,app.player.cx,app.player.cy)
    elif(isinstance(app.player.shape,Polygon)):
        startx, starty = getCell(app,app.player.shape.vertice[0].x,app.player.shape.vertice[0].y)
    bfs(app, grid, startx, starty)

def increaseTime(app, simulation):
    for sets in simulation:
        for b in sets:
            if(isinstance(b,Sphere)):
                b.x+=3*b.dx
                b.y+=3*b.dy
            elif(isinstance(b,Polygon)):
                for point in b.vertice:
                    point.x+=3*b.dx
                    point.y+=3*b.dy

def bfs(app, grid, startx, starty):
    q = []
    vis = [[ False for i in range(app.col)] for i in range(app.row)]
    dRow = [ -1, 0, 1, 0]
    dCol = [ 0, 1, 0, -1]
    # Mark the starting cell as visited
    # and push it into the queue
    q.append((startx,starty))
    vis[startx][starty] = True
    # Iterate while the queue
    # is not empty
    while (len(q) > 0):
        x,y = q.pop(0)
        # Go to the adjacent cells
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if (isValid(app, vis, adjx, adjy, grid)):
                app.safe = (adjx,adjy)
                return

def addToGrid(app, simulation, grid):
    for i in range(app.row):
        for j in range(app.col):
            x0, y0, x1, y1 = getCellBounds(app,i,j)
            for sets in simulation:
                for b in sets:
                    if(isinstance(b,Sphere)):
                        if(x0<b.x and b.x<x1 and y0<b.y and b.y<y1):
                            grid[i][j] += 1
                    else:
                        for v in b.vertice:
                            if(x0<v.x and v.x<x1 and y0<v.y and v.y<y1):
                                grid[i][j] += 1
                                
def isValid(app, vis, row, col, grid):
    # If cell lies out of bounds
    if (row < 0 or col < 0 or row >= app.row or col >= app.col):
        return False
    # If cell is already visited
    if(vis[row][col]):
        return False
    if(grid[row][col]!=0):
        return False
    return True

# Below are my collision functions.
# thanks very much to Jeffery Thompson for sharing how he did it;
# this helped me tremendously.
# http://www.jeffreythompson.org/collision-detection/

def lineLineCollision_helper(x1, y1, x2, y2, x3, y3, x4, y4):
    if(((y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)==0)):
        return False
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
    if(length**2==0):
        return False
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
            if(isinstance(app.player.shape,Sphere) and isinstance(b,Sphere)):
                if(((b.x-p.cx)**2+(b.y-p.cy)**2)**0.5<b.r+p.r):
                    bomb(app)
                    app.life-=1

def polygonCircleCollision(app):
    #  "To test if a circle has collided with a polygon, we can simplify
    #  the problem to a series of line and circle collisions, one for each
    #  side of the polygon." ----Jeffery Thompson
    nextv = 0
    vertice = 0
    for sets in app.bullets:
        for b in sets:
            if(isinstance(app.player.shape,Sphere) and isinstance(b,Polygon)):
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
                    collision = lineCircleCollision_helper(vc.x,vc.y,vn.x,vn.y,app.player.cx,app.player.cy,app.player.r)
                    if(collision):
                        bomb(app)
                        app.life-=1
            elif((isinstance(app.player.shape,Polygon) and isinstance(b,Sphere))):
                vertice = len(app.player.shape.vertice)
                for current in range(vertice):
                    nextv = current+1
                    # This goes through each vertice and the next one, also
                    # note how if this is the last vertice, the next vertice
                    # is set to the first vertice :)
                    if (nextv == vertice):
                        nextv = 0
                    vc = app.player.shape.vertice[current]
                    vn = app.player.shape.vertice[nextv]
                    # This checks for collision between the circle
                    # and the line that can be created by connecting the 
                    # two vertices that we've previously selected
                    collision = lineCircleCollision_helper(vc.x,vc.y,vn.x,vn.y,b.x,b.y,b.r)
                    if(collision):
                        bomb(app)
                        app.life-=1
                        
def polygonPolygonCollision(app):
    nextv = 0
    vertice = 0
    for sets in app.bullets:
        for b in sets:
            if(isinstance(b,Polygon) and isinstance(app.player.shape,Polygon)):
                vertice = len(b.vertice)
                for current in range(vertice):
                    nextv = current+1
                    if (nextv == vertice):
                        nextv = 0
                    vc = b.vertice[current]
                    vn = b.vertice[nextv]
                    if(linePolygonCollision_helper(app.player.shape.vertice,vc.x,vc.y,vn.x,vn.y)):
                        bomb(app)
                        app.life-=1
                        

def collisionDetection(app):
    if(isinstance(app.player.shape, Sphere)):
        circleCircleCollision(app)
    else:
        polygonPolygonCollision(app)
    polygonCircleCollision(app)

def inBoundsCheck(app):
    newList = []
    for sets in app.bullets:
        newSet = []
        for b in sets:
            if(isinstance(b,Sphere)):
                if (circleInBounds(app, b)):
                    newSet.append(b)
            else:
                if(polygonInBounds(app,b)):
                    newSet.append(b)
        newList.append(newSet)
    app.bullets = newList

def nextStepHelp(app):
    if(isinstance(app.player.shape,Sphere)):
        row, col = getCell(app,app.player.cx,app.player.cy)
    elif(isinstance(app.player.shape,Polygon)):
        row, col = getCell(app,app.player.shape.vertice[0].x,app.player.shape.vertice[0].y)
    safex, safey = app.safe
    if(row == safex and col == safey):
        bestRoute(app)
def timerFired(app):
    if(app.life<=0):
        app.gg = True
    if(not app.gg):
        if(not app.startscreen and not app.directions):
            if(app.init):
                bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
                bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
                cx, cy, r= (bf_w)/2, (bf_h)-40, 10
                shapeChoice = app.getUserInput('What shape should Kaleido take on? 0 for circle, 3 for triangle, 4 for square, etc. Inputs up to 10 allowed')
                while(not (shapeChoice=="0" or shapeChoice=="3" or shapeChoice=="4" or shapeChoice=="5" or shapeChoice=="6" or shapeChoice=="7" or shapeChoice=="8" or shapeChoice=="9" or shapeChoice=="10")):
                    shapeChoice = app.getUserInput("That's not a valid number for a shape, sorry. Can you type again? (0 and 3~10 accepted)")
                if(shapeChoice == "0"):
                    gon = Sphere("purple",app.width/2.6,app.height-60,0,0,10)
                    app.player = Player(10,gon,cx,cy)
                    app.init = False
                elif(shapeChoice.isnumeric() and int(shapeChoice)>=3 and int(shapeChoice)<=10):
                    shapeChoice = int(shapeChoice)
                    gon = Polygon("purple",[],0,0)
                    # the code below wastaken from here and then modified:
                    # https://www.cs.cmu.edu/~112/notes/notes-graphics.html#circlesWithTrig
                    for i in range(shapeChoice):
                        angle = math.pi/2 - (2*math.pi)*(i/shapeChoice)
                        xx = cx + r * math.cos(angle)
                        yy = cy + r * math.sin(angle)
                        point = Point(xx,yy)
                        gon.vertice.append(point)
                    app.player = Player(10,gon, cx, cy)
                    app.init = False
            collisionDetection(app)
            inBoundsCheck(app)
            if(app.help):
                if(app.firstHelp):
                    bestRoute(app)
                    app.firstHelp = False
                else:
                    nextStepHelp(app)
            app.time+=1
            if(app.time==2):
                starfury(app)
                app.countdown = 100
            elif(app.time==20):
                starfury_double(app)
            elif(app.time==40):
                starfury(app)
            elif(app.time==60):
                starfury_double(app)
            elif(app.time==100):
                app.rest = True
                app.currwave+=1
                app.bullets = []
                app.countdown = 120
            elif(app.time==120):
                app.countdown = 220
                app.rest = False
                not_the_bees(app)
            elif(app.time==160):
                not_the_bees(app)
            elif(app.time==220):
                app.countdown = 240
                app.rest = True
                app.currwave+=1
                app.bullets = []
            elif(app.time==240):
                app.countdown = 340
                app.rest = False
                gravityWall(app)
            elif(app.time==250):
                gravityWall(app)
            elif(app.time==260):
                gravityWall(app)
            elif(app.time==270):
                gravityWall(app)
            elif(app.time==280):
                gravityWall(app)
            elif(app.time==290):
                gravityWall(app)
            elif(app.time==300):
                gravityWall(app)
            elif(app.time==310):
                gravityWall(app)
            elif(app.time==320):
                gravityWall(app)
            elif(app.time==330):
                gravityWall(app)
            elif(app.time==340):
                app.rest = True
                app.currwave+=1
                app.bullets = []
                app.countdown = 360
            elif(app.time==360):
                app.rest = False
                app.countdown = 460
                simplySquareHell(app, "OliveDrab1", "purple")
            elif(app.time==380):
                simplySquareHell(app, "aquamarine", "light slate blue")
            elif(app.time==400):
                simplySquareHell(app, "OliveDrab1", "purple")
            elif(app.time==420):
                simplySquareHell(app, "aquamarine", "light slate blue")
            elif(app.time==440):
                simplySquareHell(app, "OliveDrab1", "purple")
            elif(app.time==460):
                app.win = True
                # app.rest = True
                # app.currwave+=1
                # app.bullets = []
                # app.countdown = 480

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
    no = 15
    # the code below was taken from here and then modified:
    # https://www.cs.cmu.edu/~112/notes/notes-graphics.html#circlesWithTrig
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

def gravityWall_help(app, sets, speed, color, dire):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    cx, cy, r= (bf_w)/2, (bf_h)/2, min(bf_w, bf_h)/3
    # the code below was taken from here and then modified:
    # https://www.cs.cmu.edu/~112/notes/notes-graphics.html#circlesWithTrig
    no = 35
    if(dire == 1):
        for i in range(no):
            gon = Polygon(color,[],0,0)
            ox = (bf_x0+bf_w/no)*i
            oy = app.height-bf_y0
            dx = 0
            dy = -1*speed
            for i in range(3):
                cx, cy, r = ox, oy, 10
                angle = math.pi/2 - (2*math.pi)*(i/3)
                xx = cx - r * math.cos(angle)
                yy = cy - r * math.sin(angle)
                point = Point(xx,yy)
                gon.vertice.append(point)
            gon.dx = dx
            gon.dy = dy
            sets.append(gon)
    elif(dire==0):
        for i in range(no):
            gon = Polygon(color,[],0,0)
            ox = bf_x0+bf_w-(bf_x0+bf_w/no)*i
            oy = bf_y0
            dx = 0
            dy = speed
            for i in range(3):
                cx, cy, r = ox, oy, 10
                angle = math.pi/2 - (2*math.pi)*(i/3)
                xx = cx + r * math.cos(angle)
                yy = cy + r * math.sin(angle)
                point = Point(xx,yy)
                gon.vertice.append(point)
            gon.dx = dx
            gon.dy = dy
            sets.append(gon)
    elif(dire==2):
        no = 6
        for i in range(no):
            gon = Polygon(color,[],0,0)
            ox = bf_x0
            oy = random.randint(bf_y0, bf_y0+bf_h)
            dx = speed
            dy = 0
            for i in range(6):
                cx, cy, r = ox, oy, 10
                angle = math.pi/2 - (2*math.pi)*(i/6)
                xx = cx + r * math.cos(angle)
                yy = cy + r * math.sin(angle)
                point = Point(xx,yy)
                gon.vertice.append(point)
            gon.dx = dx
            gon.dy = dy
            sets.append(gon)

def gravityWall(app):
    tri1 = []
    app.bullets.append(tri1)
    gravityWall_help(app, tri1, 10, "red", 1)
    tri2 = []
    app.bullets.append(tri2)
    gravityWall_help(app, tri2, 12, "dark red", 1)
    tri3 = []
    app.bullets.append(tri3)
    gravityWall_help(app, tri3, 14, "maroon", 1)

    tri4 = []
    app.bullets.append(tri4)
    gravityWall_help(app, tri4, 10, "blue", 0)
    tri5 = []
    app.bullets.append(tri5)
    gravityWall_help(app, tri5, 12, "light blue", 0)
    tri6 = []
    app.bullets.append(tri6)
    gravityWall_help(app, tri6, 14, "cyan", 0)

    hori1 = []
    app.bullets.append(hori1)
    gravityWall_help(app, hori1, 15, "white", 2)

    hori2 = []
    app.bullets.append(hori2)
    gravityWall_help(app, hori2, 20, "white", 2)

def simplySquareHell_help(app, sets, speed, color1, color2):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    cx, cy, r= (bf_w)/2, (bf_h)/2, min(bf_w, bf_h)/3
    # the code below was taken from here and then modified:
    # https://www.cs.cmu.edu/~112/notes/notes-graphics.html#circlesWithTrig
    no = 15
    for a in range(55):
        for i in range(no):
            if(i%2==0):
                gon = Polygon(color1,[],0,0)
            else:
                gon = Polygon(color2,[],0,0)
            ox = (bf_x0+bf_w/no)*a
            oy = (bf_y0+bf_h/no)*i
            if(i%2==0):
                dx = -1*speed
            else:
                dx = speed
            dy = 0
            for i in range(4):
                cx, cy, r = ox, oy, 35
                angle = math.pi/2 - (2*math.pi)*(i/4)
                xx = cx - r * math.cos(angle)
                yy = cy - r * math.sin(angle)
                point = Point(xx,yy)
                gon.vertice.append(point)
            gon.dx = dx
            gon.dy = dy
            sets.append(gon)
    
def simplySquareHell(app, color1, color2):
    sq1 = []
    app.bullets.append(sq1)
    simplySquareHell_help(app, sq1, 10, color1, color2)

    hori1 = []
    app.bullets.append(hori1)
    gravityWall_help(app, hori1, 15, "white", 2)

    hori2 = []
    app.bullets.append(hori2)
    gravityWall_help(app, hori2, 20, "white", 2)

def not_the_bees_help(app, sets, speed, color, no):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40
    bf_w, bf_h = bf_x1-bf_x0, bf_y1-bf_y0
    cx, cy, r= (bf_w)/2, (bf_h)/2, min(bf_w, bf_h)/3
    # the code below was taken from here and then modified:
    # https://www.cs.cmu.edu/~112/notes/notes-graphics.html#circlesWithTrig
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
            yy = cy - r * math.sin(angle)
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
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bg))

def redraw_battlefield(app, canvas):
    bf_x0, bf_y0, bf_x1, bf_y1 = 40, 40, app.width/1.3-40, app.height-40

    canvas.create_image((bf_x1-bf_x0)/2+40,(bf_y1-bf_y0)/2+40, image=ImageTk.PhotoImage(app.bf))

def redraw_infoboard(app,canvas):
    ib_x0, ib_y0, ib_x1, ib_y1 = app.width/1.3, 40, app.width-40, app.height/3+40
    canvas.create_rectangle(ib_x0,ib_y0,ib_x1,ib_y1,
                            fill = "black") 
    canvas.create_text(ib_x0+30,ib_y0+30, text=f"Nebula dust left: {app.bomb}",
                            font = "Ariel 20 bold", fill="white",anchor = "w") 
    canvas.create_text(ib_x0+30,ib_y0+50, text=f"Lives left: {app.life}",
                            font = "Ariel 20 bold", fill="white",anchor = "w") 
    canvas.create_text(ib_x0+30,ib_y0+70, text=f"Countdown: {app.countdown-app.time}",
                            font = "Ariel 20 bold", fill="white",anchor = "w") 
def redraw_gg(app,canvas):
    canvas.create_rectangle(0,app.height/2-40,app.width,app.height/2+40,
                            fill = "black") 
    canvas.create_text(app.width/2, app.height/2, text=f"Kaleido's Cape has run out of power! Sorry, but you need to press spacebar and restart :(",
                            font = "Ariel 20 bold", fill="white") 

def redraw_UI(app, canvas):
    redraw_background(app, canvas)
    redraw_battlefield(app, canvas)
    redraw_infoboard(app, canvas)
def redraw_player(app, canvas):
    p = app.player
    if(isinstance(p.shape, Polygon)):
        v = p.shape.vertice
        if(len(v)==3):
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,
                                    fill = p.shape.color, outline = "white", width = 5)
        elif(len(v)==4):
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,
                                    fill = p.shape.color, outline = "white", width = 5)
        elif(len(v)==5):
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,v[4].x,v[4].y,
                                    fill = p.shape.color, outline = "white", width = 5)
        elif(len(v)==6):
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,v[4].x,v[4].y,v[5].x,v[5].y,
                                    fill = p.shape.color, outline = "white", width = 5)
        elif(len(v)==7):
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,v[4].x,v[4].y,v[5].x,v[5].y,v[6].x,v[6].y,
                                    fill = p.shape.color, outline = "white", width = 5)
        elif(len(v)==8):
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,v[4].x,v[4].y,v[5].x,v[5].y,v[6].x,v[6].y,v[7].x,v[7].y,
                                    fill = p.shape.color, outline = "white", width = 5)
        elif(len(v)==9):
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,v[4].x,v[4].y,v[5].x,v[5].y,v[6].x,v[6].y,v[7].x,v[7].y,v[8].x,v[8].y,
                                    fill = p.shape.color, outline = "white", width = 5)
        elif(len(v)==10):
            canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,v[4].x,v[4].y,v[5].x,v[5].y,v[6].x,v[6].y,v[7].x,v[7].y,v[8].x,v[8].y,v[9].x,v[9].y,
                                    fill = p.shape.color, outline = "white", width = 5)
        
    else:
        canvas.create_oval(p.cx-p.r,p.cy-p.r,p.cx+p.r,p.cy+p.r,fill="Purple",
                        outline = "white", width = 5)
def redraw_bullets(app,canvas):
    for sets in app.bullets:
        for i in range(len(sets)):
            b = sets[i]
            if(isinstance(b, Sphere)):
                canvas.create_oval(b.x-b.r,b.y-b.r,b.x+b.r,b.y+b.r,
                                    fill = b.color)
            elif(isinstance(b, Polygon)):
                if(len(b.vertice)==3):
                    v = b.vertice
                    canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,
                                    fill = b.color)
                elif(len(b.vertice)==4):
                    v = b.vertice
                    canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,
                                    fill = b.color)
                elif(len(b.vertice)==6):
                    v = b.vertice
                    canvas.create_polygon(v[0].x,v[0].y,v[1].x,v[1].y,v[2].x,v[2].y,v[3].x,v[3].y,v[4].x,v[4].y,v[5].x,v[5].y,
                                    fill = b.color)


def redraw_grid(app,canvas):
    for i in range(app.row):
        for j in range(app.col):
            x0, y0, x1, y1 = getCellBounds(app, i, j)
            canvas.create_rectangle(x0,y0,x1,y1,outline = "white")
            safex, safey = app.safe
            if(i==safex and j==safey):
                canvas.create_rectangle(x0,y0,x1,y1,fill = "red", outline = "white")

def redraw_startscreen(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = "black")
    canvas.create_image(400, 400, image=ImageTk.PhotoImage(app.kaleido))
    canvas.create_text(app.width-300,100,text="Kaleido's SKY", font="Ariel 50 bold", fill="white")
    story = """\
    Kaleido is the girl right in front of you. She has always 
    been a dreamer of some sort, dreaming about the shapes and 
    colors of the stars and the universe.

    "I want to see the stars, and be able to feel their power!"

    With that, she wears her flying cape, and goes on a stargazing
    journey. However, the cosmos is no safe place. While the stars
    are pretty, they are also dangerous if touched!! On this
    mesmerizing journey, Kaleido has to avoid touching the stars,
    or they will absorb her cape's magic, and you don't want to know
    what happens next... Good luck, my friend!
    """
    canvas.create_text(app.width-280,300,text=story, font="Ariel 17", fill="white")
    canvas.create_text(app.width-300,600,text="[Press the spacebar to continue]", font="Ariel 30", fill="white")

def redraw_directions(app, canvas):
    redraw_background(app,canvas)
    canvas.create_rectangle(200,70,app.width-200,app.height-70,fill = "black")
    directions = """\
    Surviving:
    To survive, simply avoid all the stars until the countdown on the right side of the 
    screen go down to zero. By then, that wave is "cleared", and the next wave will start.
    There will be rewards after you clear each wave!

    When you touch a star, you will lose a life, and when all lives are lost, your cape
    loses power, and you will need to start over. You start out with 30 lifes.

    Moving and Restarting:
    To move, simply press the arrowkeys on your keyboard, and you will move in that direction.
    To restart at any point in the game, simply press "r".

    Bottles of Nebula dust:
    If the stars get too dense, and you sense danger, feel free to use some nebula dust by pressing "f".
    By using a bottle of nebula dust, you clear the stars that are close around you.
    You start out with 5 bottles of them (so be sure to use them at the right time).
    When you lose a life, a bottle will be used automatically, but this bottle is free, 
    so it won't deduct anything from your bottle count.

    Kaleido's Wonderful Kaleidoscope:
    Kaleido has a wonderful kaleidoscope; appearently it works with a magic spell called "BFS",
    though no one really knows what that stands for. When you look through the kaleidoscope, 
    it lights up the nearest safe spot for you to go to. After you arrive at that spot, it lights
    up the next safest spot for you, and so on. Watch through the kaleidoscope by pressing "d"

    Alright! You are all set. Press spacebar again to continue, and have fun!
    """
    canvas.create_text(app.width/2,app.height/2,text=directions, font="Ariel 20", fill="white")

def redraw_rest(app, canvas):
    canvas.create_rectangle(0,app.height/2-40,app.width,app.height/2+40,
                            fill = "black") 
    canvas.create_text(app.width/2, app.height/2, text=f"Wave {app.currwave} cleared!! Countdown until next wave: {app.countdown-app.time}",
                            font = "Ariel 20 bold", fill="white") 

def redraw_ending(app, canvas):
    redraw_background(app,canvas)
    canvas.create_rectangle(40,40,app.width/2-10,app.height-40,fill = "black")
    canvas.create_image(app.width-350, 400, image=ImageTk.PhotoImage(app.kaleido2))
    canvas.create_text(40+(app.width/2-50)/2,100,text="Kaleido's SKY", font="Ariel 50 bold", fill="white")
    ending = """\
    "Wow, that was an exciting ride," Kaleido said.

    She took out her kaleidoscope from her pocket. Now that all the stars
    are gone, it returned to a normal kaleidoscope. "Hmph," she smiled,
    "that 'BFS' magic sure saved me many times. I was soooo close to dying
    on that last wave!" She saw some orange light start to rise from the 
    east; the sun was about to come out.

    "Aww man, already?! My essay is due today!!" She laughed.
    Kaleido looked up, at the infinitely stretching cosmos above her and 
    every other thing on the Earth. "Maybe", she thought, "one day I'll 
    be able to visit other galaxies, and look at the stars there." She
    looked at the disappearing stars for one last time, and started to
    fly back home.
    
    ---------------------------------------------------------------------
    Developer thoughts:
    Wow! You've completed my game! Congrats! It's quite a hard game, isn't
    it? I had much trouble beating it myself too, hehe. I also hope you
    liked my drawing of Kaleido! I didn't have much time to do this project,
    otherwise I would've spent like 3 days just drawing her XD

    Huh? You ask me why did I make a bullet hell game? Well, I'm a fan of 
    the Touhou Project, and things started there. Definitely check it out,
    because you will then see bullet patterns that are for real mesmerizing.
    Anyways, thanks for trying it out, and I hope you have a lovely day :)

    [Press "r" to return to the start screen]
    """
    canvas.create_text((app.width/2-50)/2+25,450,text=ending, font="Ariel 17", fill="white")

def redrawAll(app, canvas):
    if(app.win):
        redraw_ending(app, canvas)
    elif(app.startscreen):
        redraw_startscreen(app, canvas)
    elif(app.directions):
        redraw_directions(app, canvas)
    else:
        redraw_UI(app,canvas)
        if(app.help):
            redraw_grid(app,canvas)
        redraw_bullets(app,canvas)
        redraw_player(app,canvas)
        if(app.rest):
            redraw_rest(app,canvas)
        elif(app.gg):
            redraw_gg(app,canvas)

runApp(width=2560, height=1600)