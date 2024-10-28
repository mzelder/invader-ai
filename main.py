import pygame
import sys

WIDTH, HEIGHT = 800, 600
screen = pygame.display
screen.set_mode((WIDTH, HEIGHT))
screen.set_caption("AInvader") 

def main():
    pygame.init()
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 48)
    text = font.render("Window Test", True, text_color)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                sys.exit()  

if __name__ == "__main__":
    main()
