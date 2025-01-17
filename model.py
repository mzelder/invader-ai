import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)  # Output size should be 2 (left or right)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        # Define a clean model folder path
        model_folder_path = './model'

        # Combine the folder path and file name properly
        full_file_path = os.path.join(model_folder_path, file_name)

        # Save the model's state dictionary
        with open(full_file_path, "w") as f:
            pass
        torch.save(self.state_dict(), full_file_path)
        

    def load(self, file_name='model.pth'):
        # Define the model folder and file paths
        model_folder_path = './model'
        full_file_path = os.path.join(model_folder_path, file_name)

        # Ensure the directory exists
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        # Check if the file exists; if not, print a warning and initialize an empty model
        if not os.path.exists(full_file_path):
            print(f"No saved model found at {full_file_path}. Initializing a new model.")
            self.save(file_name)  # Save an empty model for future use
            return

        # Load the model's state dictionary
        self.load_state_dict(torch.load(full_file_path))
        self.eval()


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # Convert inputs to PyTorch tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # Ensure tensors have the correct shape
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Predicted Q-values for the current state
        pred = self.model(state)

        # Target Q-values
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][action[idx].item()] = Q_new

        # Compute loss and optimize
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()
