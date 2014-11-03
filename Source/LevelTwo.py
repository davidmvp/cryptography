import sys as SYS
import random
import time
import pygame as PG
import os as OS
import pygame.display as PD
import pygame.event as PE
import pygame.font as PF
import pygame.time as PT
import pygame.sprite as PS
import pygame.color as PC
import pygame.mixer as PX
import pygame.image as PI
import DialogueBox as DB
import Player
import Enemy
import Setup
import smooth
import LoseScreen
import item
import NPC
from Screen import BaseState as State
from Screen import Globals
import Score as Score
Dir = OS.getcwd()

RUNNING = True
SCREEN = None
WIDTH = None
HEIGHT = None
TILES = {}
WORLD = None
CAMERA = None
LOSE_TIME = 1000


class LevelTwo(State):
    FADEINTIME = 1.0
    FADEOUTTIME = 0.2
    CYCLE = 1.0
    detection = False

    def __init__(self):
        State.__init__(self)
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map2.txt")
        print smooth.wallMap
        print smooth.entities
        self.time = 0.0
        self.alpha = 255
        Globals.WORLD.camera = smooth.Camera \
            (smooth.complex_camera, \
             Globals.WORLD, \
             Globals.WORLD.realwidth, Globals.WORLD.realheight)
        # Declare sprite groups
        self.enemyGroup = PS.Group()  # enemy sprite group
        self.enemyProjectileGroup = PS.Group()  # projectile sprite group
        self.heroGroup = PS.Group()  # hero sprite group
        self.heroProjectileGroup = PS.Group()  # projectile sprite group
        self.heroSword = PS.Group() #sword sprite group
        self.items = PS.Group()  # items to be picked up
        self.npcGroup = PS.Group() #non-player character group
        # Done declaring sprite groups
        self.events = [True, True, True, True]
        # create firewood item
        #self.firewood = item.Item(PG.Rect(100, 100, 32, 32), firewood_image)
        #self.items.add(self.firewood)
        #Globals.WORLD.addEntity(self.items)
        enemy = Enemy.Enemy(400,400,True)
        self.enemyGroup.add(enemy)
        Globals.WORLD.addEntity(enemy)
        for i in range(20):
           
            enemy = Enemy.Enemy(random.randint(0,  Globals.WORLD.realwidth),random.randint(0, Globals.WORLD.realheight),True)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
       # for i in range(Setup.NUM_VILLAINS):
       #     enemy = Enemy.Enemy()
       #     self.enemyGroup.add(enemy)
       #     Globals.WORLD.addEntity(enemy)
       # for i in range(Setup.NUM_VILLAINS):
       #     npc = NPC.NPC()
       #     self.npcGroup.add(npc)
       #     Globals.WORLD.addEntity(npc)
        self.heroGroup = PS.Group()
        self.hero = Player.Player()
        self.hero.rect.center = (32, 26*32)
        self.heroGroup.add(self.hero)
        Globals.WORLD.addEntity(self.hero)
        self.startTime = time.time()
        self.lastTime = 0
        self.surf2 = PG.Surface((800, 600))
        self.surf = Globals.FONT.render(str(LOSE_TIME), True, (0, 0, 0))
        self.score = 50
        self.firstTime = True
    def render(self):
        self.walls = PS.Group()

    def update(self, newTime):
        self.surf2.fill((0, 0, 0))
        self.surf2.set_alpha(self.alpha)
        if self.alpha > 0:
            self.alpha -= 5
        self.time = self.time + newTime

        self.currTime = time.time()  # Current time
        self.elapsedTime = int(self.currTime - self.startTime)  # elapsed time
        self.score = LOSE_TIME - self.elapsedTime
        if not self.elapsedTime == self.lastTime:
            self.surf = Globals.FONT.render(str(self.score), True, (0, 0, 0))
        self.lastTime = self.elapsedTime
        if self.elapsedTime > LOSE_TIME:
            Globals.SCREEN.fill(Setup.BLACK)
            Globals.STATE = LoseScreen.LoseScreen(self.score)
        if self.time > self.CYCLE:
            self.time = 0.0
        if self.time < 0.33:
            image_counter = 0
        elif self.time < 0.66:
            image_counter = 1
        else:
            image_counter = 2
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.hero)
        # self.group.draw(Globals.SCREEN)
        Globals.SCREEN.blit(self.surf, (500, 100))  # Drawing clock
        Globals.SCREEN.blit(self.surf2, (0,0))
        playerX = self.hero.rect.centerx
        playerY = self.hero.rect.centery
        key = PG.key.get_pressed()
        for event in PE.get():
            if event.type == PG.QUIT:
                Globals.RUNNING = False
        if key[PG.K_ESCAPE]:
            Globals.RUNNING = False
        elif key[PG.K_w]:
            self.hero.speed = 8.0
        elif not key[PG.K_w]:
            self.hero.speed = 3.0
        if key[PG.K_r]:
            Globals.WORLD.addEntity(self.hero.shoot_projectile
                                    (Globals.STATE.heroProjectileGroup))
        if key[PG.K_e]:
            Globals.WORLD.addEntity(self.hero.sword_attack
                                    (Globals.STATE.heroSword))
        elif key[PG.K_SPACE]:
            pass 
        if key[PG.K_DOWN] and not key[PG.K_LEFT] \
                and not key[PG.K_RIGHT] and not key[PG.K_UP]:
            self.hero.movedown(image_counter, self.walls)
        elif key[PG.K_LEFT] and not key[PG.K_RIGHT] \
                and not key[PG.K_UP] and not key[PG.K_DOWN]:
            self.hero.moveleft(image_counter, self.walls)
        elif key[PG.K_RIGHT] and not key[PG.K_UP] \
                and not key[PG.K_LEFT] and not key[PG.K_DOWN]:
            self.hero.moveright(image_counter, self.walls)
        elif key[PG.K_UP] and not key[PG.K_RIGHT] \
                and not key[PG.K_LEFT] and not key[PG.K_DOWN]:
            self.hero.moveup(image_counter, self.walls)
        else:
            self.hero.moveidle(image_counter)
        playerX = self.hero.rect.centerx
        playerY = self.hero.rect.centery
        self.heroGroup.update(self.enemyGroup, smooth.wallMap
                              [playerX/(Setup.GRID_SIZE *
                                        Setup.PIXEL_SIZE),
                               playerY/(Setup.GRID_SIZE *
                                        Setup.PIXEL_SIZE)],
                              self)
        self.enemyGroup.update(smooth.wallMap
                               [playerX/(Setup.GRID_SIZE * Setup.PIXEL_SIZE),
                                playerY/(Setup.GRID_SIZE * Setup.PIXEL_SIZE)],self.hero)
        self.npcGroup.update(smooth.wallMap
                               [playerX/(Setup.GRID_SIZE * Setup.PIXEL_SIZE),
                                playerY/(Setup.GRID_SIZE * Setup.PIXEL_SIZE)])
        self.enemyProjectileGroup.update(self.hero)
        for enemy in self.enemyGroup:
            self.heroProjectileGroup.update(enemy)
            self.heroSword.update(self.hero, enemy)

    def currentScore(self):
        return self.score

