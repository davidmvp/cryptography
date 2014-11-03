import os as OS
import sys as SYS
import random
import pygame as PY
import pygame.display as PD
import pygame.event as PE
import pygame.image as PI
import pygame.sprite as PS
import Setup
import GameScreen
import Projectile
from smooth import Entity
import Functions
from Character import BaseClass
from Screen import Globals
SPEED = 1

Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir), 'Images/Skeleton.png')
skull = OS.path.join(OS.path.dirname(Dir), 'Images/skull.png')

MIN_MOVE_DURATION = 20
MAX_MOVE_DURATION = 50
MAX_HEALTH = 3.0
PROJECTILE_TIMER = 150


class Enemy(Entity):
    ra = False
    def __init__(self,x,y, boole):
        self.ra = boole
        print(self.ra)
        IMAGES = None
        Entity.__init__(self)
        self.image_tracker = 0
        if not IMAGES:
            self.load_images()
        self.image = self.IMAGES[self.image_tracker]
        self.rect = self.image.get_rect()
        self.direction = 0
        self.moveCounter = 0  # allows for smooth enemy movement
        self.moveDuration = 0  # randomly generated for random movements
        self.health = 20
        self.attack_rect = (0, 0)

        #  Boundaries for the enemy
        self.MIN_X_POS = self.rect.width/2
        self.MAX_X_POS = Globals.WORLD.realwidth - self.rect.width/2
        self.MIN_Y_POS = self.rect.height/2
        self.MAX_Y_POS = Globals.WORLD.realheight - self.rect.height/2
        self.rect.centerx = x
        self.rect.centery = y
        # choose starting position
        # self.rect.centerx = random.randint(self.MIN_X_POS, self.MAX_X_POS)
        #self.rect.centery = random.randint(self.MIN_Y_POS, self.MAX_Y_POS)

        # Projectile timer
        self.pTimer = 0

    #  load enemy sprite
    def load_images(self):
        Enemy.IMAGES = []
        sheet = PI.load(image_path).convert()
        key = sheet.get_at((0, 0))
        for i in range(3):
            for j in range(4):
                surface = PY.Surface((32, 32)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*32, j*32, 32, 32))
                Enemy.IMAGES.append(surface)

    def update_image(self, image_num):
        self.image = Enemy.IMAGES[image_num]
        self.image.convert_alpha()
        self.image_tracker = (self.image_tracker + 1) % 3

    #  move enemy, then detect for collisions
    # and throw projectiles as necessary
    def update(self, wallMap, hero):
        self.pTimer += 1
        herorect = hero.rect;
        selfrect = self.rect;
        print(self.ra)

        attackrect = PY.Rect(0,0,320,320)
        attackrect.center = selfrect.center
        #PY.draw.rect(Globals.SCREEN, PY.Color(0,0,0),attackrect)
        
        if (attackrect.contains(herorect)):
            if (herorect.centery < selfrect.centery):
                print ("ee0")
                self.direction =  0
            elif (herorect.centery > selfrect.centery):
                print ("ee2")
                self.direction =  2
            elif (herorect.centerx < selfrect.centerx):
                print ("ee3")
                self.direction =  3
            elif (herorect.centerx > selfrect.centerx):
                print ("ee1")
                self.direction =  1
            isCollision = False
            print self.direction
            self.move(wallMap)
        else:
           
            if self.moveCounter >= self.moveDuration:  # need new direction
                self.moveCounter = 0  # reset moveCounter
                self.moveDuration = random.randint(
                                                       MIN_MOVE_DURATION,
                                                       MAX_MOVE_DURATION)  # new moveDuration
                    # decides which direction to move in
                self.direction = random.randint(0, 3)
                isCollision = False
            else:  # do not need new direction
                self.moveCounter += 1  # increment moveCounter
            if (self.ra == True):
                print "lolol"
                self.move(wallMap)

        if self.pTimer == PROJECTILE_TIMER:
            # Adds projectile to entity list
            Globals.WORLD.addEntity(self.shoot_projectile
                                    (Globals.STATE.enemyProjectileGroup))
            self.pTimer = 0
        if self.health <= 0:
            self.kill()
    
    def move(self,wallMap):
     
        if self.direction == 0:  # up movement
            self.rect.centery -= 1
            self.update_image(self.image_tracker*4+3)
            # adjust in case results in collision
            self.collide(0, -self.rect.centery, wallMap)
        elif self.direction == 1:  # right movement
            self.rect.centerx += 1
            self.update_image(self.image_tracker*4+2)
            # adjust in case results in collision
            self.collide(self.rect.centerx, 0, wallMap)
        elif self.direction == 2:  # down movement
            self.rect.centery += 1
            self.update_image(self.image_tracker*4)
            # adjust in case results in collision
            self.collide(0, self.rect.centery, wallMap)
        else:  # left movement
            self.rect.centerx -= 1
            self.update_image(self.image_tracker*4+1)
            # adjust in case results in collision
            self.collide(-self.rect.centerx, 0, wallMap)
    
    #  shoot projectiles from enemy
    def shoot_projectile(self, Pgroup):
        proj = Projectile.Projectile(self.rect, self.direction, skull)
        Pgroup.add(proj)
        return proj
    #  check for collisions with other sprites

    def collide(self, xvel, yvel, wallMap):
        FADEOUTTIME = 0.2
        key = PY.key.get_pressed()
        for p in wallMap:
            if PS.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                elif xvel < 0:
                    self.rect.left = p.rect.right
                elif yvel > 0:
                    self.rect.bottom = p.rect.top
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                else:
                    continue
