import pygame

#   Pygame loads bitmaps images (.bmp files) by default
#   Ship and screen treated as rectangles
#   Coordinates represent image's top left (x,y) corner
#   Screen starts at top left and increases bottom to right
#   Only integer portion of self.x will be stored in self.rect.x
#   With rect OBJECT, you can use (x,y) for top, bottom, left, and right edges

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the ship's horizontal position (rect can only store integers)
        self.x = float(self.rect.x)

        #Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flags"""

        #Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        #Not making this statement an elif to:
        #    1) nothing when both keys pressed and 2) would give right key priority
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #Update rect object with self.x value
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        #Resetting x attrib to track ship's exact position
        #Never make more than one ship; ships_left will let us know when no lives left
        self.x = float(self.rect.x)