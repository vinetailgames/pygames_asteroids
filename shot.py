from circleshape import CircleShape
from constants import SHOT_RADIUS
import pygame


class Shot(CircleShape):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, pygame.Color("white"), self.position, self.radius)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt