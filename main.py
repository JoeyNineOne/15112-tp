from cmu_112_graphics import *
import math, time
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
    app.spellcard = "Starfury!"
    app.bullets = []
    app.working = False
    app.time = 0
    app.doubleMode = False
    app.score = 0
    app.life = 5
    app.bomb = 3
    app.init = True
    app.player = Player(0,Sphere("white",0,0,0,0,0),0,0)
    app.gg = False
    app.hasBomb = False
    app.help = False
    app.grid = []
    app.row = 20
    app.col = 20
    app.safe = -999,-999
    app.startscreen = True
    app.directions = False
    app.countdown = 0
    app.endtime = 0
    app.ready = False
    app.currwave = 1
    app.rest = False

def keyPressed(app, event):
    if(not app.gg):
        if (event.key == 'Up'):
            if(isinstance(app.player.shape,Polygon)):
                for i in range(len(app.player.shape.vertice)):
                    app.player.shape.vertice[i].y -= 15
            app.player.cy -= 15
        elif (event.key == 'Down'): 
            if(isinstance(app.player.shape,Polygon)):
                for i in range(len(app.player.shape.vertice)):
                    app.player.shape.vertice[i].y += 15
            app.player.cy += 15
        elif (event.key == 'Left'):
            if(isinstance(app.player.shape,Polygon)):
                for i in range(len(app.player.shape.vertice)):
                    app.player.shape.vertice[i].x -= 15
            app.player.cx -= 15
        elif (event.key == 'Right'):
            if(isinstance(app.player.shape,Polygon)):
                for i in range(len(app.player.shape.vertice)):
                    app.player.shape.vertice[i].x += 15
            app.player.cx += 15
        elif(event.key =="r"):
            appStarted(app)
        # elif(event.key=="f" and app.bomb>0):
            # pass
            # app.hasBomb = True
            # app.bomb-=1
            # bomb(app)
        elif(event.key=="d"):
            app.help = not app.help
        elif(event.key=="Space" and app.startscreen):
            app.directions = True
            app.startscreen = False
        elif(event.key=="Space" and app.directions):
            app.directions = False
        elif(event.key=="Space" and app.rest and not app.ready):
            app.ready = True

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
    startx, starty = getCell(app,app.player.cx,app.player.cy)
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
        print()
        print(grid[x][y], end = " ")
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
                    # else:
                    #     for v in b.vertice:
                    #         if(x0<b.x and b.x<x1 and y0<b.y and b.y<y1):
                    #             grid[i][j] += 1
                                
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
            if(isinstance(app.player.shape,Sphere) and isinstance(b,Sphere)):
                if(((b.x-p.cx)**2+(b.y-p.cy)**2)**0.5<b.r+p.r):
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
                        app.life-=1

def polygonPolygonCollision(app):
    # ill annotate it this afternoon, its 8 am and i need to sleep hehe
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
    row,col = getCell(app, app.player.cx, app.player.cy)
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
                while(not app.ready):
                    pass
                app.currwave+=1
                app.rest = False
                app.bullets = []
            nextStepHelp(app)
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
                if(len(b.vertice)==6):
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
    loses power, and you will need to start over. You start out with 5 lifes, but you 
    will be rewarded with more at the end of some waves.

    Moving:
    To move, simply press the arrowkeys on your keyboard, and you will move in that direction.

    Bottles of Nebula dust:
    If the stars get too dense, and you sense danger, feel free to use some nebula dust by pressing "f".
    By using a bottle of nebula dust, you clear the stars that are close around you.
    You start out with 5 bottles of them (so be sure to use them at the right time), but you 
    will be rewarded with more at the end of some waves. When you lose a life, a bottle will be 
    used automatically, but this bottle is free, so it won't deduct anything from your bottle count.

    Kaleido's Wonderful Kaleidoscope:
    Kaleido has a wonderful kaleidoscope; appearently it works with a magic spell called "BFS",
    though no one really knows what that stands for. When you look through the kaleidoscope, 
    it lights up the nearest safe spot for you to go to. After you arrive at that spot, it lights
    up the next safest spot for you, and so on. Watch through the kaleidoscope by pressing "d"

    Alright! You are all set. Press spacebar again to continue, and have fun!
    """
    canvas.create_text(app.width/2,app.height/2,text=directions, font="Ariel 20", fill="white")

def redraw_ready(app, canvas):
    canvas.create_rectangle(0,app.height/2-40,app.width,app.height/2+40,
                            fill = "black") 
    canvas.create_text(app.width/2, app.height/2, text=f"Wave {app.currwave} cleared!! Press spacebar to continue",
                            font = "Ariel 20 bold", fill="white") 

def redrawAll(app, canvas):
    if(app.startscreen):
        redraw_startscreen(app, canvas)
    elif(app.directions):
        redraw_directions(app, canvas)
    elif(app.gg):
        redraw_gg(app,canvas)
    else:
        redraw_UI(app,canvas)
        if(app.help):
            redraw_grid(app,canvas)
        if(app.rest and not app.ready):
            redraw_ready(app,canvas)
        redraw_bullets(app,canvas)
        redraw_player(app,canvas)

runApp(width=2560, height=1600)