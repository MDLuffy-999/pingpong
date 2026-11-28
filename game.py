import pygame
from settings import (
    WIDTH, HEIGHT, FPS, WINNING_SCORE, PADDLE_WIDTH, PADDLE_SPEED, MOUSE_SPEED,
    BG, GRID, LINE, CYAN, RED, CYAN_DARK, RED_DARK, MODE_BOT, MODE_PVP, DIFFS,
)
from entities import Paddle, Ball
from controls import Controls
from bot import Bot
from ui import (
    UI, MENU_BUTTONS, CONTROLS_BACK, PAUSE_RESUME, PAUSE_MENU, WIN_AGAIN, WIN_MENU,
)
MENU, CONTROLS, GAME, PAUSE, WIN = "menu", "controls", "game", "pause", "win"
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
        self.ui = UI()
        self.left = Paddle(40, CYAN)
        self.right = Paddle(WIDTH - 40 - PADDLE_WIDTH, RED)
        self.ball = Ball()
        self.bot = Bot(self.right, self.ball)
        self.state = MENU
        self.mode = MODE_BOT
        self.mouse_control = False
        self.left_score = 0
        self.right_score = 0
        self.winner = None
        self.paused = False
        self.running = True
    def serve(self, direction=None):
        self.left.restore_size()
        self.right.restore_size()
        self.ball.reset(direction)
        self.bot.error = self.bot.new_error()
    def reset_match(self):
        self.left_score = 0
        self.right_score = 0
        self.winner = None
        self.left.reset()
        self.right.reset()
        self.serve()
    def start_match(self, mode):
        self.mode = mode
        self.mouse_control = False
        self.reset_match()
        self.state = GAME
    def handle_click(self, pos):
        if self.state == MENU:
            if MENU_BUTTONS["bot"].collidepoint(pos):
                self.start_match(MODE_BOT)
            elif MENU_BUTTONS["pvp"].collidepoint(pos):
                self.start_match(MODE_PVP)
            elif MENU_BUTTONS["level"].collidepoint(pos):
                self.bot.difficulty = (self.bot.difficulty + 1) % len(DIFFS)
            elif MENU_BUTTONS["controls"].collidepoint(pos):
                self.state = CONTROLS
            elif MENU_BUTTONS["quit"].collidepoint(pos):
                self.running = False
        elif self.state == CONTROLS:
            if CONTROLS_BACK.collidepoint(pos):
                self.state = MENU
        elif self.state == PAUSE:
            if PAUSE_RESUME.collidepoint(pos):
                self.state = GAME
            elif PAUSE_MENU.collidepoint(pos):
                self.state = MENU
        elif self.state == WIN:
            if WIN_AGAIN.collidepoint(pos):
                self.start_match(self.mode)
            elif WIN_MENU.collidepoint(pos):
                self.state = MENU
    def move_paddles(self):
        direction = self.controls.left(arrows_too=(self.mode == MODE_BOT))
        if direction != 0:
            self.mouse_control = False
        if self.mode == MODE_BOT and self.mouse_control:
            diff = pygame.mouse.get_pos()[1] - self.left.rect.centery
            if abs(diff) > 2:
                self.left.move(max(-MOUSE_SPEED, min(MOUSE_SPEED, diff)))
        else:
            self.left.move(direction * PADDLE_SPEED)
        if self.mode == MODE_PVP:
            self.right.move(self.controls.right() * PADDLE_SPEED)
        else:
            self.bot.update()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.controls.key_down(event)
                if event.key == pygame.K_ESCAPE or event.scancode in (pygame.KSCAN_ESCAPE, pygame.KSCAN_P):
                    if self.state == GAME:
                        self.state = PAUSE
                    elif self.state == PAUSE:
                        self.state = GAME
            elif event.type == pygame.KEYUP:
                self.controls.key_up(event)
            elif event.type == pygame.WINDOWFOCUSLOST:
                self.controls.clear()
                if self.state == GAME:
                    self.state = PAUSE
            elif event.type == pygame.MOUSEMOTION:
                if self.state == GAME and self.mode == MODE_BOT:
                    self.mouse_control = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)
    def update(self):
        if self.state != GAME:
            return
        self.move_paddles()
        self.ball.update()
        ball = self.ball
        if ball.rect.colliderect(self.left.rect) and ball.vx < 0:
            ball.bounce(self.left, 1)
            self.left.shrink()
            self.bot.error = self.bot.new_error()
        elif ball.rect.colliderect(self.right.rect) and ball.vx > 0:
            ball.bounce(self.right, -1)
            self.right.shrink()
        if ball.rect.left < 0:
            self.right_score += 1
            self.serve(direction=-1)
        elif ball.rect.right > WIDTH:
            self.left_score += 1
            self.serve(direction=1)
        if self.left_score >= WINNING_SCORE:
            self.winner = "left"
            self.state = WIN
        elif self.right_score >= WINNING_SCORE:
            self.winner = "right"
            self.state = WIN
    def draw_scene(self):
        self.left.draw(self.screen)
        self.right.draw(self.screen)
        self.ball.draw(self.screen)
        self.ui.draw_hud(self.screen, self)
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.state == MENU:
            self.ui.draw_menu(self.screen, self.bot.difficulty)
        elif self.state == CONTROLS:
            self.ui.draw_controls(self.screen)
        elif self.state == WIN:
            self.ui.draw_win(self.screen, self)
        else:
            self.draw_scene()
            if self.state == PAUSE:
                self.ui.draw_pause(self.screen)
        pygame.display.flip()
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

