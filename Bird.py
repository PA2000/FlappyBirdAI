import pygame
import os

class Bird:
   #load image
   imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
   maxRotation = 25
   rotVel = 20
   animationTime = 5

   def __init__(self, x , y):
      self.x = x
      self.y = y
      self.tilt = 0
      self.tickCount = 0
      self.vel = 0
      self.height = y
      self.imgCount = 0
      self.img = self.imgs[0]
   
   def jump(self):
      self.vel = -10.5
      self.tickCount = 0
      self.height = self.y

   #parabolic movement
   def move(self):
      self.tickCount += 1
      #displacement = velocity(time) + 1.5(acceleration)(time)^2
      d = (self.vel * self.tickCount) + (1.5 * self.tickCount ** 2)
      #terminal velocity; if bird is going down by more than 16, just go down by 16 (stop acceleration)
      if d >= 16:
         d = 16
      #fine tune upwards distance
      if d < 0:
         d -= 2
      self.y = self.y + d
      #if bird is going up, or is above original height
      if d < 0 or self.y < self.height + 50:
         if self.tilt < self.maxRotation:
               self.tilt = self.maxRotation
      else:
         if self.tilt > -90:
            #"nosedive" downwards
            self.tilt -= self.rotVel
   
   def draw(self, win):
      self.imgCount += 1
      #loop through the three images to create illusion of animation
      if self.imgCount <= self.animationTime:
         self.img = self.imgs[0]
      elif self.imgCount <= self.animationTime * 2:
         self.img = self.imgs[1]
      elif self.imgCount <= self.animationTime * 3:
         self.img = self.imgs[2]
      elif self.imgCount <= self.animationTime * 4:
         self.img = self.imgs[1]
      elif self.imgCount == self.animationTime * 4 + 1:
         self.img = self.imgs[0]
         self.imgCount = 0
      #when bird is nosediving, don't make it flap
      if self.tilt <= -80:
         self.img = self.imgs[1]
         self.imgCount = self.animationTime*2
      #tilt the bird
      rotated_image = pygame.transform.rotate(self.img, self.tilt)
      new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
      win.blit(rotated_image, new_rect.topleft)

   def getMask(self):
      return pygame.mask.from_surface(self.img)

