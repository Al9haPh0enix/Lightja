import math
import sys
import pygame
pygame.init()

#pygame.mixer.init()
#pygame.mixer.music.load("Chill_Final_Draft.mp3")
#pygame.mixer.music.play(-1)

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

def get_angle(x1, y1, x2, y2):
    return -math.atan2(y2 - y1, x2 - x1)/(math.pi/180)

def findTargetAngle(right, up):
    if right == 1:
        targ_angle = 0
    if right == -1:
        targ_angle = 180
    if up == 1:
        targ_angle = 90
    if up == -1:
        targ_angle = 270

    if right == -1 and up == 1:
        targ_angle = 135
    if right == -1 and up == -1:
        targ_angle = 225
    if right == 1 and up == 1:
        targ_angle = 45 
    if right == 1 and up == -1:
        targ_angle = 315
    
    return targ_angle

def intersects(circleP, circleR, rect):
    circleDistance_x = abs(circleP[0] - rect.x);
    circleDistance_y = abs(circleP[1] - rect.y);

    if (circleDistance_x > (rect.width/2 + circleR)):  return False
    if (circleDistance_y > (rect.height/2 + circleR)): return False

    if (circleDistance_x <= (rect.width/2)):    return True
    if (circleDistance_y <= (rect.height/2)):   return True

    cornerDistance_sq = (circleDistance_x - rect.width/2)**2 + (circleDistance_y - rect.height/2)**2

    return (cornerDistance_sq <= (circleR**2))

def raycast(spx, spy, lix, liy, angle, level, max = 600):
    xa = math.cos(angle * math.pi/180)
    ya = math.sin(angle * math.pi/180)
    for i in range(0, max, 5):

        cx = spx + (xa*i)
        cy = spy + (ya*i)

        pygame.draw.circle(w, (255, 0, 0), (cx, cy), 2)

        for ly in range(len(level)):
            for lx in range(len(level[ly])):
                if level[ly][lx] == "0":
                    if cx > lx*snap and cy > ly*snap and cx < (lx*snap)+snap and cy < (ly*snap)+snap:
                        return False
        d = math.dist((cx, cy), (lix, height-liy))
        if d < 10:
            return True
    return True

bugs = [
]

bangles = [
]
    
with open("level3.lightja", "r") as f:
    level = [i.strip().split(" ") for i in f.readlines()]

width, height = 640, 640

entities = []

for ly in level:
    if ly[0] == "entity":
        if ly[1] == "key":
            kx = int(ly[2])
            ky = int(ly[3])

            entities.append([kx, ky, "key"])
        elif ly[1] == "movingWall":
            wx = int(ly[2]) #x
            wy = int(ly[3]) #y
            wi = int(ly[4]) #width
            he = int(ly[5]) #height
            direc = ly[6]   #direction
            dist = int(ly[7]) #distance it will move

            entities.append([wx, wy, wi, he, direc, dist, "False", 0, "movingWall"]) #original x, original y, width, height, direction, distance to move, is moving, how far already moved, name
        elif ly[1] == "pressurePlate":
            px = int(ly[2])
            py = int(ly[3])
            amountAboveTriggered = int(ly[4])

            entities.append([px, py, amountAboveTriggered, "pressurePlate"]) #x, y, amount above triggered, name
        elif ly[1] == "light":
            lix = int(ly[2])
            liy = int(ly[3])
            on = ly[4] == "True"

            entities.append([lix, liy, on, "light"]) #x, y, on, name
        elif ly[1] == "bug":
            bx = int(ly[2])
            by = int(ly[3])

            bugs.append([bx, by]) #x, y
            bangles.append(0)

    

w = pygame.display.set_mode((width, height))
c = pygame.time.Clock()

pygame.display.set_caption('Credit to Al9haph0enix (coder), Dangerdrone ("creative" lead), and Kunpao (music)')

oplayer_im = pygame.image.load("Ninja.png")
obug1_im = pygame.image.load("Bug1.png")
obug2_im = pygame.image.load("Bug2.png")
owall_im = pygame.image.load("Wall.png")
okey_im = pygame.image.load("Key.png")
ofloor_im = pygame.image.load("FloorTile.png")
odoor_im = pygame.image.load("Door.png")
osdoor_im = pygame.image.load("SlidingDoor.png")
olon_im = pygame.image.load("lightOn.png")
oloff_im = pygame.image.load("lightOff.png")

oplayer_im = pygame.transform.scale(oplayer_im, (64, 64))
obug1_im = pygame.transform.scale(obug1_im, (64, 64))
obug2_im = pygame.transform.scale(obug2_im, (64, 64))
owall_im = pygame.transform.scale(owall_im, (64, 64))
okey_im = pygame.transform.scale(okey_im, (32, 32))
ofloor_im = pygame.transform.scale(ofloor_im, (64, 64))
odoor_im = pygame.transform.scale(odoor_im, (64, 64))
ofloor_im = pygame.transform.scale(ofloor_im, (64, 64))
osdoor_im = pygame.transform.scale(osdoor_im, (64, 64))
olon_im = pygame.transform.scale(olon_im, (64, 64))
oloff_im = pygame.transform.scale(oloff_im, (64, 64))

player_im = oplayer_im

currentLevel = 1
    
targ_angle = 0
angle = 0
pta = 0

pTurnSpeed = 0.4

bounding = 64

md = 3

pickedUp = None

bugRad = 10
bugRenRad = 2
bugSpeed = .3

mapSize = 10

snap = 640/mapSize

for lx in range(10):
    for ly in range(10):
        if level[ly][lx] == "2":
            x = (lx*snap)+(snap/2)
            y = height-((ly*snap)+(snap/2))

pickupRange = 50

speed = .15

def load(levelName):
    global targ_angle
    global angle
    global pta
    global x
    global y
    global pickedUp
    global player_im
    global bugs
    global bangles
    global entities
    global level

    targ_angle = 0
    angle = 0
    pta = 0
    
    with open(levelName+".lightja", "r") as f:
        level = [i.strip().split(" ") for i in f.readlines()]
        
    for lx in range(10):
        for ly in range(10):
            if level[ly][lx] == "2":
                x = (lx*snap)+(snap/2)
                y = height-((ly*snap)+(snap/2))
    
    player_im = oplayer_im
    
    pickedUp = None

    bugs = []
    bangles = []

    entities = []

    for ly in level:
        if ly[0] == "entity":
            if ly[1] == "key":
                kx = int(ly[2])
                ky = int(ly[3])

                entities.append([kx, ky, "key"])
            elif ly[1] == "movingWall":
                wx = int(ly[2]) #x
                wy = int(ly[3]) #y
                wi = int(ly[4]) #width
                he = int(ly[5]) #height
                direc = ly[6]   #direction
                dist = int(ly[7]) #distance it will move

                entities.append([wx, wy, wi, he, direc, dist, "False", 0, "movingWall"]) #original x, original y, width, height, direction, distance to move, is moving, how far already moved, name
            elif ly[1] == "pressurePlate":
                px = int(ly[2])
                py = int(ly[3])
                amountAboveTriggered = int(ly[4])

                entities.append([px, py, amountAboveTriggered, "pressurePlate"]) #x, y, amount above triggered, name
            elif ly[1] == "light":
                lix = int(ly[2])
                liy = int(ly[3])
                on = ly[4] == "True"

                entities.append([lix, liy, on, "light"]) #x, y, on, name
            elif ly[1] == "bug":
                bx = int(ly[2])
                by = int(ly[3])

                bugs.append([bx, by]) #x, y
                bangles.append(0)
load("level"+str(currentLevel))
running = True
while running:
    c.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    for ly in range(len(level)):
        for lx in range(len(level[ly])):
            r = pygame.Rect(lx * snap, ly * snap, snap, snap)
            if level[ly][lx] == "1": #floor
                w.blit(ofloor_im, (lx * snap, ly * snap) )
                
            if level[ly][lx] == "2": #entrance
                w.blit(ofloor_im, (lx * snap, ly * snap) )
                odoor_imf = pygame.transform.flip(odoor_im, False, True)
                w.blit(odoor_imf, (lx * snap, ly * snap) )
                
            if level[ly][lx] == "3": #exit
                w.blit(ofloor_im, (lx * snap, ly * snap) )
                w.blit(odoor_im, (lx * snap, ly * snap) )
    
    for i in entities:
        if i[-1] == "movingWall":
            ox = i[0]
            oy = i[1]
            if i[6] == "True":
                if i[4] == "left":
                    ox -= lerp(0, i[5], i[7])
                if i[4] == "up":
                    oy += lerp(0, i[5], i[7])
                if i[4] == "right":
                    ox += lerp(0, i[5], i[7])
                if i[4] == "down":
                    oy -= lerp(0, i[5], i[7])
            w.blit(osdoor_im, (ox * snap, oy * snap)) 
    
    for ly in range(len(level)):
        for lx in range(len(level[ly])):
            r = pygame.Rect(lx * snap, ly * snap, snap, snap)
            if level[ly][lx] == "0": #wall
                w.blit(owall_im, (lx * snap, ly * snap) )
    
    keys = pygame.key.get_pressed()

    up = 0
    right = 0

    if keys[pygame.K_w]:
        up += 1
    if keys[pygame.K_s]:
        up -= 1
    if keys[pygame.K_d]:
        right += 1
    if keys[pygame.K_a]:
        right -= 1

    if right != 0 or up != 0:

        targ_angle = findTargetAngle(right, up)

        if pta == 315 and targ_angle == 0:
            angle -= 360
        if pta == 0 and targ_angle == 315:
            angle += 360

        while angle < -720:
            angle += 360
        while angle > 720:
            angle -= 360

        for i in range(50):
            if angle < targ_angle:
                angle += (pTurnSpeed * c.get_time())/50
            elif angle > targ_angle:
                angle -= (pTurnSpeed * c.get_time())/50
        
        angle = round(angle)
        
        #angle = targ_angle
        pta = targ_angle

        
        player_im = pygame.transform.rotate(oplayer_im, angle-90)

        inx = False
        iny = False
        
        for ly in range(len(level)):
            for lx in range(len(level[ly])):
                r = pygame.Rect((lx * snap) + snap/2, height-((ly * snap) + snap/2), snap, snap)
                if level[ly][lx] == "0":
                    if intersects((x+(right * speed * c.get_time()), y), 28, r):
                        inx = True
                    if intersects((x, y+(up * speed * c.get_time())), 28, r):
                        iny = True

        if not inx:
            x += right * speed * c.get_time()
        if not iny:
            y += up    * speed * c.get_time()
    
    for i in entities:
        if i[2] == "key":
            pos = i[0:2]
            #held
            w.blit(okey_im, ((pos[0] * snap)-16, (pos[1] * snap)-16))

            if math.dist((x, y), (pos[0] * snap, height-(pos[1] * snap))) < pickupRange+28 and keys[pygame.K_e]:
                pickedUp = entities.index(i)
        elif i[-1] == "movingWall":
            pos = i[0:2]
            if i[6]=="True":
                i[7] += .001 * c.get_time()
                if i[7] > 1:
                    i[7] = 1
        elif i[-1] == "light":
            pos = i[0:2]
            if i[2]:
                w.blit(olon_im, ((pos[0] * snap), (pos[1] * snap)))
            else:
                w.blit(oloff_im, ((pos[0] * snap), (pos[1] * snap)))
    
    if keys[pygame.K_q]:
        pickedUp = None
    
    if pickedUp != None:
        entities[pickedUp][0] = x/snap
        entities[pickedUp][1] = (height-y)/snap

    w.blit(player_im, (x-(player_im.get_width()/2), (height-y)-(player_im.get_height()/2)))

    for i in range(len(bugs)):
        rotBugIm = pygame.transform.rotate(obug1_im, bangles[i]-90)
        w.blit(rotBugIm, (bugs[i][0]-(rotBugIm.get_width()/2), (height-bugs[i][1])-(rotBugIm.get_height()/2)))

        bx = bugs[i][0]
        by = height-(bugs[i][1])

        r = pygame.Rect(bx-bounding/2, by-bounding/2, bounding, bounding)

        ld = math.inf
        lp = None

        canMove = True

        for j in entities:
            if j[-1] == "light" and j[2]:
                ray = raycast(bx, by, (j[0] * snap)+32, (height-(j[1] * snap))-32, get_angle((j[0]*snap)+32, (height-(j[1]*snap))-32, bx, height-by)+180, level)
                if ray:
                    d = math.dist(bugs[i], ((j[0] * snap)+32, (height-(j[1] * snap))-32))

                    if d < ld:
                        ld = d
                        lp = (j[0] * snap)+32, (height-(j[1] * snap))-32
                    
                    if d < md:
                        canMove = False
                else:
                    canMove = False
            if j[-1] == "key":
                ray = raycast(bx, by, (j[0] * snap), (height-(j[1] * snap)), get_angle((j[0]*snap), (height-(j[1]*snap)), bx, height-by)+180, level)
                if ray:
                    d = math.dist(bugs[i], ((j[0] * snap), (height-(j[1] * snap))))

                    if d < ld:
                        ld = d
                        lp = (j[0] * snap), (height-(j[1] * snap))
                    
                    if d < md:
                        canMove = False
                else:
                    canMove = False
        
        if canMove:

            canx = True
            cany = True

            for ly in range(len(level)):
                for lx in range(len(level[ly])):
                    r = pygame.Rect((lx * snap) + snap/2, height-((ly * snap) + snap/2), snap, snap)
                    if level[ly][lx] == "0":
                        if intersects((bugs[i][0] + math.cos((bangles[i]) * math.pi/180)*bugSpeed * c.get_time(), bugs[i][1]), bounding/2, r):
                            canx = False
                        if intersects((bugs[i][0], bugs[i][1] + math.sin((bangles[i]) * math.pi/180)*bugSpeed * c.get_time()), bounding/2, r):
                            cany = False
            if canx:
                bugs[i][0] += math.cos((bangles[i]) * math.pi/180)* bugSpeed * c.get_time()
            if cany: 
                bugs[i][1] += math.sin((bangles[i]) * math.pi/180)* bugSpeed * c.get_time()

            bangles[i] = get_angle(lp[0], height-lp[1], bugs[i][0], height-bugs[i][1])+180

        if math.dist((x, y), (bx, by)) < 28+28:
            load("level"+str(currentLevel))
    if keys[pygame.K_e]:
        breakOut = False
        for ly in range(len(level)-1):
            for lx in range(len(level[ly])):
                if level[ly][lx] == "3":
                    if math.dist((x, y), (lx*snap, height-(ly*snap))) < pickupRange:
                        if entities[pickedUp][-1] == "key":
                            currentLevel += 1
                            if currentLevel > 5:
                                sys.exit()
                            load("level"+str(currentLevel))
                            breakOut = True
                            break
            if breakOut:
                break
    
    
    pygame.display.flip()
pygame.quit()
