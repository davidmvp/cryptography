import os as OS
import sys as SYS
import pygame as PY
import pygame.display as PD
import pygame.event as PE
import pygame.image as PI
import pygame.sprite as PS
import Setup
from Character import BaseClass
from smooth import Entity
Dir = OS.getcwd()
PROJECTILE_SPEED = 1
MAX_DISTANCE = 200


class Sword(Entity):
    # startRect is the Rect of the sprite that generates the projectile
    # direction is an int that specifies which direction projectile moves
    # 0: up, 1: right, 2: down, 3: left
    def __init__(self, startRect, direction, imagePath):
        IMAGES = None
        Entity.__init__(self)
        if not IMAGES:
            self.load_images(imagePath)
        self.image = self.IMAGES
        self.direction = direction
        self.distance = 0
        self.rect = self.image.get_rect()
    # Starting position of projectile equals starting position of
        self.rect.centerx = startRect.centerx
        self.rect.centery = startRect.centery
    
    def load_images(self, imagePath):
        picture = PI.load(imagePath).convert_alpha()
        self.IMAGES = PY.transform.scale(picture, (32, 32))
    # targetRect is the sprite of the target of the projectile
    # Returns 1 if the projectile hit its target
    # Returns 0 if the projectile has not reached its max range
    # Returns -1 if the projectile has passed its max range
    def update(self, heroSprite, targetSprite):

        # If reached max range
        if self.distance >= MAX_DISTANCE:
            self.kill()

        # If collided
        if PS.collide_rect(self, targetSprite):
            # Removes this sprite from all groups.
            # Should delete from screen
            self.kill()
            targetSprite.health -= 10

        # Move the projectile
        if self.direction == 0 or self.direction == "moveup":  # up
            self.rect.centery = heroSprite.rect.centery - 16
        elif self.direction == 1 or self.direction == "moveright":  # right
            self.rect.centerx = heroSprite.rect.centerx + 16
        elif self.direction == 2 or self.direction == "movedown":  # down
            self.rect.centery = heroSprite.rect.centery + 16
        elif self.direction == 3 or self.direction == "moveleft": #  left
            self.rect.centerx = heroSprite.rect.centerx - 16
       
        self.distance += 1 








