from random import choice, randint

import pygame as pg

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Центр экрана
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
SPEED = 5

# Инициализация Pygame
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""
    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку."""
        if not color:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока."""
    def __init__(self, position=SCREEN_CENTER, body_color=APPLE_COLOR, full_cells=None):
        super().__init__(position, body_color)
        full_cells = full_cells or [SCREEN_CENTER]  # Начальная позиция змейки
        self.position = self.randomize_position(full_cells)

    def randomize_position(self, full_cells):
        """Определяет случайную позицию яблока на поле."""
        while True:
            pos = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if pos not in full_cells:
                self.position = pos
                break
        return self.position

    def draw(self):
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""
    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.last = []

    def update_direction(self):
        if self.next_direction:
            # Запрет движения в обратную сторону
            if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (
            (head[0] + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last.append(self.positions.pop())

    def draw(self):
        for pos in self.positions:
            self.draw_cell(pos)
        for pos in self.last:
            self.draw_cell(pos, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        return self.positions[0]


def handle_keys(snake):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    pg.init()
    snake = Snake()
    apple = Apple(full_cells=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()

        # Съели яблоко?
        if head == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        # Столкновение с собой?
        if head in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position(snake.positions)

        # Очистка экрана (можно заменить на отрисовку фона)
        screen.fill(BOARD_BACKGROUND_COLOR)
        
        apple.draw()
        snake.draw()
        
        pg.display.update()


if __name__ == '__main__':
    main()
