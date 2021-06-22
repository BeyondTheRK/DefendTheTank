import pygame.font

class Button():

    def __init__(self, ai_settings, screen):
        """initialize buttom attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Set dimensions and properties of button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Sans", 48, bold=False, italic=False)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # button message needs to prepped once
     #   self.prep_msg("Play")

  #  def prep_msg(self):
        """Turn msg in to a rendered image and center text on the button."""
        self.msg_image = self.font.render('Play', True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #draw blank button then draw mssage
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
