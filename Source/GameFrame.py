import Setup
import sys as SYS
import pygame as PG
import pygame.mouse as PM
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
import Player
import Enemy
import Title as Title
from Screen import BaseState as State
from Screen import Globals
import smooth
INTERVAL = .01


def main():
    initialize()
    loop()
    finalize()


def initialize():
    passed, failed = PG.init()
    print passed
    Globals.SCREEN = PDI.set_mode((800, 600), PG.DOUBLEBUF | PG.HWSURFACE)
    Globals.WIDTH = Globals.SCREEN.get_width()
    Globals.HEIGHT = Globals.SCREEN.get_height()
    Globals.FONT = PF.Font(None, 48)
    Globals.STATE = Title.Title_Screen()


def loop():
    clock = PT.Clock()
    leftover = 0.0
    updates = 0
    while Globals.RUNNING:
        start_time = PT.get_ticks()
        Globals.STATE.render()
        PDI.flip()
        updates = 0
        clock.tick(60)
        last = PT.get_ticks()
        elapsed = (last - start_time) / 1000.0
        Globals.STATE.update(elapsed)
        leftover += elapsed
        while leftover > INTERVAL:
            Globals.STATE.render()
            leftover -= INTERVAL
            updates += 1
            for event in PE.get():
                if event.type == PG.QUIT:
                    Globals.RUNNING = False
                else:
                    Globals.STATE.event(event)

def finalize():
   print 1
   PDI.quit()
   print 2
   PX.quit()
   print 3
   PG.quit()
   print 4
   SYS.exit()
   print 5

if __name__ == "__main__":
    main()
