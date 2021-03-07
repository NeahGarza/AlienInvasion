#   IMPORTING the sys and pygame modules; pygame helps create game functionality and sys exits
import sys
import pygame

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        
        #   CREATING a display window
        #   (1200, 800) is a tuple that defines window dimensions in pixels
        #   OBJECT assigned to self.screen is a surface 
        #   SURFACE = part of screen where element can be displayed; each alien/ship is its own surface
        #   SURFACE updated with each user input (redrawn with every loop iteration)
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

        #Set the background color
        self.bg_color = (230, 230, 230)

    #   ENTIRE game controlled by this method
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                #   FOR loop returns a list of events that take place since last time called
                if event.type == pygame.QUIT:
                    sys.exit()

            #Redraw the screen during each pass through the loop
            self.screen.fill(self.bg_color)

            #Make the most recently drawn screen visible
            #   CONTINUALLY updates display window to show new positions of game elements & hiding old ones
            pygame.display.flip()

#   ONLY runs the game if file (main) is directly called
if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()