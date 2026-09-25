import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROIDS_PER_WAVE
from sounds import play_background_music


class GameOver:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 74)
        self.option_font = pygame.font.Font(None, 36)

    def draw(self, screen):
        # Render the "Game Over" title
        title_surf = self.title_font.render("Game Over", True, (255, 0, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_surf, title_rect)

        # Render the instructions: Restart or Quit
        options_surf = self.option_font.render("Press [R] to Restart   |   Press [Q] to Quit", True, (255, 255, 255))
        options_rect = options_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(options_surf, options_rect)

    def handle_input(self):
        """
        Polls events while on the game over screen.
        Returns:
            "restart" if R is pressed
            "quit" if Q, ESC, or window close is triggered
            None if still waiting
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return "quit"
        return None

    def restart(self, player, score, lives, asteroids, shots, asteroid_field):
        for a in asteroids:
            a.kill()
        for s in shots:
            s.kill()

        score.reset()
        if hasattr(lives, "reset"):
            lives.reset()

        player.respawn(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        asteroid_field.start_wave(ASTEROIDS_PER_WAVE)

        pygame.mixer.music.stop()
        play_background_music()