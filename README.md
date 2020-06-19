# FlappyBirdAI
An AI that masters the infamously difficult game of "Flappy Bird" using a genetic algorithm, NEAT
# How To Run This Project
Simply clone or download this repo onto your machine and run game.py
# How It Works
The AI is built and trained using NEAT(Neuroevolution of augmenting topologies). The AI can "see", or in other words is given the inputs of, its vertical distance(height), the distance to the top pipe, and the distance to the bottome pipe. Initially, during GEN 1, the neural network generates random weights, causing the AI do behave randomly. The birds that progress the farthest are given a higher fitness score. The bird with the highest fitness score in a generation gets to pass its "genes", its weights, to the next generation of birds. This cycle continues until we have a perfect AI for the bird and the program then terminates.
