import random
import numpy as np
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim

# Define the Deep Q-Network (DQN) model
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        # Define the layers of the neural network
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        # Define the forward pass
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Define the DQN Agent
class DQNAgent:
    def __init__(self, state_dim, action_dim):
        # Initialize the DQN model
        self.model = DQN(state_dim, action_dim)
        # Define the optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        # Define the loss function
        self.loss_fn = nn.MSELoss()
        # Initialize the replay buffer
        self.replay_buffer = deque(maxlen=10000)
        # Set the batch size
        self.batch_size = 64
        # Set the discount factor
        self.gamma = 0.99
        # Set the exploration rate
        self.epsilon = 1.0
        # Set the exploration decay rate
        self.epsilon_decay = 0.995
        # Set the minimum exploration rate
        self.epsilon_min = 0.1

    def get_action(self, state):
        # Select an action using epsilon-greedy policy
        if random.random() < self.epsilon:
            return random.randint(0, 3)
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            return torch.argmax(self.model(state)).item()

    def train(self):
        # Train the DQN model
        if len(self.replay_buffer) < self.batch_size:
            return

        # Sample a batch from the replay buffer
        batch = random.sample(self.replay_buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convert batch data to tensors
        states = torch.tensor(np.array(states), dtype=torch.float32)
        actions = torch.tensor(np.array(actions))
        rewards = torch.tensor(np.array(rewards))
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        dones = torch.tensor(np.array(dones), dtype=torch.float32)

        # Compute Q-values and targets
        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze()
        next_q_values = self.model(next_states).max(1)[0]
        targets = rewards + self.gamma * next_q_values * (1 - dones)

        # Compute the loss
        loss = self.loss_fn(q_values, targets)
        # Perform backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Update the exploration rate
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay