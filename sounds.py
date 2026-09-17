import pygame

pygame.mixer.init()

shoot_sound = pygame.mixer.Sound("sounds/laser.wav")
shoot_sound.set_volume(0.4)

explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
explosion_sound.set_volume(0.7)

def play_background_music():
    pygame.mixer.music.load("sounds/background.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)