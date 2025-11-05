import pygame
import sys
import os

# تنظیمات اولیه
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Arial", 30)

# متغیرهای بازی
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 7
FPS = 60
SCORE_FILE = "scores.txt"

# کلاس‌ها
class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= 5
        elif not up and self.rect.bottom < HEIGHT:
            self.rect.y += 5

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x, self.y = WIDTH//2, HEIGHT//2
        self.dx, self.dy = 4, 4

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.y <= 0 or self.y >= HEIGHT:
            self.dy *= -1

    def draw(self):
        pygame.draw.circle(WIN, WHITE, (self.x, self.y), BALL_RADIUS)

# توابع
def draw_menu():
    WIN.fill(BLACK)
    title = FONT.render("Ping Pong Game", True, WHITE)
    start = FONT.render("Press SPACE to Start", True, WHITE)
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    WIN.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2))
    pygame.display.update()

def draw_game(paddle1, paddle2, ball, score1, score2):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, paddle1.rect)
    pygame.draw.rect(WIN, WHITE, paddle2.rect)
    ball.draw()
    score_text = FONT.render(f"{score1} - {score2}", True, WHITE)
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    pygame.display.update()

def save_score(score1, score2):
    scores = []
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            scores = f.readlines()
    scores.append(f"{score1}-{score2}\n")
    scores = scores[-5:]
    with open(SCORE_FILE, "w") as f:
        f.writelines(scores)

def main():
    clock = pygame.time.Clock()
    paddle1 = Paddle(20)
    paddle2 = Paddle(WIDTH - 30)
    ball = Ball()
    score1, score2 = 0, 0
    run = True
    in_menu = True

    while run:
        clock.tick(FPS)
        if in_menu:
            draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    in_menu = False
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

            # امتیازدهی
            if ball.x < 0:
                score2 += 1
                ball.reset()
            elif ball.x > WIDTH:
                score1 += 1
                ball.reset()

            draw_game(paddle1, paddle2, ball, score1, score2)

            if score1 >= 5 or score2 >= 5:
                save_score(score1, score2)
                score1, score2 = 0, 0
                in_menu = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()