import random
import sys

import pygame

from objects import Bullet  # Import the Bullet class
from objects import Lives  # Import the Lives class
from objects import SpaceShip  # Import the SpaceShip class

# Set the dimensions of the game window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AInvader")  # Set the title of the game window
clock = pygame.time.Clock()


def main():
    pygame.init()
    text_color = (255, 255, 255)  # Set the text color to white
    font = pygame.font.Font(None, 48)
    spaceship = SpaceShip(WIDTH, HEIGHT)  # Create a SpaceShip object
    bullets = []  # List to store bullets
    lives = Lives(3, 10, 10)  # Create a Lives object with 3 initial lives

    while True:
        clock.tick(60)  # Set the frame rate to 60 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        if keys[pygame.K_UP]:
            spaceship.forward()
        if keys[pygame.K_DOWN]:
            spaceship.backward()
        if keys[pygame.K_LEFT]:
            spaceship.left()
        if keys[pygame.K_RIGHT]:
            spaceship.right()

        if random.randint(1, 20) == 1:  # Adjust the frequency as needed
            bullet_x = random.randint(0, WIDTH)
            # Add a new bullet at a random x position at the top
            bullets.append(Bullet(bullet_x, 0))

        # Update bullet positions
        for bullet in bullets:
            bullet.y += 5
            if bullet.y > HEIGHT:
                bullets.remove(bullet)
            # Check for collision between bullet and spaceship
            elif (
                    bullet.y + bullet.size >= spaceship.y and bullet.y <= spaceship.y + spaceship.size and  # Check if the bullet is in the same y position as the spaceship
                    bullet.x + bullet.size >= spaceship.x and bullet.x <= spaceship.x + spaceship.size):  # Check if the bullet is in the same x position as the spaceship
                lives.decrease()  # Decrease lives if bullet hits the spaceship
                bullets.remove(bullet)  # Remove the bullet

        window.fill((0, 0, 0))

        # Draw the spaceship
        spaceship.create(window)

        # Draw bullets
        for bullet in bullets:
            bullet.create(window)

        # Draw lives
        lives.draw(window)

        pygame.display.flip()

        # Check if the spaceship is out of lives
        if lives.is_out_of_lives():
            # Display "Game Over" text
            font = pygame.font.Font(None, 74)
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() //
                                         2, HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait for 3 seconds before exiting
            sys.exit()


if __name__ == "__main__":
    main()
