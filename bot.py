import random
from settings import HEIGHT, DIFFS
class Bot:
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball
        self.difficulty = 1
        self.error = 0.0
    def new_error(self):
        d = DIFFS[self.difficulty]
        if random.random() < d["miss"]:
            return random.choice([-1, 1]) * random.randint(78, 120)
        return random.uniform(-d["error"], d["error"])
    def predict_y(self):
        ball = self.ball
        if ball.vx <= 0:
            return ball.rect.centery
        t = (self.paddle.rect.left - ball.rect.right) / ball.vx
        span = HEIGHT - ball.rect.height
        y = (ball.rect.top + ball.vy * t) % (2 * span)
        if y > span:
            y = 2 * span - y
        return y + ball.rect.height / 2
    def update(self):
        d = DIFFS[self.difficulty]
        if self.ball.vx > 0:
            target = (self.predict_y() if d["predict"] else self.ball.rect.centery) + self.error
            speed = d["speed"]
        else:
            target = HEIGHT / 2
            speed = d["speed"] * 0.5
        diff = target - self.paddle.rect.centery
        if abs(diff) > 6:
            step = max(1, round(min(speed, abs(diff))))
            self.paddle.move(step if diff > 0 else -step)

