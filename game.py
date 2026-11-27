import pygame
from settings import (
    WIDTH, HEIGHT, FPS, WINNING_SCORE, PADDLE_WIDTH, PADDLE_SPEED,
    BG, GRID, LINE, CYAN, RED, CYAN_DARK, RED_DARK,
)
from entities import Paddle, Ball
from controls import Controls
def build_background():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill(BG)
    for x in range(0, WIDTH, 50):
        pygame.draw.line(surf, GRID, (x,0), (x, HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(surf, GRID, (0, y), (WIDTH, y))
    frame = pygame.Rect(10, 10, WIDTH - 20, HEIGHT - 20)
    pygame.draw.rect(surf, LINE, frame, 2, border_radius=16)
    # Верх и низ рамки: слева голубая, справа красная
    for y in (10, HEIGHT - 11):
        pygame.draw.line(surf, CYAN_DARK, (30, y), (WIDTH // 2 - 20, y), 3)
        pygame.draw.line(surf, RED_DARK, (WIDTH // 2 + 20, y), (WIDTH - 30, y), 3)
    for y in range(28, HEIGHT - 20, 28):
        pygame.draw.rect(surf, LINE, (WIDTH // 2 - 2, y, 4, 14), border_radius=2)
    return surf
class PingPongGame:
    def __init__(self):
        pygame.init()
        # SCALED делает картинку чёткой на Retina-экранах (без размытия)
        try:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=1)
        except Exception:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Neon Ping Pong")
        self.clock = pygame.time.Clock()
        self.background = build_background()
        self.controls = Controls()
        self.left = Paddle(40, CYAN)
        self.right = Paddle(WIDTH - 40 - PADDLE_WIDTH, RED)
        self.ball = Ball()
        self.left_score = 0
        self.right_score = 0
        self.winner = None
        self.running = True
    def reset_match(self):
        self.left_score = 0
        self.right_score = 0
        self.winner = None
        self.left.reset()
        self.right.reset()
        self.ball.reset()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.controls.key_down(event)
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.KEYUP:
                self.controls.key_up(event)
            elif event.type == pygame.WINDOWFOCUSLOST:
                self.controls.clear()
    def update(self):
        if self.winner:
            return
        self.left.move(self.controls.left() * PADDLE_SPEED)
        self.right.move(self.controls.right() * PADDLE_SPEED)
        self.ball.update()
        ball = self.ball
        if ball.rect.colliderect(self.left.rect) and ball.vx < 0:
            ball.bounce(self.left, 1)
            self.left.shrink()
        elif ball.rect.colliderect(self.right.rect) and ball.vx > 0:
            ball.bounce(self.right, -1)
            self.right.shrink()
        if ball.rect.left < 0:
            self.right_score += 1
            ball.reset(direction=-1)
        elif ball.rect.right > WIDTH:
            self.left_score += 1
            ball.reset(direction=1)
        if self.left_score >= WINNING_SCORE:
            self.winner = "left"
        elif self.right_score >= WINNING_SCORE:
            self.winner = "right"
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.left.draw(self.screen)
        self.right.draw(self.screen)
        self.ball.draw(self.screen)
        pygame.display.flip()
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

