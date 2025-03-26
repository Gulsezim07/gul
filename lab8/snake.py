import pygame  
import sys
import copy
import random
import time

pygame.init()

# Параметры игры
scale = 15
score = 0
level = 0
SPEED = 10

food_x = 10
food_y = 10

# Окно
display = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Цвета
background_top = (0, 0, 50)
background_bottom = (0, 0, 0)
snake_colour = (255, 137, 0)
snake_head = (255, 247, 0)
font_colour = (255, 255, 255)
defeat_colour = (255, 0, 0)

# Класс змейки
class Snake:
    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.w = scale
        self.h = scale
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def reset(self):
        self.x = 500 / 2 - scale
        self.y = 500 / 2 - scale
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def show(self):
        for i in range(self.length):
            color = snake_colour if i != 0 else snake_head
            pygame.draw.rect(display, color, (self.history[i][0], self.history[i][1], self.w, self.h))

    def check_eaten(self):
        snake_rect = pygame.Rect(self.history[0][0], self.history[0][1], self.w, self.h)
        food_rect = pygame.Rect(food_x, food_y, scale, scale)
        return snake_rect.colliderect(food_rect)

    def grow(self):
        self.length += 1
        self.history.append(self.history[self.length - 2])

    def death(self):
        for i in range(1, self.length):
            if abs(self.history[0][0] - self.history[i][0]) < self.w and abs(self.history[0][1] - self.history[i][1]) < self.h and self.length > 2:
                return True

    def update(self):
        for i in range(self.length - 1, 0, -1):
            self.history[i] = copy.deepcopy(self.history[i - 1])
        self.history[0][0] += self.x_dir * scale
        self.history[0][1] += self.y_dir * scale

# Класс еды с картинкой
class Food:
    def __init__(self):
        self.image = pygame.image.load("apple.png")
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.new_location([])

    def new_location(self, snake_body):
        global food_x, food_y
        while True:
            food_x = random.randrange(1, int(500 / scale) - 1) * scale
            food_y = random.randrange(1, int(500 / scale) - 1) * scale
            if [food_x, food_y] not in snake_body:
                break

    def show(self):
        display.blit(self.image, (food_x, food_y))

# Отображение счёта и уровня
def show_score():
    font = pygame.font.SysFont(None, 20)
    text = font.render("Score: " + str(score), True, font_colour)
    display.blit(text, (scale, scale))

def show_level():
    font = pygame.font.SysFont(None, 20)
    text = font.render("Level: " + str(level), True, font_colour)
    display.blit(text, (90 - scale, scale))

# Основной цикл игры
def gameLoop():
    global score, level, SPEED

    snake = Snake(500 / 2, 500 / 2)
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if snake.y_dir == 0:
                    if event.key == pygame.K_UP:
                        snake.x_dir = 0
                        snake.y_dir = -1
                    if event.key == pygame.K_DOWN:
                        snake.x_dir = 0
                        snake.y_dir = 1
                if snake.x_dir == 0:
                    if event.key == pygame.K_LEFT:
                        snake.x_dir = -1
                        snake.y_dir = 0
                    if event.key == pygame.K_RIGHT:
                        snake.x_dir = 1
                        snake.y_dir = 0

        # Градиентный фон
        for y in range(500):
            color = (
                background_top[0] + (background_bottom[0] - background_top[0]) * y / 500,
                background_top[1] + (background_bottom[1] - background_top[1]) * y / 500,
                background_top[2] + (background_bottom[2] - background_top[2]) * y / 500
            )
            pygame.draw.line(display, color, (0, y), (500, y))

        # Отрисовка
        snake.show()
        snake.update()
        food.show()
        show_score()
        show_level()

        # Проверка поедания еды
        if snake.check_eaten():
            food.new_location(snake.history)
            score += random.randint(1, 5)
            snake.grow()
            if snake.length % 4 == 0:
                level += 1
                SPEED += 1

        # Проверка на смерть от хвоста
        if snake.death():
            score = 0
            level = 0
            font = pygame.font.SysFont(None, 100)
            text = font.render("Game Over!", True, defeat_colour)
            display.blit(text, (50, 200))
            pygame.display.update()
            time.sleep(3)
            snake.reset()
            food.new_location(snake.history)

        # Проверка на удар о стену
        if (snake.history[0][0] < 0 or snake.history[0][0] >= 500 or
            snake.history[0][1] < 0 or snake.history[0][1] >= 500):
            score = 0
            level = 0
            font = pygame.font.SysFont(None, 100)
            text = font.render("Game Over!", True, defeat_colour)
            display.blit(text, (50, 200))
            pygame.display.update()
            time.sleep(3)
            snake.reset()
            food.new_location(snake.history)

        pygame.display.update()
        clock.tick(SPEED)

gameLoop()
