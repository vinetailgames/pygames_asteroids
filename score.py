import pygame

from constants import (
    HIGHSCORE_FILE,
    SCORE_SMALL_ASTEROID,
    SCORE_MEDIUM_ASTEROID,
    SCORE_LARGE_ASTEROID,
)

class Score:
    def __init__(self):
        self.score = 0
        self.highscore = self.load_highscore()
        self.font = pygame.font.Font(None, 36)

    def load_highscore(self):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_highscore(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.highscore))

    def add_asteroid_points(self, asteroid_size):
        points = {
            "small": SCORE_SMALL_ASTEROID,
            "medium": SCORE_MEDIUM_ASTEROID,
            "large": SCORE_LARGE_ASTEROID,
        }[asteroid_size]
        self.score += points
        if self.score > self.highscore:
            self.highscore = self.score
            self.save_highscore()

    def reset(self):
        self.score = 0 

    def draw(self, screen):
        highscore_text = self.font.render(
            f"Highscore: {self.highscore}", True, (255, 255, 255)
        )
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(highscore_text, (10, 10))
        screen.blit(score_text, (10, 50))