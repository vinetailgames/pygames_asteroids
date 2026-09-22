import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS
from constants import LINE_WIDTH
from constants import PLAYER_TURN_SPEED
from constants import PLAYER_SPEED
from constants import PLAYER_SHOOT_SPEED
from constants import PLAYER_SHOOT_COOLDOWN_SECONDS
from constants import PLAYER_ACCELERATION
from constants import PLAYER_MAX_SPEED
from constants import PLAYER_FRICTION
from shot import Shot
from sounds import shoot_sound

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.velocity = pygame.Vector2(0, 0)

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, pygame.Color("white"), self.triangle())

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        self.velocity += rotated_vector * PLAYER_ACCELERATION * dt
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    def reverse(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        self.velocity -= rotated_vector * PLAYER_ACCELERATION * dt
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    def shoot(self) -> pygame.Vector2:
        shot = Shot(self.position.x, self.position.y, 0)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def respawn(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        
    def update(self, dt:float) -> None:
        keys = pygame.key.get_pressed()
        self.shot_cooldown_timer -= dt
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.accelerate(dt)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.reverse(dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown_timer > 0:
                pass
            else:
                shoot_sound.play()
                self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
        self.position += self.velocity * dt
        decay = max(0, 1 - PLAYER_FRICTION * dt)
        self.velocity *= decay
        self.wrap_position()