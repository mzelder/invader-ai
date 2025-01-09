import pygame

multiplier = 2

class SpaceShip:
    def __init__(self, width, height):
        # Initialize the spaceship with size, color, position, and speed
        self.height = height
        self.width = width
        self.size = 25
        self.color = (255, 0, 0)
        self.x = width // 2
        self.y = height - self.size
        self.speed = 10 * multiplier

    def create(self, window):
        # Draw the spaceship on the game window
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.size, self.size))

    def forward(self):
        if self.y - self.speed <= 0: return None
        self.y -= self.speed

    def backward(self):
        if self.y + self.speed >= self.height - self.size: return None
        self.y += self.speed

    def left(self):
        if self.x - self.speed <= 0: return None
        self.x -= self.speed

    def right(self):
        if self.x + self.speed >= self.width - self.size: return None
        self.x += self.speed


class Bullet:
    def __init__(self, x, y):
        # Initialize the bullet with size, color, position, and speed
        self.size = 20
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.speed = 10 * multiplier

    def create(self, window):
        # Draw the bullet on the game window
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.size, self.size))

    def move(self):
        self.y -= self.speed

    def off_screen(self, height):
        return self.y < 0


class Lives:
    def __init__(self, initial_lives, x, y):
        # Initialize the lives with the initial number of lives and position
        self.lives = initial_lives
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 36)

    def decrease(self):
        # Decrease the number of lives by 1
        if self.lives > 0:
            self.lives -= 1

    def is_out_of_lives(self):
        # Check if the spaceship is out of lives
        return self.lives <= 0

    def draw(self, window):
        lives_text = self.font.render(
            f'Lives: {self.lives}', True, (255, 255, 255))
        window.blit(lives_text, (self.x, self.y))
