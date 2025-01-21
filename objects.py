import pygame

class SpaceShip:
    def __init__(self, width, height, speed):
        # Initialize the spaceship with size, color, position, and speed
        self.height = height
        self.width = width
        self.size = 20
        self.color = (255, 0, 0)
        self.x = width // 2
        self.y = height - self.size
        self.speed = speed

    def create(self, window):
        # Draw the spaceship on the game window
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.size, self.size))

    def left(self):
        if self.x - self.speed <= 0: return None
        self.x -= self.speed

    def right(self):
        if self.x + self.speed >= self.width - self.size: return None
        self.x += self.speed


class Bullet:
    def __init__(self, x, y, speed):
        # Initialize the bullet with size, color, position, and speed
        self.size = 20
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.speed = speed

    def create(self, window):
        # Draw the bullet on the game window
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.size, self.size))

    def move(self):
        self.y += self.speed