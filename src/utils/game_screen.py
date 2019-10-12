import pygame

display_width = 150
display_height = 50


class GameHandler:
    def __init__(self, game_display):
        self.gameDisplay = game_display

    def text_objects(self, text, font):
        textSurface = font.render(text, True, pygame.color.Color("black"))
        return textSurface, textSurface.get_rect()

    def message_display(self, text, position=None):
        if position is None:
            position = [int(display_width / 2), int(display_height / 2)]
        largeText = pygame.font.Font('freesansbold.ttf', 18)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        TextRect.center = position
        self.gameDisplay.blit(TextSurf, TextRect)
