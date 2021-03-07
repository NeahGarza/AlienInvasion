import pygame

#   Pygame loads bitmaps images (.bmp files) by default
#   Ship and screen treated as rectangles
#   Coordinates represent image's top left (x,y) corner
#   Screen starts at top left and increases bottom to right

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flags"""
        if self.moving_right:
            self.rect.x += 1
        #Not making this statement an elif to:
        #  1) nothing when both keys pressed and 2) would give right key priority
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)