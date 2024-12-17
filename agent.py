import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
import os

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # Exploration rate
        self.gamma = 0.9  # Discount factor
        self.memory = deque(maxlen=100_000)
        self.model = Linear_QNet(5, 256, 4)
        self.trainer = QTrainer(self.model, lr=0.001, gamma=self.gamma)
        self.model_path = './model/model.pth'

    def get_state(self, spaceship, bullets, lives, width, height):
        state = [
            spaceship.x / width,
            spaceship.y / height,
            len(bullets) / 10,
            lives.lives,
            random.random(),  # Additional feature
        ]
        return np.array(state, dtype=float)

    def act(self, state):
        self.epsilon = 80 - self.n_games  # Decrease exploration over time
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
        else:
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
        self.model.save(self.model_path)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model.load_state_dict(torch.load(self.model_path))
            self.model.eval()  # Set the model to evaluation mode
            print(f"Model loaded from {self.model_path}")
        else:
            print(f"No saved model found at {self.model_path}")