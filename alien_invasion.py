import sys
import pygame

from settings import Settings
from ship import Ship

#   OBJECT assigned to self.screen is a surface 
#   SURFACE = part of screen where element can be displayed; each alien/ship is its own surface
#   COLORS specified as RGB colors: red, green, blue
#   VALUES range from 0 - 255
#   for event in pygame.event.get() runs a for loop getting events that happened since loop was called
#   Loop keeps calling the screen, loading it anew each time (transition is smooth so user can't really tell)
#   Helper method (one _) works inside a class but isn't called through the instance

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

        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        #Respond to keyboard and mouse events. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
    def _update_screen(self):
        """Updates images on the screen, and flip to the new screen"""
        #Redrawing screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        #Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()