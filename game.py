import pygame
from settings import (
    WIDHT, HEIGHT, FPS, WINNING_SCORE, PADDLE_WIDTH,
    BG, GRID, LINE, CYAN, RED, CYAN_DARK, RED_DARK,
)
from entities import Paddle, Ball
def build_background():
    surf = pygame.Surface((WIDHT, HEIGHT))
    surf.fill(BG)
    for x in range(0, WIDHT, 50):
        pygame.draw.line(surf, GRID, (x,0), (x, HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(surf, GRID, (0, y), (WIDHT, y))
    frame = pygame.Rect(10, 10, WIDHT - 20, HEIGHT - 20)
    pygame.draw.rect(surf, LINE, frame, 2, border_radius=16)
    # Верх и низ рамки: слева голубая, справа красная
    for y in (10, HEIGHT - 11):
        pygame.draw.line(surf, CYAN_DARK, (30, Y), (WIDHT // 2 - 20, y), 3)
        pygame.draw.line(surf, RED_DARK, (WIDHT // 2 + 20, y), (WIDHT - 30, y), 3)
    for y in range(28, HEIGHT - 20, 28):
        pygame.draw.rect(surf, LINE, (WIDTH // 2 - 2, y, 4, 14), border_radius=2)
    return surf
                