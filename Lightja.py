import math
import pygame
pygame.init()

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

w = pygame.display.set_mode((600, 600))
c = pygame.time.Clock()

oim = pygame.image.load("Ninja.png")

oim = pygame.transform.scale(oim, (48, 48))

im = oim
    
targ_angle = 0
angle = 0
pa = 0

turnSpeed = .5


flyRad = 10
flyRenRad = 2
flySpeed = .25

flys = [(100, 100) for i in range(1)]

x = 300
y = 300

speed = .15

doneAddition = False
circleAdd = 0

running = True
while running:
    c.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    w.fill((127, 127, 127))
    
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
            targ_angle = -45
        if right == 1 and up == 1:
            targ_angle = 45
        if right == 1 and up == -1:
            targ_angle = 315
        
        print(pa, angle, targ_angle)

        if pa == 270 + (circleAdd * 360) and targ_angle == 0:
            circleAdd += 1
        if pa == 0 + (circleAdd * 360) and targ_angle == 270:
            circleAdd -= 1

        angle = lerp(pa, targ_angle + (circleAdd * 360), turnSpeed)
        pa = round(angle)

        
        im = pygame.transform.rotate(oim, angle-90)
        
        x += math.cos(angle * math.pi/180) * speed * c.get_time()
        y += math.sin(angle * math.pi/180) * speed * c.get_time()

    w.blit(im, (x-(im.get_width()/2), (600-y)-(im.get_height()/2)))
    
    pygame.display.flip()
pygame.quit()
