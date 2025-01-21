import pygame
import random
from objects import SpaceShip, Bullet
from enum import Enum

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

#rgb colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

SPEED = 40
SPAWN_RATE = 30

class InvaderAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('InvaderAI')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        self.bullets = []
        self.score = 0
        self.spaceship = SpaceShip(self.w, self.h, SPEED)
        self.frame_iteration = 0

    def _spawn_bullets(self):
        if self.frame_iteration % SPAWN_RATE == 0:
            for i in range(5):
                self.bullets.append(Bullet(i * 100, 0, SPEED))
                # self.bullets.append(random.randint(0, 450), 0, SPEED)


    def play_step(self, action):
        self.frame_iteration += 1
        #collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)

        # drop bullets
        self._spawn_bullets()
        for bullet in self.bullets:
            bullet.move()
            if bullet.y > self.h:
                self.bullets.remove(bullet)

        # score up
        reward = 0
        if self.frame_iteration % SPAWN_RATE == 0:
            self.score += 1
            reward = 10
        
        # 3. check if game is over
        game_over = False
        if self.is_collision():
            game_over = True
            reward = -50
            return reward, game_over, self.score

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
        
        
    def _move(self, action):
        if action == 0:
            self.spaceship.left()
        elif action == 1:
            self.spaceship.right()

    
    def is_collision(self):
        for bullet in self.bullets:
            if (
                bullet.y + bullet.size >= self.spaceship.y
                and bullet.y <= self.spaceship.y + self.spaceship.size
                and bullet.x + bullet.size >= self.spaceship.x
                and bullet.x <= self.spaceship.x + self.spaceship.size
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


