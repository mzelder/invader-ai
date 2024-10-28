import pygame

class SpaceShip:
    def __init__(self, width, height):
        self.size = 25
        self.color = (255, 0, 0)
        self.x = width // 2
        self.y = height - self.size
        self.speed = 10

    def create(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def forward(self):
        self.y -= self.speed
    
    def backward(self):
        self.y += self.speed

    def left(self):
        self.x -= self.speed
    
    def right(self):
        self.x += self.speed