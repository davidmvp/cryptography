import os as OS
import sys as SYS
import pygame as PY
import pygame.display as PD
import pygame.image as PI
import pygame.event as PE
import pygame.sprite as PS
import pygame.time as PT
import pygame.mixer as PX
import DialogueBox as DB
import Functions
import Setup
import Character
import Score
import GameScreen
import WinScreen
import LoseScreen
import Projectile
import Sword
from Character import BaseClass
from smooth import wallMap
from smooth import Grass
from smooth import Sand
from smooth import Grey_brick
from smooth import TriggerBlockSand
from smooth import Entity
from Screen import Globals
import LevelTwo
Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir),
                          'Images/WarriorSpriteSheet.png')
fireball = OS.path.join(OS.path.dirname(Dir), 'Images/Fireball.png')
sword = OS.path.join(OS.path.dirname(Dir), 'Images/sword.png')
SOUND_PATH = OS.path.join(OS.path.dirname(Dir), 'Sounds/playerCollision.wav')
MAX_SPEED = 5.0
DECELERATION_RATE = 0.5
FADEOUTTIME = 0.2
MAX_HEALTH = 100.0
TIME_UPDATE = 5


class Player(Entity):
    def __init__(self):
        IMAGES = None
        Entity.__init__(self)
        if not IMAGES:
            self.load_images()
        self.image_timer = 0
        self.image_tracker = 0
        self.image = Player.IMAGES[2]
        self.area = PY.Rect(0, 0, Globals.WORLD.realwidth,
                            Globals.WORLD.realheight)
        self.image_rect = self.image.get_rect()
        self.rect = PY.Rect(0,0, 32, 32)
        self.rect.midbottom = self.image_rect.midbottom
        self.rect.centery = self.rect.centery
        self.speed = 3.0
        self.direction = "still"
        self.change_direction = False
        self.movepos = [0.0, 0.0]
        self.time = 0.0
        self.moving = False
        self.walls = None
        self.newpos = [0.0, 0.0]
        self.action_rect = PY.Rect(0, 0, 64, 32)
        self.health = MAX_HEALTH
        self.firewood = 0
        self.elderCount = 0  # number of times spoken to elder

    def update(self, enemyGroup, spriteGroup, thisGameScreen, item = None):
        PY.mixer.music.load(SOUND_PATH)
        self.dirty = 1
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            if not self.movepos[0] == 0:
                self.rect.left += self.movepos[0]
                self.image_rect.left += self.movepos[0]

            if not self.movepos[1] == 0:
                self.rect.bottom += self.movepos[1]
                self.image_rect.bottom += self.movepos[1]
        # if Functions.isCollision(self.rect):
        #    PY.mixer.music.play()
        self.collide(self.movepos[0], 0, spriteGroup, thisGameScreen, item)
        self.collide(0, self.movepos[1], spriteGroup, thisGameScreen, item)
        # Draw healthbar
        self.healthBarBack = PY.Rect(self.rect.centerx
                                     - 20, self.rect.centery - 40, 40, 8)
        self.healthBarFront = PY.Rect(self.rect.centerx - 20,
                                      self.rect.centery
                                      - 40, 40*(self.health/MAX_HEALTH), 8)
        self.healthBarBack = Globals.WORLD.camera.apply(self.healthBarBack)
        self.healthBarFront = Globals.WORLD.camera.apply(self.healthBarFront)
        PY.draw.rect(Globals.SCREEN, (255, 0, 0), self.healthBarBack)
        PY.draw.rect(Globals.SCREEN, (0, 255, 0), self.healthBarFront)
        self.enemyCollide(enemyGroup, thisGameScreen)
        self.eventCollide(Globals.WORLD.get_entities(), thisGameScreen)

    def load_images(self):
        Player.IMAGES = []
        sheet = PI.load(image_path).convert_alpha()
        key = (255,255,255)
        for i in range(3):
            for j in range(4):
                surface = PY.Surface((64, 64)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*64, j*64, 64, 64))
                Player.IMAGES.append(surface)

    def update_image(self, image_num, change_direction):
        if self.image_timer > TIME_UPDATE or change_direction:
            self.image = Player.IMAGES[image_num]
            self.image.convert_alpha()
            self.image_tracker = (self.image_tracker+1) % 3
            self.image_timer = 0
            self.change_direction = False
        else:
            self.image_timer += 1
        # self.rect = self.image.get_rect()
        # Player.rect.center = (Setup.WIDTH/2, Setup.HEIGHT/2)  DO WE USE THIS?

    def movedown(self, image_counter, walls):
        wall_list = PS.spritecollide(self, walls, False)
        if self.direction != 'movedown':  # we just changed directions
            self.movepos = [0.0, 0.0]  # remove deceleration
            self.image_tracker = 0
            self.change_direction = True
        else:
            self.movepos[1] = self.speed
            
        self.direction = "movedown"
        self.update_image(self.image_tracker*4, self.change_direction)
        self.moving = True
        self.action_rect.width = 64
        self.action_rect.height = 32
        self.action_rect.midtop = self.rect.midbottom
        #self.action_rect = Globals.WORLD.camera.apply(self.action_rect)

    def moveleft(self, image_counter, walls):
        wall_list = PS.spritecollide(self, walls, False)
        if self.direction != 'moveleft':
            self.movepos = [0.0, 0.0]  # remove deceleration
            self.image_tracker = 0
            self.change_direction = True
        else:
            self.movepos[0] = -self.speed
        self.direction = "moveleft"
        self.update_image(self.image_tracker*4+2, self.change_direction)
        self.moving = True
        self.action_rect.width = 32
        self.action_rect.height = 64
        self.action_rect.midright = self.rect.midleft
        #self.action_rect = Globals.WORLD.camera.apply(self.action_rect)

    def moveright(self, image_counter, walls):
        wall_list = PS.spritecollide(self, walls, False)
        if self.direction != 'moveright':
            self.movepos = [0.0, 0.0]  # remove deceleration
            self.image_tracker = 0
            self.change_direction = True
        else:
            self.movepos[0] = self.speed
        self.direction = "moveright"
        self.update_image(self.image_tracker*4+3, self.change_direction)
        self.moving = True
        self.action_rect.width = 32
        self.action_rect.height = 64
        self.action_rect.midleft = self.rect.midright
        #self.action_rect = Globals.WORLD.camera.apply(self.action_rect)

    def moveup(self, image_counter, walls):
        wall_list = PS.spritecollide(self, walls, False)
        if self.direction != 'moveup':  # we just changed directions
            self.movepos = [0.0, 0.0]  # remove deceleration
            self.image_tracker = 0
            self.change_direction = True
        else:
            self.movepos[1] = -self.speed
        self.direction = "moveup"
        self.update_image(self.image_tracker*4+1, self.change_direction)
        self.moving = True
        self.action_rect.width = 64
        self.action_rect.height = 32
        self.action_rect.midbottom = self.rect.midtop
        #self.action_rect = Globals.WORLD.camera.apply(self.action_rect)

    def moveidle(self, image_counter):

        # Implementing deceleration
        if self.movepos != [0, 0]:
            if self.movepos[0] > 0:
                self.movepos[0] -= DECELERATION_RATE
                if self.movepos[0] < 0:
                    self.movepos[0] = 0
            else:  # self.movepos[0] < 0
                self.movepos[0] += DECELERATION_RATE
                if self.movepos[0] > 0:
                    self.movepos[0] = 0

            if self.movepos[1] > 0:
                self.movepos[1] -= DECELERATION_RATE
                if self.movepos[1] < 0:
                    self.movepos[1] = 0
            else:  # self.movepos[1] < 0
                self.movepos[1] += DECELERATION_RATE
                if self.movepos[1] > 0:
                    self.movepos[1] = 0
        # Done with deceleration

        # Makes sure that correct sprite is showing due to direction
        if self.direction == 'moveleft':
            if self.movepos[0] < 0:
                self.update_image(self.image_tracker*4+2, False)
            else:
                self.image = Player.IMAGES[6]
            self.action_rect.midright = self.rect.midleft

        elif self.direction == 'moveup':
            if self.movepos[1] < 0:
                self.update_image(self.image_tracker*4+1, False)
            else:
                self.image = Player.IMAGES[5]
            self.action_rect.midbottom = self.rect.midtop


        elif self.direction == 'movedown':
            if self.movepos[1] > 0:
                self.update_image(self.image_tracker*4, False)
            else:
                self.image = Player.IMAGES[4]
            self.action_rect.midtop = self.rect.midbottom
            
        else:
            if self.movepos[0] > 0:
                self.update_image(self.image_tracker*4+3, False)
            else:
                self.image = Player.IMAGES[7]
            self.action_rect.midleft = self.rect.midright
           
        # self.direction = 'moveidle'
        self.moving = False

    def collide(self, xvel, yvel, spriteGroup, thisGameScreen, item):
        FADEOUTTIME = 0.2
        key = PY.key.get_pressed()
        for p in spriteGroup:
            if PS.collide_rect(self, p):
                print 'hi'
                print 1
                if isinstance(p, Grey_brick) and item != None and item.isPickedUp:
                    spriteGroup.remove(p)
                #elif isinstance(p, ExitBlock):
                #    Globals.STATE = WinScreen.WinScreen(100)
                elif xvel > 0:
                    self.rect.right = p.rect.left
                elif xvel < 0:
                    self.rect.left = p.rect.right
                elif yvel > 0:
                    self.rect.bottom = p.rect.top
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                else:
                    continue

    # collision detection between hero and enemies
    def enemyCollide(self, enemyGroup, thisGameScreen):
        key = PY.key.get_pressed()
        for enemy in enemyGroup:
            if PS.collide_rect(self, enemy):
                self.health -= 1
                if self.health == 0:
                    Globals.STATE = LoseScreen.LoseScreen(0)
    
    def eventCollide(self, spriteGroup, thisGameScreen):
        for p in spriteGroup:
            if PS.collide_rect(self, p):
                if isinstance(p, TriggerBlockSand) and p.event == 1 \
                        and Globals.STATE.events[1]:
                    dialogue = DB.Dialogue_box("cutscene2_dialogue.txt")
                    while dialogue.isOpen:
                        dialogue.update()
                    Globals.STATE.events[1] = False
                elif isinstance(p, TriggerBlockSand) and p.event == 2 \
                        and not Globals.STATE.events[1] \
                        and Globals.STATE.events[2] \
                        and self.elderCount == 0:
                    dialogue = DB.Dialogue_box("cutscene3_dialogue.txt")
                    while dialogue.isOpen:
                        dialogue.update()
                    self.elderCount = 1
                elif isinstance(p, TriggerBlockSand) and p.event == 2 \
                        and not Globals.STATE.events[1] \
                        and Globals.STATE.events[2] \
                        and self.elderCount == 1 \
                        and self.firewood >= 3:
                    dialogue = DB.Dialogue_box("cutscene4_dialogue.txt")
                    while dialogue.isOpen:
                        dialogue.update()
                    Globals.STATE.events[2] = False
                elif isinstance(p, TriggerBlockSand) and p.event == 3 \
                        and not Globals.STATE.events[2] \
                        and Globals.STATE.events[3]:
                    Globals.STATE.events[3] = False

            else:
                pass
    
    #  shoot projectiles from enemy
    def shoot_projectile(self, Pgroup):
        proj = Projectile.Projectile(self.rect, self.direction, fireball)
        Pgroup.add(proj)
        return proj

    def sword_attack(self, Pgroup):
        proj = Sword.Sword(self.rect, self.direction, sword)
        Pgroup.add(proj)
        return proj
