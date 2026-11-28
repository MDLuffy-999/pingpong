import pygame
from settings import (
    WIDTH, HEIGHT, WHITE, CYAN, RED, YELLOW, MUTED, PANEL, BTN, BTN_HOVER,
    DIFFS, MODE_BOT, WINNING_SCORE,
)

CX = WIDTH // 2

MENU_PANEL = pygame.Rect(CX - 220, 40, 440, 540)
MENU_BUTTONS = {
    "bot": pygame.Rect(CX - 150, 235, 300, 52),
    "pvp": pygame.Rect(CX - 150, 301, 300, 52),
    "level": pygame.Rect(CX - 150, 367, 300, 52),
    "controls": pygame.Rect(CX - 150, 433, 300, 52),
    "quit": pygame.Rect(CX - 150, 499, 300, 52),
}
CONTROLS_BACK = pygame.Rect(CX - 125, 510, 250, 52)
PAUSE_RESUME = pygame.Rect(CX - 130, 280, 260, 52)
PAUSE_MENU = pygame.Rect(CX - 130, 348, 260, 52)
WIN_AGAIN = pygame.Rect(CX - 130, 355, 260, 52)
WIN_MENU = pygame.Rect(CX - 130, 423, 260, 52)


def dim(color, factor):
    return tuple(int(c * factor) for c in color)


class UI:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 96)
        self.font_title = pygame.font.Font(None, 68)
        self.font_title.set_bold(True)
        self.font = pygame.font.Font(None, 34)
        self.font_small = pygame.font.Font(None, 25)
        self.pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.pause_overlay.fill((4, 6, 14, 200))

    def text(self, screen, text, font, color, center, shadow=False):
        if shadow:
            sh = font.render(text, True, dim(color, 0.35))
            screen.blit(sh, sh.get_rect(center=(center[0] + 3, center[1] + 3)))
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=center)
        screen.blit(surface, rect)
        return rect
    
    def panel(self, screen, rect, color):
        pygame.draw.rect(screen, PANEL, rect, border_radius=16)
        pygame.draw.rect(screen, color, rect, 2, border_radius=16)
        pygame.draw.rect(screen, color, (rect.x + 28, rect.y, rect.width - 56, 4), border_radius=2)

    def button(self, screen, label, rect, mouse_pos, color=CYAN):
        hovered = rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, BTN_HOVER if hovered else BTN, rect, border_radius=12)
        pygame.draw.rect(screen, color, rect, 3 if hovered else 2, border_radius=12)
        pygame.draw.rect(screen, color, (rect.x + 12, rect.y + 13, 4, rect.height - 26), border_radius=2)
        self.text(screen, label, self.font, WHITE, rect.center)

    def draw_hud(self, screen, game):
        self.text(screen, str(game.left_score), self.font_big, CYAN, (CX - 90, 75), True)
        self.text(screen, str(game.right_score), self.font_big, RED, (CX + 90, 75), True)
        if game.mode == MODE_BOT:
            left_label, right_label = "ТЫ", "БОТ " + DIFFS[game.bot.difficulty]["name"]
        else:
            left_label, right_label = "ИГРОК 1", "ИГРОК 2"
        self.text(screen, left_label, self.font_small, MUTED, (CX - 90, 130))
        self.text(screen, right_label, self.font_small, MUTED, (CX + 90, 130))
        if game.mode == MODE_BOT:
            self.text(screen, "W / S или ВВЕРХ / ВНИЗ или МЫШЬ", self.font_small, CYAN, (200, HEIGHT - 38))
            self.text(screen, "ESC = ПАУЗА", self.font_small, MUTED, (WIDTH - 90, HEIGHT - 38))
        else:
            self.text(screen, "W / S", self.font_small, CYAN, (80, HEIGHT - 38))
            self.text(screen, "ВВЕРХ / ВНИЗ", self.font_small, RED, (WIDTH - 90, HEIGHT - 38))
            self.text(screen, "ESC = ПАУЗА", self.font_small, MUTED, (CX, HEIGHT - 38))
        if game.ball.serve_timer > 0:
            self.text(screen, "ПРИГОТОВЬТЕСЬ", self.font, YELLOW, (CX, HEIGHT // 2 - 60))
    
    def draw_menu(self, screen, difficulty):
        self.panel(screen, MENU_PANEL, CYAN)
        self.text(screen, "NEON", self.font_title, CYAN, (CX, 100), True)
        self.text(screen, "PING PONG", self.font_title, RED, (CX, 156), True)
        self.text(screen, "CLASSIC ARCADE", self.font_small, MUTED, (CX, 204))
        mouse = pygame.mouse.get_pos()
        self.button(screen, "ИГРА С БОТОМ", MENU_BUTTONS["bot"], mouse, CYAN)
        self.button(screen, "ДВА ИГРОКА", MENU_BUTTONS["pvp"], mouse, CYAN)
        self.button(screen, "СЛОЖНОСТЬ:  " + DIFFS[difficulty]["name"], MENU_BUTTONS["level"], mouse, YELLOW)
        self.button(screen, "УПРАВЛЕНИЕ", MENU_BUTTONS["controls"], mouse, WHITE)
        self.button(screen, "ВЫХОД", MENU_BUTTONS["quit"], mouse, RED)
        self.text(screen, f"Первый кто наберет {WINNING_SCORE} очков побеждает", self.font_small, MUTED, (CX, 566))

    def draw_controls(self, screen):
        self.text(screen, "КАК ИГРАТЬ", self.font_title, CYAN, (CX, 95), True)
        self.panel(screen, pygame.Rect(80, 150, 350, 215), CYAN)
        self.panel(screen, pygame.Rect(470, 150, 350, 215), RED)
        self.text(screen, "ИГРОК 1", self.font, CYAN, (255, 192))
        self.text(screen, "W  -  ВВЕРХ", self.font, WHITE, (255, 245))
        self.text(screen, "S  -  ВНИЗ", self.font, WHITE, (255, 285))
        self.text(screen, "против бота: стрелки и мышь", self.font_small, MUTED, (255, 336))
        self.text(screen, "ИГРОК 2", self.font, RED, (645, 192))
        self.text(screen, "СТРЕЛКА ВВЕРХ", self.font_small, WHITE, (645, 245))
        self.text(screen, "СТРЕЛКА ВНИЗ", self.font_small, WHITE, (645, 285))
        self.text(screen, "в игре с ботом это БОТ", self.font_small, MUTED, (645, 336))
        self.text(screen, "ESC  -  пауза / продолжить", self.font, WHITE, (CX, 410))
        self.text(screen, "Ракетка уменьшается при каждом ударе по мячу!", self.font_small, YELLOW, (CX, 458))
        self.button(screen, "В МЕНЮ", CONTROLS_BACK, pygame.mouse.get_pos(), WHITE)

    def draw_pause(self, screen):
        screen.blit(self.pause_overlay, (0, 0))
        self.panel(screen, pygame.Rect(CX - 170, 170, 340, 270), CYAN)
        self.text(screen, "ПАУЗА", self.font_title, WHITE, (CX, 225), True)
        mouse = pygame.mouse.get_pos()
        self.button(screen, "ПРОДОЛЖИТЬ", PAUSE_RESUME, mouse, CYAN)
        self.button(screen, "В МЕНЮ", PAUSE_MENU, mouse, RED)

    def draw_win(self, screen, game):
        left_won = game.winner == "left"
        if game.mode == MODE_BOT:
            title = "ВЫ ПОБЕДИЛИ!" if left_won else "БОТ ПОБЕДИЛ!"
        else:
            title = "ИГРОК 1 ПОБЕДИЛ!" if left_won else "ИГРОК 2 ПОБЕДИЛ!"
        color = CYAN if left_won else RED
        self.panel(screen, pygame.Rect(CX - 320, 150, 640, 350), color)
        self.text(screen, title, self.font_title, color, (CX, 218), True)
        self.text(screen, f"ИТОГОВЫЙ СЧЁТ   {game.left_score} : {game.right_score}", self.font, WHITE, (CX, 290))
        mouse = pygame.mouse.get_pos()
        self.button(screen, "ИГРАТЬ СНОВА", WIN_AGAIN, mouse, color)
        self.button(screen, "В МЕНЮ", WIN_MENU, mouse, WHITE)
