from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет гнилого яблока
WR_APPLE_COLOR = (128, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Центр игрового окна
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Базовый класс игрового объекта."""

    def __init__(
            self,
            position=SCREEN_CENTER,
            body_color=None
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объектов. Переопределяется в дочерних классах"""
        pass

    def draw_cell(self, position, color=None):
        """Метод отрисовывает одну ячейку."""
        if not color:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс игрового объекта - яблока."""

    def __init__(self, position=SCREEN_CENTER,
                 body_color=APPLE_COLOR, full_cells=None):
        super().__init__(position, body_color)
        # Передаём начальную позицию змейки, чтобы яблоко не появилось на ней
        self.position = self.randomize_position(full_cells or [SCREEN_CENTER])

    def randomize_position(self, full_cells):
        """Определяет случайную позицию яблока на поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in full_cells:
                break
        return self.position

    def draw(self):
        """Метод draw класса Apple."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Дочерний класс игрового объекта - змейка."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновляет позицию змейки."""
        head = self.get_head_position()
        pos_width, pos_height = head
        dir_width, dir_height = self.direction

        self.next_head = (
            (pos_width + dir_width * GRID_SIZE) % SCREEN_WIDTH,
            (pos_height + dir_height * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, self.next_head)
        # Удаляем последний элемент, если длина не увеличилась
        if len(self.positions) > self.length:
            self.last = [self.positions.pop()]
        else:
            self.last = []

    def draw(self):
        """Метод отрисовывает змейку на экране."""
        self.draw_cell(self.get_head_position())
        for position in self.last:
            self.draw_cell(position, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Запускает игру."""
    pg.init()
    snake = Snake()
    apple = Apple(full_cells=snake.positions)
    wrong_apple = Apple(full_cells=snake.positions, body_color=WR_APPLE_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()

        if head == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        elif head == wrong_apple.position:
            snake.get_wrong_apple()
            wrong_apple.position = wrong_apple.randomize_position(snake.positions)
            if snake.length >= 3:
                snake.length -= 1

        elif head in snake.positions[1:]:
            snake.reset()
            # Закрашиваем всю доску фоном при сбросе игры
            screen.fill(BOARD_BACKGROUND_COLOR)
            pg.display.update()

        apple.draw()
        wrong_apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
