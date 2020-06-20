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

#GLOBAL: Generation number
gen = 0;
bestOfEachGen = []
#set window parameters
winWidth = 500
windHeight = 800
#load background
bgImg = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
#font for score
font = pygame.font.SysFont('agencyfb', 50)

def drawWindow(win, birds, pipes, base, score, gen, numAlive):
   win.blit(bgImg, (0, 0))
   for pipe in pipes:
      pipe.draw(win)
   for bird in birds:
      bird.draw(win)
   base.draw(win)

   text = font.render("Score: " + str(score), 1, (255, 255, 255))
   win.blit(text, (winWidth - 10 - text.get_width(), 10))
   text = font.render("Gen: " + str(gen), 1, (255, 255, 255))
   win.blit(text, (10, 10))
   text = font.render("Num Alive: " + str(numAlive), 1, (255, 255, 255))
   win.blit(text, (10, 50))

   pygame.display.update()

def fitness(genomes, config):
   global gen
   gen += 1
   
   #adjacency arrays
   nets = [] #list of neural networks for birds
   ge = [] #list of genomes
   birds = [] 

   for _, g in genomes: #genomes is a TUPLE: (genome key, genome object); we only care about genome object
      net = neat.nn.FeedForwardNetwork.create(g, config)
      nets.append(net)
      birds.append(Bird(230, 350))
      g.fitness = 0
      ge.append(g)

   base = Base(700)
   score = 0
   pipes = [Pipe(730, score)]
   win = pygame.display.set_mode((winWidth, windHeight))
   pygame.display.set_caption("Padmank's Flappy Bird AI")
   clock = pygame.time.Clock()

   run = True
   while run:
      clock.tick(60)
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               run = False
               pygame.quit()
               quit()
      numAlive = len(ge)
      pipeIndex = 0
      if len(birds) > 0:
         if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].topPipe.get_width():
            pipeIndex = 1
      else: #No birds left in a generation
         run = False
         break

      for x, bird in enumerate(birds):
         bird.move()
         ge[x].fitness += 0.033333

         distToTop = abs(bird.y - pipes[pipeIndex].height)
         distToBottom = abs(bird.y - pipes[pipeIndex].bottom)
         #RETURNS: List of output neurons; INPUT: Input nodes
         output = nets[x].activate((bird.y, distToTop, distToBottom)) 
         #our NN only has one output, hence output[0]
         if output[0] > 0.5:
            bird.jump()

      addPipe = False
      removePipes = []
      for pipe in pipes:
         for x, bird in enumerate(birds):
            if pipe.collide(bird):
               ge[x].fitness -= 1
               birds.pop(x)
               nets.pop(x)
               ge.pop(x)
            if not pipe.passed and pipe.x < bird.x:
               pipe.passed = True
               addPipe = True

         if pipe.x + pipe.topPipe.get_width() < 0: #if pipe is off the screen completely
            removePipes.append(pipe)
         pipe.move()

      if addPipe:
         score += 1
         for g in ge:
            g.fitness += 5
         pipes.append(Pipe(600, score))
      for r in removePipes:
         pipes.remove(r)

      #INCENTIVE To progress past 50, 60, 70, etc.
      if score > 50 and score % 10 == 0:
         if score > 100:
            for g in ge:
               g.fitness += score
         for g in ge:
               g.fitness += score
      
      for x, bird in enumerate(birds):
         if bird.y + bird.img.get_height() >= 730 or bird.y < 0: 
            birds.pop(x)
            nets.pop(x)
            ge.pop(x)
      
      base.move()
      drawWindow(win, birds, pipes, base, score, gen, numAlive)
      if score > 0:
         bestFitness, index = 0, 0
         if len(ge) > 130:
            for g in ge:
               if g.fitness > bestFitness:
                  bestFitness = g.fitness
                  index += 1
         pickle.dump(nets[index], open("victor.pickle", "wb"))
         print('changed victor file, score:' + str(score) + ' ' + str(index))
         break
   
def run(configFile):
   config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configFile)
   p = neat.Population(config)

   p.add_reporter(neat.StdOutReporter(True))
   p.add_reporter(neat.StatisticsReporter())

   victor = p.run(fitness, 50)
   print(victor)
   


if __name__ == "__main__":
   local_dir = os.path.dirname(__file__)
   configFile = os.path.join(local_dir, "config-feedforward.txt")
   run(configFile)

