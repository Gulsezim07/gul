# Импорт библиотеки pygame
import pygame

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)  # Чёрный цвет для рисования
green = (34, 139, 34)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Основная функция

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15  # толщина линии при рисовании мышкой
    mode = white  # цвет по умолчанию
    last_pos = None  # последняя позиция мышки

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # Смена цвета по нажатию клавиш
                if event.key == pygame.K_r:
                    mode = red
                elif event.key == pygame.K_g:
                    mode = green
                elif event.key == pygame.K_b:
                    mode = blue
                elif event.key == pygame.K_y:
                    mode = yellow
                elif event.key == pygame.K_k:
                    mode = black  # рисовать чёрным цветом
                elif event.key == pygame.K_BACKSPACE:
                    screen.fill(white)  # очистка экрана

                # Рисование фигур по нажатию клавиш
                elif event.key == pygame.K_w:
                    drawRectangle(screen, pygame.mouse.get_pos(), 200, 100, mode)
                elif event.key == pygame.K_c:
                    drawCircle(screen, pygame.mouse.get_pos(), mode)
                elif event.key == pygame.K_t:
                    drawRightTriangle(screen, pygame.mouse.get_pos(), 100, mode)
                elif event.key == pygame.K_e:
                    drawEquilateralTriangle(screen, pygame.mouse.get_pos(), 100, mode)
                elif event.key == pygame.K_h:
                    drawRhombus(screen, pygame.mouse.get_pos(), 80, 60, mode)

            # Рисование мышкой (при зажатой ЛКМ)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                last_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if last_pos is not None:
                    start_pos = last_pos
                    end_pos = pygame.mouse.get_pos()
                    drawLineBetween(screen, start_pos, end_pos, radius, mode)
                    last_pos = end_pos

        pygame.display.flip()
        clock.tick(60)

# Функция для рисования линии между двумя точками (при движении мышкой)
def drawLineBetween(screen, start, end, width, color_mode):
    color = color_mode
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

# Рисование прямоугольника
def drawRectangle(screen, mouse_pos, w, h, color):
    x = mouse_pos[0]
    y = mouse_pos[1]
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, 3)  # параметр 3 — толщина рамки

# Рисование круга
def drawCircle(screen, mouse_pos, color):
    x = mouse_pos[0]
    y = mouse_pos[1]
    pygame.draw.circle(screen, color, (x, y), 100, 3)  # радиус 100, толщина 3

# Рисование прямоугольного треугольника (правого)
def drawRightTriangle(screen, pos, size, color):
    x, y = pos
    points = [(x, y), (x + size, y), (x, y + size)]
    pygame.draw.polygon(screen, color, points, 3)

# Рисование равностороннего треугольника
def drawEquilateralTriangle(screen, pos, size, color):
    x, y = pos
    height = (3 ** 0.5 / 2) * size
    points = [
        (x, y),
        (x + size, y),
        (x + size / 2, y - height)
    ]
    pygame.draw.polygon(screen, color, points, 3)

# Рисование ромба
def drawRhombus(screen, pos, w, h, color):
    x, y = pos
    points = [
        (x, y - h // 2),
        (x + w // 2, y),
        (x, y + h // 2),
        (x - w // 2, y)
    ]
    pygame.draw.polygon(screen, color, points, 3)

# Запуск приложения
main()
