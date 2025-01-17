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
episodes = 1000
BULLET_SPAWN_INTERVAL = 60

def main():
    pygame.init()
    agent = Agent()  # RL agent
    total_score = 0  # Track total score across episodes

    # Load the model if it exists
    agent.load_model()

    for _ in range(episodes):
        # Reset environment for new episode
        spaceship = SpaceShip(WIDTH, HEIGHT)
        bullets = []
        lives = Lives(1, 10, 10)
        score = 0
        done = False
        frame_counter = 0

        while not done:
            clock.tick(60)
            frame_counter += 1
            reward = 0

            # Get current state
            state = agent.get_state(spaceship, bullets, lives, WIDTH, HEIGHT)
            
            # Agent takes action
            action = agent.act(state)

            # Map action to game controls (left or right only)
            if action == 0: spaceship.left()
            elif action == 1: spaceship.right()

            # Spawn bullets at consistent intervals
            if frame_counter % BULLET_SPAWN_INTERVAL == 0:
                # Random 5 bullets
                for _ in range(5):
                    bullets.append(Bullet(random.randint(0, WIDTH), 0))
                # Bullet on the left side of the screen
                bullets.append(Bullet(0, 0))
                # Bullet on the right side of the screen
                bullets.append(Bullet(WIDTH - 20, 0))  # Adjust `20` based on bullet width

            # Update bullet positions and check collisions
            reward += 1  # Reward for surviving a frame
            for bullet in bullets[:]:
                bullet.move()
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

            # Check if game is over
            if lives.is_out_of_lives():
                done = True
                reward -= 50

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
