import pygame
import sys
from constants import *
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from shot import Shot
from asteroidfield import AsteroidField
from sounds import play_background_music, explosion_sound
from score import Score
from lives import Lives
from gameover import GameOver

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    Shot.containers = (updatable, drawable, shots)
    AsteroidField.containers = (updatable,)


    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField()

    play_background_music()

    score = Score()
    lives = Lives()
    game_over_screen = GameOver()
    is_game_over = False

    level = 1
    in_transition = False
    transition_timer = 0.0
    transition_stage = 0
    transition_blink_timer = 0.0
    transition_message_visible = True

    while True:
        if is_game_over:
            action = game_over_screen.handle_input()
            if action == "quit":
                return
            elif action == "restart":
                game_over_screen.restart(player, score, lives, asteroids, shots, asteroid_field)
                asteroid_field.start_wave(ASTEROIDS_PER_WAVE)
                is_game_over = False
            game_over_screen.draw(screen)
            pygame.display.flip()
            clock.tick(60)
            continue
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))
        for sprite in drawable:
            sprite.draw(screen)
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid_size = asteroid.get_size()
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    explosion_sound.play()
                    score.add_asteroid_points(asteroid_size)
        if not in_transition and asteroid_field.is_wave_spawned() and len(asteroids) == 0:
            in_transition = True
            transition_stage = 1
            transition_timer = LEVEL_MESSAGE_1_DURATION
        if in_transition:
            transition_timer -= dt
            transition_blink_timer += dt
            if transition_blink_timer >= TRANSITION_BLINK_INTERVAL:
                transition_blink_timer = 0.0
                transition_message_visible = not transition_message_visible
            if transition_stage == 1:
                message = "More asteroids incoming!"
            elif transition_stage == 2:
                message = "Get Ready!"
            else:
                raise ValueError(f"Unexpected transition_stage: {transition_stage}")
            if transition_timer <= 0:
                if transition_stage == 1:
                    transition_stage = 2
                    transition_timer = LEVEL_MESSAGE_2_DURATION
                elif transition_stage == 2:
                    level += 1
                    lives.gain_life()
                    asteroid_field.start_wave(ASTEROIDS_PER_WAVE)
                    player.respawn(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, grant_invincibility=False)
                    in_transition = False
                    transition_stage = 0
                else:
                    raise ValueError(f"Unexpected transition_stage: {transition_stage}")
            if transition_message_visible:
                text_surf = game_over_screen.title_font.render(message, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text_surf, text_rect)
        score.draw(screen)
        lives.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0
        if not in_transition:
            updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                if player.is_invincible():
                    continue

                log_event("player_hit")
                explosion_sound.play()
                lives.lose_life()

                if lives.is_game_over():
                    log_event("game_over")
                    is_game_over = True
                    break
                
                for s in shots:
                    s.kill()
                player.respawn(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                break
                


if __name__ == "__main__":
    main()
