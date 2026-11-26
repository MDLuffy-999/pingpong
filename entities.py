import pygame


class Paddle:
    def __init__(self, x, y, width=14, height=110, speed=7, color=(50, 220, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.color = color

    def move(self, direction, screen_height):
        """direction: -1 вверх, 1 вниз, 0 стоять."""
        self.rect.y += direction * self.speed
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(screen_height, self.rect.bottom)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)