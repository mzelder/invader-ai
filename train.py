from env import AInvaderEnv
from dqn_agent import DQNAgent

# Initialize the environment and the DQN agent
env = AInvaderEnv()
agent = DQNAgent(state_dim=4, action_dim=4)

# Set the number of episodes for training
num_episodes = 3

# Loop over each episode
for episode in range(num_episodes):
    # Reset the environment and get the initial state
    state = env.reset()
    total_reward = 0

    # Loop until the episode is done
    while True:
        # Get an action from the agent
        action = agent.get_action(state)
        # Take the action in the environment
        next_state, reward, done, _ = env.step(action)
        # Store the transition in the replay buffer
        agent.replay_buffer.append((state, action, reward, next_state, done))

        # Update the current state
        state = next_state
        # Accumulate the reward
        total_reward += reward
        # Train the agent
        agent.train()

        # Render the environment
        env.render()

        # Check if the episode is done
        if done:
            break

    # Print the total reward for the episode
    print(f'Episode {episode + 1}, Total Reward: {total_reward}')

# Close the environment
env.close()
