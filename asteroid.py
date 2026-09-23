import pygame
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from logger import log_event
import random

class Asteroid(CircleShape):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, pygame.Color("white"), self.position, self.radius, LINE_WIDTH)

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