import pygame
pygame.init()

w = pygame.display.set_mode((640, 640))
c = pygame.time.Clock()

with open("level2.lightja", "r") as f:
    level = [i.strip().split(" ") for i in f.readlines()]

entities = []

for y in range(len(level)):
    if level[y][0] == "entity":
        if level[y][1] == "key":
            kx = int(level[y][2])+.5
            ky = int(level[y][3])+.5

            entities.append((kx, ky, "key"))
        elif level[y][1] == "movingWall":
            wx = int(level[y][2])
            wy = int(level[y][3])
            wi = int(level[y][4])
            he = int(level[y][5])
            direc = level[y][6]
            dist = int(level[y][7])

            entities.append([wx, wy, wi, he, direc, dist, False, 0, "movingWall"]) #x, y, width, height, direction, distance to move, is moving, how far already moved, name
        
        elif level[y][1] == "pressurePlate":
            wx = int(level[y][2])
            wy = int(level[y][3])

            entities.append([wx, wy, "pressurePlate"]) #x, y, name

print()

for i in level:
    print(i)


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

running = True
while running:
    c.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    w.fill((0, 0, 0))

    snap = 64
    
    for y in range(len(level)):
        for x in range(len(level[y])):
            r = pygame.Rect(x * snap, y * snap, snap, snap)
            if level[y][x] == "0": #wall
                pygame.draw.rect(w, (0, 0, 0), r)
                
            if level[y][x] == "1": #floor
                pygame.draw.rect(w, (127, 127, 127), r)
                
            if level[y][x] == "2": #entrance
                pygame.draw.rect(w, (0, 255, 0), r)
                
            if level[y][x] == "3": #exit
                pygame.draw.rect(w, (255, 0, 0), r)
        
    for i in entities:

        if i[-1] == "movingWall":
            pos = i[0:2]
            if i[6]:
                if i[4] == "left":
                    pos[0] -= lerp(0, i[5], i[7])
                if i[4] == "up":
                    pos[1] += lerp(0, i[5], i[7])
                if i[4] == "right":
                    pos[0] += lerp(0, i[5], i[7])
                if i[4] == "down":
                    pos[1] -= lerp(0, i[5], i[7])
                i[7] += .001 * c.get_time()
                if i[7] > 1:
                    i[7] = 1
            pygame.draw.rect(w, (50, 50, 50), pygame.Rect((pos[0] * snap), (pos[1] * snap), snap, snap))
        elif i[-1] == "pressurePlate":
            pos = i[0:2]
            pygame.draw.rect(w, (127, 127, 50), pygame.Rect((pos[0] * snap), (pos[1] * snap), snap, snap))
        elif i[-1] == "key":
            pos = i[0:2]
            pygame.draw.rect(w, (255, 255, 0), pygame.Rect((pos[0] * snap)-10, (pos[1] * snap)-5, 20, 10))
    
    pygame.display.flip()
