# add to objects.py yours bullets class
from objects import SpaceShip
import pygame
import sys

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AInvader") 
clock = pygame.time.Clock()

def main():
    pygame.init()
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 48)
    spaceship = SpaceShip(WIDTH, HEIGHT)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                sys.exit()  
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            spaceship.forward()
        if keys[pygame.K_DOWN]:
            spaceship.backward()
        if keys[pygame.K_LEFT]:
            spaceship.left()
        if keys[pygame.K_RIGHT]:
            spaceship.right()

        window.fill((0, 0, 0))
        spaceship.create(window)
        pygame.display.flip()

if __name__ == "__main__":
    main()
