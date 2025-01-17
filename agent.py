import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
import os

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 1.0  # Start with full exploration
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.epsilon_decay = 0.995  # Decay factor for epsilon
        self.gamma = 0.9
        self.memory = deque(maxlen=100_000)
        self.model = Linear_QNet(4, 256, 2)
        self.trainer = QTrainer(self.model, lr=0.001, gamma=self.gamma)
        
    def get_state(self, spaceship, bullets, lives, WIDTH, HEIGHT):
        # State could include:
        # - spaceship position (x, y)
        # - closest bullet's position (if any)
        # - distance to nearest bullet
        # - spaceship's speed
        # - number of lives left
        state = [
            spaceship.x / WIDTH,  # Normalize position of spaceship
            spaceship.y / HEIGHT,  # Normalize position of spaceship
            lives.lives,  # Number of lives left
        ]

        # Include distance to nearest bullet
        if bullets:  # Check if there are any bullets
            closest_bullet_distance = min(abs(bullet.x - spaceship.x) for bullet in bullets)
        else:
            closest_bullet_distance = WIDTH  # No bullets: Set max possible distance

        state.append(closest_bullet_distance / WIDTH)  # Normalize distance to nearest bullet
        print(closest_bullet_distance)
        return state


    def act(self, state):
        # Decay epsilon after each game
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        if random.random() < self.epsilon:
            print("HERE")
            # Exploration: Random action
            move = random.randint(0, 1)
        else:
            # Exploitation: Predict the best action
            state_tensor = torch.tensor(state, dtype=torch.float).unsqueeze(0)
            prediction = self.model(state_tensor)
            move = torch.argmax(prediction).item()
        return move


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > 1000:
            mini_sample = random.sample(self.memory, 1000)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def save_model(self):
        self.model.save()

    def load_model(self):
        self.model.load()