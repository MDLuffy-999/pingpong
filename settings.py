# Окно и игровой цикл
WIDTH, HEIGHT = 900, 600
FPS = 60
WINNING_SCORE = 5
MAX_SPEED = 11
SERVE_DELAY = 45

# Ракетки и мяч
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 110
PADDLE_SPEED = 7
BALL_SIZE = 20

# Цвета
BG = (11, 15, 28)
GRID = (19,27,48)
LINE = (44, 58, 92)
WHITE = (235, 245, 255)
CYAN = (50, 220, 255)
RED = (255, 85, 105)
YELLOW = (255, 205, 90)
MUTED = (145, 165, 190)
PANEL = (20, 28, 50)
BTN = (26, 36, 62)
BTN_HOVER = (40, 58, 94)
CYAN_DARK = (27, 121, 140)
RED_DARK = (140, 46, 57)

# Уменьшение ракетки
PADDLE_SHRINK_STEP = 6
MIN_PADDLE_HEIGHT = 30

# Бот и мышь
MOUSE_SPEED = 14
MODE_BOT = "bot"
MODE_PVP = "pvp"
DIFFS = [
    {"name": "Легкий", "speed": 4.0, "error": 50, "miss": 0.40, "predict": False},
    {"name": "Средний", "speed": 5.6, "error": 30, "miss": 0.22, "predict": False},
    {"name": "Тяжелый", "speed": 7.0, "error": 15, "miss": 0.10, "predict": True},
]