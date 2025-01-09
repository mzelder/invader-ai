import pygame
import random
import sys
from objects import SpaceShip, Bullet, Lives
from agent import Agent
from helper import plot

# Game configuration
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Invader")
clock = pygame.time.Clock()
plot_scores = []
plot_mean_scores = []

def main():
    pygame.init()
    agent = Agent()  # RL agent
    total_score = 0  # Track total score across episodes

    # Load the model if it exists
    agent.load_model()

    while True:  # Infinite loop for episodes
        # Reset environment for new episode
        spaceship = SpaceShip(WIDTH, HEIGHT)
        bullets = []
        lives = Lives(1, 10, 10)
        score = 0
        done = False

        while not done:
            clock.tick(60)

            # Get current state
            state = agent.get_state(spaceship, bullets, lives, WIDTH, HEIGHT)
            
            # Agent takes action
            action = agent.act(state)

            # Map action to game controls
            if action == 0: spaceship.left()
            elif action == 1: spaceship.right()
            elif action == 2: spaceship.forward()
            elif action == 3: spaceship.backward()

            # Spawn bullets
            if random.randint(1, 20) == 1:
                bullets.append(Bullet(random.randint(0, WIDTH), 0))

            # Update bullet positions and check collisions
            reward = 0
            for bullet in bullets[:]:
                bullet.y += 5
                if bullet.y > HEIGHT:
                    bullets.remove(bullet)
                elif (
                    bullet.y + bullet.size >= spaceship.y
                    and bullet.y <= spaceship.y + spaceship.size
                    and bullet.x + bullet.size >= spaceship.x
                    and bullet.x <= spaceship.x + spaceship.size
                ):
                    bullets.remove(bullet)
                    lives.decrease()
                    reward = -10

            if lives.is_out_of_lives():
                done = True
                reward -= 50  # Additional penalty for losing
            else:
                reward += 1  # Reward for surviving a frame

            # Update the display
            window.fill((0, 0, 0))
            spaceship.create(window)
            for bullet in bullets:
                bullet.create(window)
            lives.draw(window)
            pygame.display.flip()

            # Get the next state and train agent
            next_state = agent.get_state(spaceship, bullets, lives, WIDTH, HEIGHT)
            agent.train_short_memory(state, action, reward, next_state, done)
            agent.remember(state, action, reward, next_state, done)

            score += reward

        # After the episode ends, train the agent on long memory
        agent.train_long_memory()

        # Track total score and print episode results
        print(f"Episode complete! Score: {score}, Total Score: {total_score}")
        
        # Save the model after each episode
        agent.save_model()

        # Increment game count
        plot_scores.append(score)
        total_score += score
        agent.n_games += 1
        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    main()
