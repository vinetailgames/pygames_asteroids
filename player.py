import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
from sounds import shoot_sound

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.invincible_timer = 0.0
        self.blink_timer = 0.0
        self.visible = True

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if not self.visible:
            return
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

    def respawn(self, x, y, grant_invincibility=True):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        if grant_invincibility:
            self.invincible_timer = INVINCIBILITY_DURATION
            self.blink_timer = 0.0
            self.visible = True
        else:
            self.invincible_timer = 0.0
            self.visible = True

    def is_invincible(self) -> bool:
        return self.invincible_timer > 0
        
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
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            self.blink_timer += dt
            if self.blink_timer >= INVINCIBILITY_BLINK_INTERVAL:
                self.visible = not self.visible
                self.blink_timer = 0.0
            if self.invincible_timer <= 0:
                self.visible = True