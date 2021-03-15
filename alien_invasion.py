import sys
#Import sleep method from time module so we can pause game for a moment when a ship is hit
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
#   OBJECT assigned to self.screen is a surface 
#   SURFACE = part of screen where element can be displayed; each alien/ship is its own surface
#   COLORS specified as RGB colors: red, green, blue
#   VALUES range from 0 - 255
#   for event in pygame.event.get() runs a for loop getting events that happened since loop was called
#   Loop keeps calling the screen, loading it anew each time (transition is smooth so user can't really tell)
#   Helper method (one _) works inside a class but isn't called through the instance
#   Each keypress by user is registered as a KEYDOWN event
#   Need to eventually get rid of created bullets because they keep going (just off screen and up/negative)
#   _create_fleet method creates instance of Alien, then adds it to the group that will hold the fleet
#   floor division (//) divides numbers and drops remainder, so just returns an int
#   Always need to call check_events() to see if user Quits or closes window
#   Game should freeze when user loses all ships

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

        #Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        #Set the background color
        self.bg_color = (230, 230, 230)

        self.ship = Ship(self)
        #Group will store all live bullets in game
        #Group is instance of sprite class and behaves like a list with added functionality
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make the Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Next line returns a tuple containing mouse cursor's x and y coordinates when mouse is clicked
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the Player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset game settings
            self.settings.initialize_dynamic_settings()
            #Hide mouse cursor when mouse is over game window
            pygame.mouse.set_visible(False)
            #Next line checks whether mouse click overlaps the Play button region; 
            #   if yes, set game_active to True and start game
            if self.play_button.rect.collidepoint(mouse_pos):
                #Reset the game statistics
                self.stats.reset_stats()
                self.stats.game_active = True

                #Get rid of any remaining aliens and bullets
                self.aliens.empty()
                self.bullets.empty()

                #Create a new fleet and center the ship
                self._create_fleet()
                self.ship.center_ship()

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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):  
        """Respond to bullet-alien collisions"""
        #Remove any bullets or aliens that have collided
        #Check for any bullets that have hit aliens
        #If so, get rid of the bullet and the alien
        #This line compares positions of all bullets in self.bullets and all aliens in self.aliens and identifies overlap
        #Two true arguments tell pygame to delete the bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            #Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_screen(self):
        """Updates images on the screen, and flip to the new screen"""
        #Redrawing screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #When draw used on group, Pygame draws each element at position defined by rect attribute
        self.aliens.draw(self.screen)

        #Draw the score info
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        #Make the most recently drawn screen visible
        pygame.display.flip()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row
        #Spacing between each alien is equal to one alien width
        #THIS ALIEN INSTANCE WILL ONLY BE USED TO CALCULATE SCREEN/ALIEN DIMENSIONS
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                 (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #Create an alien and place it in the row
        alien = Alien(self)
        #  each alien is is pushed to the right one alien width from the left margin
        #  multiplying each alien width by 2 to account for each space each alien occupies (including empty space to right)
        #  we then multiply this amount by alien's position in row; using alien's x attrib to set position of its rect
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x 
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        Check if he fleet is at an edge, 
        then update the positions of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions
        #Two arguments are a sprite and a group
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        #Going through the group of aliens and checking the position of each one to see if it's at bottom of screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #Decrement ships/lives left
            self.stats.ships_left -= 1

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #After this pause: code moves to the _update_screen() method that draws new fleet to screen
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()