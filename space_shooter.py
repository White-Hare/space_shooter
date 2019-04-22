import pygame as pg
import random
import math
import os

WIDTH,HEIGHT=600,400

pg.init()
screen=pg.display.set_mode((WIDTH,HEIGHT),0,32)

def write(msg,color=(255,255,255)):
    font=pg.font.SysFont("none",15)
    text=font.render(msg,True,color)
    text.convert()
    return text

clock=pg.time.Clock()
FPS=60
running=True

screen.fill((50,50,50))


class Enemies(pg.sprite.Sprite):

    r=5
    targetpos=(WIDTH/2,HEIGHT/2)

    def __init__(self,pos=[0,0],area=screen.get_rect(),):
        pg.sprite.Sprite.__init__(self,self.groups)
        
        self.image=pg.Surface((Enemies.r*2,Enemies.r*2))
        pg.draw.circle(self.image,(200,0,0),(Enemies.r,Enemies.r),Enemies.r)
        self.image.set_colorkey((0,0,0))
        self.image.convert()

        self.radius=Enemies.r
        self.rect=self.image.get_rect()
        self.pos=pos.copy()

        self.area=area


        
    def update(self,time):
        if self.area.contains(self.rect):
            x1=Enemies.targetpos[0]
            y1=Enemies.targetpos[1]
            x2=self.pos[0]
            y2=self.pos[1]
            d=50

            self.dx=((x1-x2)/((x1-x2)**2+(y1-y2)**2)**0.5)*d*time
            self.dy=((y1-y2)/((x1-x2)**2+(y1-y2)**2)**0.5)*d*time

            self.pos[0]+=self.dx
            self.rect.centerx=self.pos[0]
            self.pos[1]+=self.dy
            self.rect.centery=self.pos[1]


        else:
            self.kill()

Enemies.r=7

class Hero(pg.sprite.Sprite):
    r=5
    def __init__(self,area=screen.get_rect()):
        pg.sprite.Sprite.__init__(self,self.groups)
        
        self.image=pg.Surface((self.r*2,self.r*2))
        pg.draw.circle(self.image,(0,0,200),(self.r,self.r),self.r)
        self.image.set_colorkey((0,0,0))
        self.image.convert()

        self.rect=self.image.get_rect()
        self.radius=self.r

        self.area=area
        self.pos=[20,20]

        self.speed=250


    def update(self,time):
        key=pg.key.get_pressed()
        dx,dy=0,0

        if key[pg.K_w]:
            dy=-self.speed*time
        if key[pg.K_s]:
            dy=self.speed*time
        if key[pg.K_d]:
            dx=self.speed*time
        if key[pg.K_a]:
            dx=-self.speed*time

        if dx+self.rect.left>self.area.left and dx+self.rect.right<self.area.right:
            self.pos[0]+=dx

        if dy+self.rect.top>self.area.top and dy+self.rect.bottom<self.area.bottom:
            self.pos[1]+=dy

        self.rect.centerx=self.pos[0]
        self.rect.centery=self.pos[1]


class Bullets(pg.sprite.Sprite):
    r=2
    def __init__(self,pos=[0,0],targetpos=[0,0],area=screen.get_rect()):
        pg.sprite.Sprite.__init__(self,self.groups)

        self.image=pg.Surface((self.r*2,self.r*2))
        pg.draw.circle(self.image,(210,210,210),(self.r,self.r),self.r)
        self.image.set_colorkey((0,0,0))
        self.image.convert()

        self.radius=self.r
        self.rect=self.image.get_rect()
        
        self.pos=pos.copy()
        self.area=area

        self.targetpos=targetpos
        self.angle=math.atan2((self.targetpos[1]-self.pos[1]),(self.targetpos[0]-self.pos[0]))
        self.v=700

    def update(self,time):       


        if self.area.contains(self.rect):
            self.pos[0]+=self.v*math.cos(self.angle)*time
            self.pos[1]+=self.v*math.sin(self.angle)*time

            self.rect.centerx=self.pos[0]
            self.rect.centery=self.pos[1]

        else:
            self.kill()


allgroups=pg.sprite.Group()
enemygroup=pg.sprite.Group()
bulletgroup=pg.sprite.Group()

Enemies.groups=allgroups,enemygroup
Hero.groups=allgroups
Bullets.groups=allgroups,bulletgroup

background=pg.Surface(screen.get_rect()[2:])
background.fill((50,50,50))

screen.blit(background,(0,0))

frequency=1
bulletfrequency=0.2
f=0
bf=0
maxenemynumber=100

score=0
bullettarget=[]

#spawnpoints=([2*Enemies.r,2*Enemies.r],[WIDTH-2*Enemies.r,2*Enemies.r],[2*Enemies.r,HEIGHT-2*Enemies.r],[WIDTH-2*Enemies.r,HEIGHT-2*Enemies.r])
spawnpoints=([WIDTH/2-2*Enemies.r,HEIGHT/2-2*Enemies.r],[WIDTH/2+2*Enemies.r,HEIGHT/2-2*Enemies.r],[WIDTH/2-2*Enemies.r,HEIGHT/2+2*Enemies.r],[WIDTH/2+2*Enemies.r,HEIGHT/2+2*Enemies.r])

hero=Hero()
allgroups.add(hero)

while running:
    screen.fill((50,50,50))

    time=clock.tick(FPS)/1000.0
    #print(1/time)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                running=False

                    
    f+=time
    bf+=time
    if f>frequency and len(enemygroup)<=maxenemynumber:    
        for s in spawnpoints:
            enemy=Enemies(s)
            enemygroup.add(enemy)
            allgroups.add(enemy)
        f=0

    Enemies.targetpos=hero.pos

            
    if bf>bulletfrequency and pg.mouse.get_pressed()[0]:
        mousepos=pg.mouse.get_pos()
        bullet=Bullets(hero.pos,mousepos)
        bulletgroup.add(bullet)
        allgroups.add(bullet)
        bf=0

    collision=pg.sprite.spritecollide(hero,enemygroup,True,pg.sprite.collide_circle)
    if collision:
        i=0

    for bullet in bulletgroup.sprites():
        if pg.sprite.spritecollide(bullet,enemygroup,True,pg.sprite.collide_circle):
            score+=1


    allgroups.clear(screen,background)
    allgroups.update(time)

    group=enemygroup.sprites()
    i=0
    while i <len(group):
        enemy=group[i]
        tgroup=group.copy()
        tgroup.remove(enemy)
        for enemy2 in tgroup:

            xDistance=enemy.pos[0]-enemy2.pos[0]
            yDistance=enemy.pos[1]-enemy2.pos[1]

            if enemy.radius+enemy2.radius>=(xDistance**2+yDistance**2)**0.5:
                

                xVelocity=enemy2.dx-enemy.dx
                yVelocity=enemy2.dy-enemy.dy
                dotProuduct=xDistance*xVelocity+yDistance*yVelocity

                if(dotProuduct>0):
                   collisionScale=dotProuduct/(xDistance**2+yDistance**2)
                   xCollision=xDistance*collisionScale
                   yCollision=yDistance*collisionScale

                   enemy.dx+=xCollision-enemy.dx
                   enemy.dy+=yCollision-enemy.dy
                   enemy2.dx-=xCollision+enemy2.dx
                   enemy2.dy-=yCollision+enemy2.dy

                   enemy.pos[0]+=enemy.dx
                   enemy.pos[1]+=enemy.dy
                   enemy2.pos[0]+=enemy2.dx
                   enemy2.pos[1]+=enemy2.dy
        i+=1

    allgroups.draw(screen)


    text=write("SCORE: "+str(score))
    screen.blit(text,(0,0))
    pg.display.update(text.get_rect())
    pg.display.flip()

pg.quit()