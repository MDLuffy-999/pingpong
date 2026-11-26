import random
from collections import deque

import pygame

from settings import (
    WIDTH, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, BALL_SIZE,
    MAX_SPEED, SERVE_DELAY, CYAN, WHITE,
)

SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)


class Paddle:
    def __init__(self, x, color):
        self.color = color
        self.rect = pygame.Rect(x, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.reset()

    def reset(self):
        self.rect.centery = HEIGHT // 2

    def move(self, dy):
        self.rect.y += dy
        self.rect.clamp_ip(SCREEN_RECT)

    def draw(self, screen):
        r = self.rect
        pygame.draw.rect(screen, self.color, r, border_radius=6)
        pygame.draw.rect(screen, WHITE, (r.x + 3, r.y + 8, 3, r.height - 16), border_radius=2)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.trail = deque(maxlen=8)
        self.trail_sprites = []
        for i in range(8):
            r = 3 + i
            sprite = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(sprite, (*CYAN, 30 + i * 12), (r, r), r)
            self.trail_sprites.append(sprite)
        self.reset()

    def sync(self):
        self.rect.center = (round(self.x), round(self.y))

    def reset(self, direction=None):
        self.x, self.y = WIDTH / 2, HEIGHT / 2
        self.sync()
        self.vx = random.choice([-5, 5]) if direction is None else 5 * direction
        self.vy = random.choice([-4, -3, 3, 4])
        self.serve_timer = SERVE_DELAY
        self.trail.clear()

    def update(self):
        if self.serve_timer > 0:
            self.serve_timer -= 1
            return
        self.trail.append(self.rect.center)
        self.x += self.vx
        self.y += self.vy
        half = self.rect.height / 2
        if self.y - half <= 0:
            self.y = half
            self.vy = abs(self.vy)
        elif self.y + half >= HEIGHT:
            self.y = HEIGHT - half
            self.vy = -abs(self.vy)
        self.sync()

    def bounce(self, paddle, direction):
        """Отскок от ракетки: угол зависит от места попадания, скорость растёт."""
        speed = min(abs(self.vx) + 0.4, MAX_SPEED)
        offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        offset = max(-1.0, min(1.0, offset))
        self.vx = direction * speed
        self.vy = offset * 7
        if abs(self.vy) < 1:
            self.vy = random.choice([-1, 1])
        if direction > 0:
            self.rect.left = paddle.rect.right
        else:
            self.rect.right = paddle.rect.left
        self.x = float(self.rect.centerx)

    def draw(self, screen):
        for sprite, pos in zip(self.trail_sprites, self.trail):
            screen.blit(sprite, sprite.get_rect(center=pos))
        r = BALL_SIZE // 2
        pygame.draw.circle(screen, CYAN, self.rect.center, r + 2, 2)
        pygame.draw.circle(screen, WHITE, self.rect.center, r - 1)        
