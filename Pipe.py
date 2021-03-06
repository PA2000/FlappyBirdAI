import pygame
import os
import random
import math

class Pipe:
   #load image
   pipeImg = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
   gap = 200

   def __init__(self, x, score):
      self.x = x
      self.height = 0
      self.top = 0 #top of object, not indiviual pipe
      self.bottom = 0 #bottom of object, not indiviual pipe

      if score < 40:
         self.vel = 4
      elif score < 110:
         self.vel = math.floor(score/10)
      else:
         self.vel = 11  

      #seperate images for top and bottom pipes
      self.topPipe = pygame.transform.flip(self.pipeImg, False, True)
      self.bottomPipe = self.pipeImg
      
      self.passed = False
      self.setHeight()
   
   def setHeight(self):
      self.height = random.randrange(50, 450)
      self.top = self.height - self.topPipe.get_height()
      self.bottom = self.height + self.gap

   def move(self):
      self.x -= self.vel

   def draw(self, win):
      win.blit(self.topPipe, (self.x, self.top))
      win.blit(self.bottomPipe, (self.x, self.bottom))
   
   def collide(self, bird):
      birdMask = bird.getMask()
      topMask = pygame.mask.from_surface(self.topPipe)
      bottomMask = pygame.mask.from_surface(self.bottomPipe)

      topOffset = (round(self.x - bird.x), self.top - round(bird.y))
      bottomOffset = (round(self.x - bird.x), self.bottom - round(bird.y))
      
      bottomPoint = birdMask.overlap(bottomMask, bottomOffset)
      topPoint = birdMask.overlap(topMask, topOffset)
      if topPoint or bottomPoint:
         return True
      return False

   








