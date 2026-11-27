import pygame
from settings import WIDTH, HEIGHT, WHITE, CYAN, RED, YELLOW, MUTED, DIFFS, MODE_BOT

CX = WIDTH // 2


def dim(color, factor):
    return tuple(int(c * factor) for c in color)


class UI:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 96)
        self.font_title = pygame.font.Font(None, 68)
        self.font_title.set_bold(True)
        self.font = pygame.font.Font(None, 34)
        self.font_small = pygame.font.Font(None, 25)

    def text(self, screen, text, font, color, center, shadow=False):
        if shadow:
            sh = font.render(text, True, dim(color, 0.35))
            screen.blit(sh, sh.get_rect(center=(center[0] + 3, center[1] + 3)))
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=center)
        screen.blit(surface, rect)
        return rect

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

    def draw_pause(self, screen):
        self.text(screen, "ПАУЗА", self.font_title, WHITE, (CX, HEIGHT // 2 - 20), True)
        self.text(screen, "ESC - ПРОДОЛЖИТЬ", self.font_small, MUTED, (CX, HEIGHT // 2 + 28))

    def draw_win(self, screen, game):
        left_won = game.winner == "left"
        if game.mode == MODE_BOT:
            title = "ТЫ ПОБЕДИЛ!" if left_won else "БОТ ВЫЙГРАЛ!"
        else:
            title = "ИГРОК 1 ПОБЕДИЛ!" if left_won else "ИГРОК 2 ПОБЕДИЛ!"
        color = CYAN if left_won else RED
        self.text(screen, title, self.font_title, color, (CX, HEIGHT // 2 - 25), True)
        self.text(screen, "НАЖМИТЕ R ДЛЯ НОВОЙ ИГРЫ", self.font_small, WHITE, (CX, HEIGHT // 2 + 25))