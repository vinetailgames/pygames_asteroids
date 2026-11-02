import pygame
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from logger import log_event
import random

class Asteroid(CircleShape):
    textures_loaded = False
    large_texture = None
    medium_texture = None
    small_texture = None

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        if not Asteroid.textures_loaded:
            Asteroid.large_texture = pygame.image.load("textures/large_asteroid.png").convert_alpha()
            Asteroid.medium_texture = pygame.image.load("textures/medium_asteroid.png").convert_alpha()
            Asteroid.small_texture = pygame.image.load("textures/small_asteroid.png").convert_alpha()
            Asteroid.textures_loaded = True

        base_texture = self._select_base_texture()
        diameter = int(self.radius * 2)
        scaled_texture = pygame.transform.scale(base_texture, (diameter, diameter))

        random_angle = random.uniform(0, 360)
        self.image = pygame.transform.rotate(scaled_texture, random_angle)

    def _select_base_texture(self):
        if self.radius >= ASTEROID_MIN_RADIUS * 3:
            return Asteroid.large_texture
        elif self.radius >= ASTEROID_MIN_RADIUS * 2:
            return Asteroid.medium_texture
        else:
            return Asteroid.small_texture

    def draw(self, screen: pygame.Surface) -> None:
        rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.wrap_position()

    def get_size(self) -> str:
        if self.radius <= ASTEROID_MIN_RADIUS:
            return "small"
        elif self.radius <= ASTEROID_MIN_RADIUS * 2:
            return "medium"
        else:
            return "large"

    def split(self) -> list["Asteroid"]:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_angle = random.uniform(20, 50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = 1.2 * self.velocity.rotate(random_angle)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2.velocity = 1.2 * self.velocity.rotate(-random_angle)