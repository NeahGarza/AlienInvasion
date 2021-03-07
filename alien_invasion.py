import sys
import pygame

from settings import Settings

#   OBJECT assigned to self.screen is a surface 
#   SURFACE = part of screen where element can be displayed; each alien/ship is its own surface
#   COLORS specified as RGB colors: red, green, blue
#   VALUES range from 0 - 255
#   for event in pygame.event.get() runs a for loop getting events that happened since loop was called
#   Loop keeps calling the screen, loading it anew each time (transition is smooth so user can't really tell)

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        #Set the background color
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)

            #Make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()