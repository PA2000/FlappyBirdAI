import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
pygame.font.init()
import neat
import time
import random
import pickle
from Bird import Bird
from Pipe import Pipe
from Base import Base

#set window parameters
winWidth = 500
windHeight = 800
#load background
bgImg = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
#font for score
font = pygame.font.SysFont('agencyfb', 70)


def drawWindow(win, bird, pipes, base, score):
   win.blit(bgImg, (0, 0))
   bird.draw(win)
   for pipe in pipes:
      pipe.draw(win)
   base.draw(win)
   text = font.render("Score: " + str(score), 1, (255, 0, 0))
   win.blit(text, (winWidth/2 - text.get_width()/2, 10))
   pygame.display.update()

def game(neural_net):
   run = True
   #while run:
   bird = Bird(230, 350)
   base = Base(700)
   score = 0
   pipes = [Pipe(730, score)]
   win = pygame.display.set_mode((winWidth, windHeight))
   pygame.display.set_caption("Padmank's Flappy Bird Test")
   clock = pygame.time.Clock()

   alive, paused = True, False
   while alive:
      clock.tick(60)
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run, alive = False, False
            pygame.quit()
            quit()
            break
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               run, alive = False, False
               pygame.quit()
               quit()
               break
      
      if not paused:
         pipeIndex = 0
         if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].topPipe.get_width():
            pipeIndex = 1

         bird.move()
         distToTop = abs(bird.y - pipes[pipeIndex].height)
         distToBottom = abs(bird.y - pipes[pipeIndex].bottom)
         #RETURNS: List of output neurons; INPUT: Input nodes
         output = neural_net.activate((bird.y, distToTop, distToBottom)) 
         #our NN only has one output, hence output[0]
         if output[0] > 0.5:
            bird.jump()

         addPipe = False
         removePipes = []
         for pipe in pipes:
            if pipe.collide(bird):
               paused = True
            if pipe.x + pipe.topPipe.get_width() < 0: #if pipe is off the screen completely
               removePipes.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
               pipe.passed = True
               addPipe = True
            pipe.move()
         if addPipe:
            score += 1
            pipes.append(Pipe(600, score))
         for r in removePipes:
            pipes.remove(r)

         if bird.y + bird.img.get_height() >= 730:
            paused = True

         base.move()
         drawWindow(win, bird, pipes, base, score)  

def main():
   neural_net = pickle.load(open("winner.pickle", "rb"))
   print(neural_net)
   game(neural_net)

if __name__ == "__main__":
    main()