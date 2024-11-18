import random
import gym
import numpy as np
import pygame
from gym import spaces
from objects import SpaceShip, Bullet, Lives

WIDTH, HEIGHT = 800, 600


class AInvaderEnv(gym.Env):
    def __init__(self):
        super(AInvaderEnv, self).__init__()
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AInvader AI")
        self.clock = pygame.time.Clock()

        # Initialize game objects
        self.spaceship = SpaceShip(WIDTH, HEIGHT)
        self.bullets = []
        self.lives = Lives(3, 10, 10)

        # Define action and observation space
        self.action_space = spaces.Discrete(4)  # Actions: [0=up, 1=down, 2=left, 3=right]
        self.observation_space = spaces.Box(low=0, high=255, shape=(4,), dtype=np.float32)

    def reset(self):
        # Reset the game state
        self.spaceship = SpaceShip(WIDTH, HEIGHT)
        self.bullets = []
        self.lives = Lives(3, 10, 10)
        return self._get_state()

    def _get_state(self):
        # Get the state of the game: [spaceship_x, spaceship_y, nearest_bullet_x, nearest_bullet_y]
        if self.bullets:
            nearest_bullet = min(self.bullets, key=lambda b: b.y)
            return np.array([self.spaceship.x, self.spaceship.y, nearest_bullet.x, nearest_bullet.y])
        return np.array([self.spaceship.x, self.spaceship.y, WIDTH, HEIGHT])

    def step(self, action):
        # Take an action: move the spaceship
        if action == 0:
            self.spaceship.forward()
        elif action == 1:
            self.spaceship.backward()
        elif action == 2:
            self.spaceship.left()
        elif action == 3:
            self.spaceship.right()

        # Generate new bullets randomly
        if random.randint(1, 20) == 1:
            bullet_x = random.randint(0, WIDTH)
            self.bullets.append(Bullet(bullet_x, 0))

        # Update bullets
        for bullet in self.bullets:
            bullet.y += 5
            if bullet.y > HEIGHT:
                self.bullets.remove(bullet)
            elif (bullet.y + bullet.size >= self.spaceship.y and
                  bullet.y <= self.spaceship.y + self.spaceship.size and
                  bullet.x + bullet.size >= self.spaceship.x and
                  bullet.x <= self.spaceship.x + self.spaceship.size):
                self.lives.decrease()
                self.bullets.remove(bullet)

        # Calculate reward
        reward = 1
        done = self.lives.is_out_of_lives()
        if done:
            reward = -100

        # Return step information
        return self._get_state(), reward, done, {}

    def render(self):
        # Render the game window
        self.window.fill((0, 0, 0))
        self.spaceship.create(self.window)
        for bullet in self.bullets:
            bullet.create(self.window)
        self.lives.draw(self.window)
        pygame.display.flip()
        self.clock.tick(60)

    def close(self):
        # Close the game window
        pygame.quit()
