import sys as SYS
import time
import pygame as PG
import os as OS
import pygame.display as PDI
import pygame.draw as PD
import pygame.event as PE
import pygame.font as PF
import pygame.time as PT
import pygame.sprite as PS
import pygame.color as PC
import pygame.mixer as PX
import pygame.image as PI
import DialogueBox as DB
from Screen import BaseState as State
from Screen import Globals
import GameScreen as GS
import Player
import smooth
Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir),
                          'Images/brick_wall_tiled_perfect.png')
sound_path = OS.path.join(OS.path.dirname(Dir),
                          'Sounds/screen_start.wav')


class Cutscene(State):
    def __init__(self):
        State.__init__(self)
        smooth.loadtiles()
        Globals.WORLD = smooth.World("map.txt")
        Globals.WORLD.camera = smooth.Camera(smooth.complex_camera,
                                             Globals.WORLD,
                                             Globals.WORLD.realwidth,
                                             Globals.WORLD.realheight)
        self.npc1 = Player.Player()
        self.npc2 = Player.Player()
        self.npc1.image = self.npc1.IMAGES[0]
        self.npc2.image = self.npc2.IMAGES[0]
        self.npc1.rect.center = (451, 752)
        self.npc2.rect.center = (451, 752)
        self.Timer = 0

    def update(self, time):
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.npc1)
        if self.Timer == 0:
            Globals.WORLD.addEntity(self.npc1)
        while self.Timer < 150:
            key = PG.event.get(PG.KEYDOWN)
            for event in key:
                if event.type == PG.KEYDOWN:
                    self.Timer = 181
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.npc1)
            set_timer = self.Timer % 10
            if set_timer == 0:
                self.npc1.rect.centery += 4
                self.npc1.update_image(self.npc1.image_tracker*4,
                                       self.npc1.change_direction)
            self.Timer += 1
            PDI.flip()
        if self.Timer == 175:
            self.npc1.update_image(self.npc1.image_tracker*4+3, True)
            Globals.WORLD.addEntity(self.npc2)
        if self.Timer == 176:
            Dialogue = DB.Dialogue_box('cutscene1_dialogue.txt')
            while Dialogue.isOpen:
                Dialogue.update()
        self.Timer += 1
        if self.Timer == 183:
            Globals.WORLD.addEntity(self.npc2)
            self.npc1.rect.centery += 60
            self.npc1.update_image(self.npc1.image_tracker*4+3, True)
            self.endScene()

    def endScene(self):
        fpsClock = PT.Clock()
        DURATION = 2000.0
        start_time = PT.get_ticks()
        ratio = 0.0
        while ratio < 1.0:
            current_time = PT.get_ticks()
            ratio = (current_time - start_time)/DURATION
            if ratio > 1.0:
                ratio = 1.0
            value = int(255*ratio)
            fade_color = PC.Color(0, 0, 0, 0)
            fade_color.a = value
            # PD.rect(Globals.SCREEN, fade_color, (0,0,400,300))
            # print 'hi'
            surf = PG.Surface((800, 600))
            surf.set_alpha(value)
            surf.fill((0, 0, 0))
            Globals.SCREEN.blit(surf, (0, 0))
            PDI.flip()
            fpsClock.tick(60)
        Globals.STATE = GS.GameScreen()
