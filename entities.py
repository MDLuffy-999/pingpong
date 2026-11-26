import random
from collections import deque

import pygame

from settings import (
    WIDTH, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, BALL_SIZE,
    MAX_SPEED, SERVE_DELAY, CYAN, WHITE,
)

SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)


class Paddle:
    def init(self, x, color):
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