import pygame
from constants import (
    SCREEN_WIDTH,
    PLAYER_MAX_LIVES,
    LIFE_ICON_SIZE,
    LIFE_ICON_SPACING
)

class Lives:
    def __init__(self):
        self.lives = PLAYER_MAX_LIVES

    def lose_life(self):
        self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0

    def reset(self):
        self.lives = PLAYER_MAX_LIVES

    def draw(self, screen):
        start_x = SCREEN_WIDTH - 30
        start_y = 30

        reserve_lives = max(0, self.lives - 1)

        for i in range(reserve_lives):
            x = start_x - (i * LIFE_ICON_SPACING)
            y = start_y

            points = [
                (x, y - LIFE_ICON_SIZE // 2),
                (x + LIFE_ICON_SIZE // 2, y + LIFE_ICON_SIZE),
                (x - LIFE_ICON_SIZE // 2, y + LIFE_ICON_SIZE)
            ]
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)