import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

#   OBJECT assigned to self.screen is a surface 
#   SURFACE = part of screen where element can be displayed; each alien/ship is its own surface
#   COLORS specified as RGB colors: red, green, blue
#   VALUES range from 0 - 255
#   for event in pygame.event.get() runs a for loop getting events that happened since loop was called
#   Loop keeps calling the screen, loading it anew each time (transition is smooth so user can't really tell)
#   Helper method (one _) works inside a class but isn't called through the instance
#   Each keypress by user is registered as a KEYDOWN event
#   Need to eventually get rid of created bullets because they keep going (just off screen and up/negative)

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        
        #Modifying game to run in fullscreen mode
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #Set the background color
        self.bg_color = (230, 230, 230)

        self.ship = Ship(self)
        #Group will store all live bullets in game
        #Group is instance of sprite class and behaves like a list with added functionality
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        #Respond to keyboard and mouse events. 
        for event in pygame.event.get():
            #if exit
            if event.type == pygame.QUIT:
                sys.exit()
            #if right/left key is pressed
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            #if right/left key was let go
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
                """Update the position of bullets and get rid of old bullets"""
                #Update all bullet positions
                #When update is called on a group, group automatically calls update() for each sprite in group
                self.bullets.update()      
                
                #Get rid of bullets that have disappeared
                for bullet in self.bullets.copy():
                    #When using for loop for a list, we can't remove items form a list/group;
                    #     we use copy() to modify bullets inside the loop
                    if bullet.rect.bottom <= 0:
                        self.bullets.remove(bullet)

    def _update_screen(self):
        """Updates images on the screen, and flip to the new screen"""
        #Redrawing screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()