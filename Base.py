import pygame
import os
import random

class Base:
   baseImg = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
   vel = 5
   width = baseImg.get_width()
   img = baseImg

   def __init__(self, y):
      self.y = y
      #starting points of the base imgs
      self.x1 = 0
      self.x2 = self.width
   
   def move(self):
      self.x1 -= self.vel
      self.x2 -= self.vel

      #if base imgs are off the screen(went to the left); cycle images
      if self.x1 + self.width < 0:
         self.x1 = self.x2 + self.width
      if self.x2 + self.width < 0:
         self.x2 = self.x1 + self.width

   def draw(self, win):
      win.blit(self.img, (self.x1, self.y))
      win.blit(self.img, (self.x2, self.y))