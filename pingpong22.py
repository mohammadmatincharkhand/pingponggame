import pygame
import sys
import random

# تنظیمات اولیه
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong with Obstacles")

# رنگ‌ها
BG_COLOR = (30, 30, 60)
PADDLE_COLOR = (255, 165, 0)
BALL_COLORS = [(255, 0, 0), (0, 255, 0), (0, 200, 255), (255, 255, 0)]
TEXT_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (200, 0, 200)

# تنظیمات بازی
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 8
FPS = 60
FONT = pygame.font.SysFont("Arial", 30)
SCORE_FILE = "scores.txt"

# کلاس‌ها
class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= 6
        elif not up and self.rect.bottom < HEIGHT:
            self.rect.y += 6

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x, self.y = WIDTH//2, HEIGHT//2
        self.dx, self.dy = random.choice([-4, 4]), random.choice([-4, 4])
        self.color = random.choice(BALL_COLORS)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.y <= 0 or self.y >= HEIGHT:
            self.dy *= -1
            self.color = random.choice(BALL_COLORS)

    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), BALL_RADIUS)

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 20)
        self.hits = 0

    def draw(self):
        pygame.draw.rect(WIN, OBSTACLE_COLOR, self.rect)

# توابع
def draw_menu():
    WIN.fill(BG_COLOR)
    title = FONT.render("Ping Pong Game", True, TEXT_COLOR)
    start = FONT.render("Press SPACE to Start", True, TEXT_COLOR)
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    WIN.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2))
    pygame.display.update()

def draw_game(paddle1, paddle2, ball, score1, score2, obstacles):
    WIN.fill(BG_COLOR)
    pygame.draw.rect(WIN, PADDLE_COLOR, paddle1.rect)
    pygame.draw.rect(WIN, PADDLE_COLOR, paddle2.rect)
    ball.draw()
    for obs in obstacles:
        obs.draw()
    score_text = FONT.render(f"{score1} - {score2}", True, TEXT_COLOR)
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    pygame.display.update()

def save_score(score1, score2):
    try:
        with open(SCORE_FILE, "r") as f:
            scores = f.readlines()
    except FileNotFoundError:
        scores = []
    scores.append(f"{score1}-{score2}\n")
    scores = scores[-5:]
    with open(SCORE_FILE, "w") as f:
        f.writelines(scores)

def create_obstacles():
    obstacles = []
    for i in range(5):
        x = WIDTH//2 - 100 + i * 45
        y = HEIGHT//2 - 10
        obstacles.append(Obstacle(x, y))
    return obstacles

def main():
    clock = pygame.time.Clock()
    paddle1 = Paddle(20)
    paddle2 = Paddle(WIDTH - 30)
    ball = Ball()
    score1, score2 = 0, 0
    run = True
    in_menu = True
    obstacles = []

    while run:
        clock.tick(FPS)
        if in_menu:
            draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    in_menu = False
                    ball.reset()
                    obstacles = create_obstacles()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: paddle1.move(up=True)
            if keys[pygame.K_s]: paddle1.move(up=False)
            if keys[pygame.K_UP]: paddle2.move(up=True)
            if keys[pygame.K_DOWN]: paddle2.move(up=False)

            ball.move()

            # برخورد با پدال‌ها
            if paddle1.rect.collidepoint(ball.x - BALL_RADIUS, ball.y) or \
               paddle2.rect.collidepoint(ball.x + BALL_RADIUS, ball.y):
                ball.dx *= -1
                ball.color = random.choice(BALL_COLORS)

            # برخورد با موانع
            for obs in obstacles[:]:
                if obs.rect.collidepoint(ball.x, ball.y):
                    ball.dx *= -1
                    obs.hits += 1
                    ball.color = random.choice(BALL_COLORS)
                    if obs.hits >= 2:
                        obstacles.remove(obs)

            # امتیازدهی
            if ball.x < 0:
                score2 += 1
                ball.reset()
                obstacles = create_obstacles()
            elif ball.x > WIDTH:
                score1 += 1
                ball.reset()
                obstacles = create_obstacles()

            draw_game(paddle1, paddle2, ball, score1, score2, obstacles)

            if score1 >= 5 or score2 >= 5:
                save_score(score1, score2)
                score1, score2 = 0, 0
                in_menu = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()