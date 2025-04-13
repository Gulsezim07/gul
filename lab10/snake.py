import pygame
import sys
import random
import psycopg2

# Ввод имени игрока
username = input("Введите имя игрока: ")

# Подключение к базе
conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="12345",  
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Создание таблиц, если их нет
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS user_score (
    user_id INTEGER REFERENCES users(id),
    score INTEGER,
    level INTEGER
);
""")
conn.commit()

# Проверка: игрок уже есть?
cur.execute("SELECT id FROM users WHERE username = %s", (username,))
user = cur.fetchone()

if user:
    user_id = user[0]
    cur.execute("SELECT score, level FROM user_score WHERE user_id = %s", (user_id,))
    data = cur.fetchone()
    if data:
        print("⬅️ Ваши предыдущие результаты:")
        print(f"Счёт: {data[0]}, Уровень: {data[1]}")
        score, level = data
    else:
        score, level = 0, 0
else:
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
    score, level = 0, 0

# Игровые переменные
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = [10, 0]
food = {'pos': [0, 0], 'weight': 1, 'spawn_time': 0}
food_spawn = True
speed_increase = 0.1
food_counter = 0
fps = pygame.time.Clock()
paused = False

font = pygame.font.SysFont('arial', 20)

def insert_score():
    cur.execute("DELETE FROM user_score WHERE user_id = %s", (user_id,))
    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
                (user_id, score, level))
    conn.commit()

def check_collision(pos):
    return (
        pos[0] < 0 or pos[0] > SCREEN_WIDTH - 10 or
        pos[1] < 0 or pos[1] > SCREEN_HEIGHT - 10 or
        pos in snake_pos[1:]
    )

def get_random_food():
    global food_counter
    while True:
        pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
               random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
        if pos not in snake_pos:
            weight = 2 if food_counter >= 2 else 1
            food_counter = 0 if weight == 2 else food_counter + 1
            return {'pos': pos, 'weight': weight, 'spawn_time': pygame.time.get_ticks()}

def draw_ui():
    info = font.render(f"👤 {username}   Score: {score}   Level: {level}", True, WHITE)
    screen.blit(info, (10, 10))

    if paused:
        pause_text = font.render("⏸ Пауза - нажмите P для продолжения", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2))

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                insert_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_speed[1] == 0:
                    snake_speed = [0, -10]
                elif event.key == pygame.K_DOWN and snake_speed[1] == 0:
                    snake_speed = [0, 10]
                elif event.key == pygame.K_LEFT and snake_speed[0] == 0:
                    snake_speed = [-10, 0]
                elif event.key == pygame.K_RIGHT and snake_speed[0] == 0:
                    snake_speed = [10, 0]
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        insert_score()

        if not paused:
            snake_pos.insert(0, [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]])

            if check_collision(snake_pos[0]):
                insert_score()
                pygame.quit()
                sys.exit()

            if snake_pos[0] == food['pos']:
                score += food['weight']
                if score % 3 == 0:
                    level += 1
                food_spawn = True
            else:
                snake_pos.pop()

            if food_spawn:
                food = get_random_food()
                food_spawn = False

            if pygame.time.get_ticks() - food['spawn_time'] > 10000:
                food_spawn = True

        # Отрисовка
        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        food_color = RED if food['weight'] == 1 else ORANGE
        pygame.draw.rect(screen, food_color, pygame.Rect(food['pos'][0], food['pos'][1], 10, 10))

        draw_ui()
        pygame.display.flip()
        fps.tick(10 + level * speed_increase)

except SystemExit:
    insert_score()
    pygame.quit()
    cur.close()
    conn.close()
