import pygame
from constants import *

class Lives:
    def __init__(self):
        self.lives = PLAYER_MAX_LIVES
        self.icon = pygame.image.load("textures/battleship.png").convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (LIFE_ICON_SIZE, LIFE_ICON_SIZE))

    def lose_life(self):
        self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0

    def reset(self):
        self.lives = PLAYER_MAX_LIVES

    def gain_life(self):
        self.lives = min(self.lives + 1, PLAYER_MAX_LIVES_CAP)

    def draw(self, screen):
        start_x = SCREEN_WIDTH - 30
        start_y = 30

        reserve_lives = max(0, self.lives - 1)

        for i in range(reserve_lives):
            x = start_x - (i * LIFE_ICON_SPACING)
            y = start_y
            icon_rect = self.icon.get_rect(center=(x, y))
            screen.blit(self.icon, icon_rect)