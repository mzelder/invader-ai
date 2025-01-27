import pygame
import random
import math
from objects import SpaceShip, Bullet
from enum import Enum

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

SPEED = 20
SPAWN_RATE = 30

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

class InvaderGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('InvaderGame')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.bullets = []
        self.score = 0
        self.spaceship = SpaceShip(self.w, self.h, SPEED)
        self.frame_iteration = 0

    def _spawn_bullets(self):
        if self.frame_iteration % SPAWN_RATE == 0:
            for i in range(15):
                self.bullets.append(Bullet(random.randint(0, 640), 0, SPEED))
                
    def play_step(self):
        self.frame_iteration += 1

        # Handle player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Drop bullets
        self._spawn_bullets()
        for bullet in self.bullets:
            bullet.move()
            if bullet.y > self.h:
                self.bullets.remove(bullet)

        # Update score
        if self.frame_iteration % SPAWN_RATE == 0:
            self.score += 1

        # Check if the game is over
        game_over = False
        if self.is_collision():
            print("COLISION")
            game_over = True
            #return game_over, self.score

        # AI Decision-Making (using fake Q-learning simulation)
        state = self.get_state()
        self.ai_decision(state)

        # Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def get_state(self):
        # Returns the state as a list indicating whether bullets are coming from the front, left, or right
        state = []
        front = False
        left = False
        right = False

        for bullet in self.bullets:
            # Check if a bullet is in front
            if self.spaceship.x - self.spaceship.size < bullet.x < self.spaceship.x + self.spaceship.size:
                front = True

            # Check if a bullet is on the left
            if (
                bullet.x <= self.spaceship.x - bullet.size and
                bullet.x >= self.spaceship.x - self.spaceship.size * 2 and
                self.spaceship.y - self.spaceship.size * 16 <= bullet.y <= self.spaceship.y + self.spaceship.size
            ):
                left = True

            # Check if a bullet is on the right
            if (
                bullet.x >= self.spaceship.x + self.spaceship.size and
                bullet.x <= self.spaceship.x + self.spaceship.size * 2 and
                self.spaceship.y - self.spaceship.size * 16 <= bullet.y <= self.spaceship.y + self.spaceship.size
            ):
                right = True
        
        return [int(front), int(left), int(right)]

    def ai_decision(self, state):
        # Fake Q-learning simulation for dodging bullets
        # Based on the state, we choose a direction
        if state[0] == 1:
            # Bullet is in front, so move left or right randomly
            move = random.randint(0, 1)
            if move == 1:
                self.spaceship.left()
            else:
                self.spaceship.right()

    def is_collision(self):
        for bullet in self.bullets:
            if (
                bullet.y + bullet.size >= self.spaceship.y
                and bullet.y < self.spaceship.y + self.spaceship.size
                and bullet.x + bullet.size > self.spaceship.x
                and bullet.x < self.spaceship.x + self.spaceship.size
            ):
                return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        self.spaceship.create(self.display)
        for bullet in self.bullets:
            bullet.create(self.display)

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

if __name__ == "__main__":
    game = InvaderGame()

    while True:
        game_over, score = game.play_step()

        if game_over:
            game.reset()
