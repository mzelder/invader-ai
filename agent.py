import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from objects import Bullet
from game import InvaderAI
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(4, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
    def get_state(self, spaceship, bullets):
        state = [
            spaceship.x,
        ]

        front = False
        left = False
        right = False

        for bullet in bullets:
            # Check if a bullet is in front
            if spaceship.x - spaceship.size < bullet.x < spaceship.x + spaceship.size:
                front = True
            
            # Check if a bullet is on the left
            if (
                bullet.x <= spaceship.x - bullet.size and
                bullet.x >= spaceship.x - spaceship.size * 2 and
                spaceship.y - spaceship.size * 16 <= bullet.y <= spaceship.y + spaceship.size
            ):
                left = True

            # Check if a bullet is on the right
            if (
                bullet.x >= spaceship.x + spaceship.size and
                bullet.x <= spaceship.x + spaceship.size * 2 and
                spaceship.y - spaceship.size * 16 <= bullet.y <= spaceship.y + spaceship.size
            ):
                right = True


        directions = [int(front), int(left), int(right)]
        state = state + directions
        print(state)
        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 500 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            #print(f"random {move}")
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            #print(f"predicted {move}")
        return move

def train():    
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = InvaderAI()
    while True:
        # Get old state
        state_old = agent.get_state(
            game.spaceship, 
            game.bullets
        )

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(
            game.spaceship, 
            game.bullets, 
        )

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
    