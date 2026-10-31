import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
from sounds import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.invincible_timer = 0.0
        self.blink_timer = 0.0
        self.visible = True
        self.is_thrusting = False
        self.base_image = pygame.image.load("textures/battleship.png").convert_alpha()

        battleship_sheet = pygame.image.load("textures/battleship_sheet.png")
        self.thrust_frames = []
        for i in range(THRUST_FRAME_COUNT):
            frame_rect = pygame.Rect(i * THRUST_FRAME_WIDTH, 0, THRUST_FRAME_WIDTH, THRUST_FRAME_HEIGHT)
            frame = battleship_sheet.subsurface(frame_rect).copy()
            self.thrust_frames.append(frame)
        self.current_frame_index = 0
        self.animation_timer = 0.0

        self.current_frame_index = 0
        self.animation_timer = 0.0

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

        if self.is_thrusting:
            current_image = self.thrust_frames[self.current_frame_index]
        else:
            current_image = self.base_image
        
        rotated_image = pygame.transform.rotate(current_image, -self.rotation)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate(self, dt):
        unit_vector = pygame.Vector2(0, -1)
        rotated_vector = unit_vector.rotate(self.rotation)
        self.velocity += rotated_vector * PLAYER_ACCELERATION * dt
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    def shoot(self) -> pygame.Vector2:
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        spawn_position = self.position + forward * (self.radius * 2.7)
        shot = Shot(spawn_position.x, spawn_position.y, 0)
        shot.velocity = forward * PLAYER_SHOOT_SPEED

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
            if not self.is_thrusting:
                thrust_sound.play(loops=-1)
                self.is_thrusting = True

            self.animation_timer += dt
            if self.animation_timer >= THRUST_ANIMATION_SPEED:
                self.animation_timer = 0.0
                self.current_frame_index = (self.current_frame_index + 1) % THRUST_FRAME_COUNT
        else:
            if self.is_thrusting:
                thrust_sound.stop()
                self.is_thrusting = False
            self.current_frame_index = 0
            self.animation_timer = 0.0
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