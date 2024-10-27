import pygame
import sys

# Function to create a window with given width and height


def create_window(width, height):
    pygame.init()
    # Set the display mode with the specified width and height
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("AInvader")  # Set the window title
    return screen

# Main function to run the game loop


def main():
    width = 800  # Width of the window
    height = 600  # Height of the window
    screen = create_window(width, height)
    background_color = (0, 0, 0)  # Background color (black)
    text_color = (255, 255, 255)  # Text color (white)
    font = pygame.font.Font(None, 48)  # Default font with size 48
    text = font.render("Window Test", True, text_color)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the quit event is triggered
                sys.exit()  # Exit the program

        # Fill the screen with the background color
        screen.fill(background_color)
        # Draw the text in the center of the screen
        screen.blit(text, (width/2 - text.get_width() /
                    2, height/2 - text.get_height()/2))
        pygame.display.flip()


if __name__ == "__main__":
    main()
