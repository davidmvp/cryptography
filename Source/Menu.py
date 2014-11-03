import os as OS
import Setup
import sys as SYS
import pygame as PG
import pygame.mouse as PM
import pygame.draw as PD
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
import pygame.font as PF
import pygame.key as PK
import Player
import Enemy
import Setup
from Screen import BaseState as State
from Screen import Globals
import GameScreen as GS
import Score as Score
import string
import cutscene1
Dir = OS.getcwd()
sound_path = OS.path.join(OS.path.dirname(Dir), 'Sounds/screen_start.wav')
image_path = OS.path.join(OS.path.dirname(Dir), 'Images/menu_screen.jpg')


class Menu(State):
    FADEINTIME = 1.0
    FADEOUTTIME = 0.2
    NEW_GAME = None
    VOLUME = None
    BRIGHTNESS = None
    HIGH_SCORE = None
    EXIT = None

    def __init__(self):
        State.__init__(self)
        self.color = PC.Color("black")
        self.time = 0.0
        Globals.FONT = PF.SysFont("monospace", 15)
        PX.music.load(sound_path)
        PX.music.play(-1)
        Globals.SCREEN.fill(PC.Color("black"))
        self.new_game = []
        self.exit = []
        self.score = []
        self.brightness = []
        self.volume = []
        self.hover = [False, False, False, False, False]

    def render(self):
        surf = Globals.FONT.render("Menu", True, self.color)
        self.width, height = surf.get_size()
        sheet = PI.load(image_path).convert()
        Globals.SCREEN.blit(sheet, (0, 0))
        Globals.SCREEN.blit(surf, (0 + self.width/2, 0 + height/2))
        if not self.hover[0]:
            self.NEW_GAME = Globals.FONT.render("New Game", True, self.color)
        else:
            self.NEW_GAME = Globals.FONT.render("New Game",
                                                True, PC.Color("black"),
                                                PC.Color("white"))
        Globals.SCREEN.blit(
            self.NEW_GAME,
            (self.width/2, Globals.HEIGHT/2+100))
        self.rect_new_game = self.NEW_GAME.get_rect(topleft=(self.
                                                    NEW_GAME.get_width()/2,
                                                    Globals.HEIGHT/2 + 100))
        self.new_game = [self.rect_new_game.left,
                         self.rect_new_game.right,
                         self.rect_new_game.top,
                         self.rect_new_game.bottom]
        if not self.hover[1]:
            self.VOLUME = Globals.FONT.render("Adjust Volume",
                                              True, self.color)
        else:
            self.VOLUME = Globals.FONT.render("Adjust Volume",
                                              True, PC.Color("black"),
                                              PC.Color("white"))
        Globals.SCREEN.blit(
            self.VOLUME,
            (self.width/2, Globals.HEIGHT/2+125))
        self.volume_rect = self.VOLUME.get_rect(topleft=(
                                                self.width/2,
                                                Globals.HEIGHT/2 + 125))
        self.volume = [self.volume_rect.left,
                       self.volume_rect.right,
                       self.volume_rect.top,
                       self.volume_rect.bottom]
        if not self.hover[2]:
            self.BRIGHTNESS = Globals.FONT.render(
                "Adjust Brightness",
                True,
                self.color)
        else:
            self.BRIGHTNESS = Globals.FONT.render("Adjust Brightness",
                                                  True, PC.Color("black"),
                                                  PC.Color("white"))
        Globals.SCREEN.blit(
            self.BRIGHTNESS,
            (self.width/2, Globals.HEIGHT/2+150))
        self.brightness_rect = self.BRIGHTNESS.get_rect(topleft=(self.width/2, Globals.
                                                                 HEIGHT/2 +
                                                                 150))
        self.brightness = [self.brightness_rect.left,
                           self.brightness_rect.right,
                           self.brightness_rect.top,
                           self.brightness_rect.bottom]

        if not self.hover[3]:
            self.HIGH_SCORE = Globals.FONT.render("High Score",
                                                  True, self.color)
        else:
            self.HIGH_SCORE = Globals.FONT.render("High Score",
                                                  True, PC.Color("black"),
                                                  PC.Color("white"))
        Globals.SCREEN.blit(
            self.HIGH_SCORE,
            (self.width/2, Globals.HEIGHT/2+175))
        self.score_rect = self.HIGH_SCORE.get_rect(topleft=(self.width/2,
                                                            Globals.HEIGHT/2 +
                                                            175))
        self.score = [self.score_rect.left,
                      self.score_rect.right,
                      self.score_rect.top,
                      self.score_rect.bottom]

        if not self.hover[4]:
            self.EXIT = Globals.FONT.render("Exit", True, self.color)
        else:
            self.EXIT = Globals.FONT.render("Exit",
                                            True, PC.Color("black"),
                                            PC.Color("white"))
        Globals.SCREEN.blit(
            self.EXIT,
            (self.width/2, Globals.HEIGHT/2+200))
        self.exit_rect = self.EXIT.get_rect(topleft=(self.width/2,
                                                     Globals.HEIGHT/2 + 200))
        self.exit = [self.exit_rect.left,
                     self.exit_rect.right,
                     self.exit_rect.top,
                     self.exit_rect.bottom]

    def update(self, time):
        self.time += time
        if self.time < Menu.FADEINTIME:
            ratio = self.time / Menu.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)
        position = PM.get_pos()
        if self.inrange(self.new_game, position):
            self.hover[0] = True
        else:
            self.hover[0] = False

        if self.inrange(self.volume, position):
            self.hover[1] = True
        else:
            self.hover[1] = False

        if self.inrange(self.brightness, position):
            self.hover[2] = True
        else:
            self.hover[2] = False

        if self.inrange(self.score, position):
            self.hover[3] = True
        else:
            self.hover[3] = False

        if self.inrange(self.exit, position):
            self.hover[4] = True
        else:
            self.hover[4] = False

    def inrange(self, ranges, position):
        if (position[0] <= ranges[1]and position[0] >= ranges[0])and (position[1] <= ranges[3] and position[1] >= ranges[2]):
            return True
        else:
            return False

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == PG.MOUSEBUTTONDOWN:
            position = PM.get_pos()
            if self.rect_new_game.collidepoint(position):
                Globals.SCREEN.fill(PC.Color("black"))
                Globals.CURRENT_PLAYER[0] = self.ask(Globals.SCREEN, "Name")
                if Globals.CURRENT_PLAYER != 0:
                    print Globals.CURRENT_PLAYER
                    Globals.STATE = cutscene1.Cutscene()
                    # Globals.STATE = GS.GameScreen()
            if self.score_rect.collidepoint(position):
                Globals.STATE = Score.Score_Screen()
            if self.exit_rect.collidepoint(position):
                Globals.RUNNING = False

    def display_box(self, screen, message):
        screen.fill(PC.Color("black"))
        fontobject = Globals.FONT
        PD.rect(screen, (0, 0, 0), ((screen.get_width()/2) - 100, (screen.get_height()/2) - 12, 204, 24), 1)
        PD.rect(screen, (255, 255, 255), ((screen.get_width()/2) - 102, (screen.get_height()/2) - 12, 204, 24), 1)
        if len(message) != 0:
                screen.blit(fontobject.render(message, 1, (255, 255, 255)), ((screen.get_width()/2) - 100, (screen.get_height()/2) - 10))
        PDI.flip()

    def ask(self, screen, question):
        current_string = []
        self.display_box(screen, question + ": " + string.join(current_string, ""))
        while 1:
            inkey = self.get_key()
            Mod = self.get_mod()
            if inkey == 27:
                return 0
            elif inkey == PG.K_BACKSPACE:
                current_string = current_string[0: len(current_string) - 1]
            elif inkey == PG.K_RETURN:
                break
            elif inkey == PG.K_MINUS:
                current_string.append("_")
            elif Mod:
                if inkey <= 127:
                    temp_string = []
                    temp_string.append(chr(inkey))
                    temp_string = [x.upper() for x in temp_string]
                    current_string.append("".join(temp_string))
            elif inkey <= 127:
                current_string.append(chr(inkey))
            self.display_box(screen, question + ": " + string.join(current_string, ""))
        return string.join(current_string, "")

    def get_key(self):
        while 1:
            event = PE.poll()
            if event.type == PG.KEYDOWN:
                return event.key
            else:
                pass

    def get_mod(self):
        key = PK.get_pressed()
        if key[PG.K_LSHIFT] or key[PG.K_RSHIFT]:
            return True
        else:
            return False
