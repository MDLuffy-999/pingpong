import pygame


class Controls:
    """Следит за нажатыми клавишами. Проверка по scancode (физическое положение
    клавиши), поэтому управление работает и на русской раскладке."""

    W = (pygame.KSCAN_W, pygame.K_w)
    S = (pygame.KSCAN_S, pygame.K_s)
    UP = (pygame.KSCAN_UP, pygame.K_UP)
    DOWN = (pygame.KSCAN_DOWN, pygame.K_DOWN)

    def __init__(self):
        self.held_scan = set()
        self.held_key = set()

    def key_down(self, event):
        self.held_scan.add(event.scancode)
        self.held_key.add(event.key)

    def key_up(self, event):
        self.held_scan.discard(event.scancode)
        self.held_key.discard(event.key)

    def clear(self):
        self.held_scan.clear()
        self.held_key.clear()

    def is_down(self, pair):
        scancode, keycode = pair
        return scancode in self.held_scan or keycode in self.held_key

    def left(self, arrows_too=False):
        """-1 вверх, 0 стоим, 1 вниз. arrows_too: стрелки тоже двигают левую ракетку."""
        direction = int(self.is_down(self.S)) - int(self.is_down(self.W))
        if arrows_too and direction == 0:
            direction = self.right()
        return direction

    def right(self):
        return int(self.is_down(self.DOWN)) - int(self.is_down(self.UP))