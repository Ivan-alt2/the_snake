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

    def drow_cell(self, position, color=None):
        """Метод отрисовывает одну ячейку."""
        if not color:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple (GameObject):
    """Дочерний класс игрового объекта - яблока."""

    def __init__(self, position=SCREEN_CENTER,
                 body_color=APPLE_COLOR, full_cells=None):
        super().__init__(position, body_color)
        full_cells = full_cells or []
        self.position = self.randomize_position(full_cells)

    def randomize_position(self, full_cells):
        """Определяет случайную позицию яблока на поле."""
        while True:
            self.position = (
                (randint(0, (GRID_WIDTH - 1)) * GRID_SIZE),
                (randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE)
            )
            if self.position not in full_cells:
                break
        return self.position

    def draw(self):
        """Метод draw класса Apple - из прекода."""
        self.drow_cell(self.position)


class Snake(GameObject):
    """Дочерний класс игрового объекта - змейка."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()  # Сделала, но теперь нельзя менять длину змеи в
        self.direction = RIGHT  # в начале игры
        self.next_direction = None

    def update_direction(self):
        """
        Метод обновления направления после нажатия на кнопку
        - из прекода.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Метод обновляет позицию змейки (координаты каждой секции), добавляя
        новую голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        # Получаем координаты новаой головы.
        head = self.get_head_position()
        pos_width, pos_height = head
        dir_width, dir_height = self.direction

        self.next_head = (
            (pos_width + dir_width * GRID_SIZE) % SCREEN_WIDTH,
            (pos_height + dir_height * GRID_SIZE) % SCREEN_HEIGHT
        )
        # Добавляем в список позиций координаты новой головы.
        self.positions.insert(0, self.next_head)
        # Эта перерменная передает в drow список ячеек, которые нужно затереть.
        # Также удаляем последний элемент, если длина змеи не увеличилась
        self.last = ([self.positions.pop()]
                     if len(self.positions) > self.length else self.last)

    def draw(self):
        """
        # Метод отрисовывает змейку на экране, затирая след
        - из прекода.
        """
        # Отрисовка головы змейки  - из прекода
        self.drow_cell(self.get_head_position())

        # Затирание последнего сегмента - из прекода, исправлена
        # теперь еще затирает хвост после reset() и после get_wrong_apple().
        for position in self.last:
            self.drow_cell(position, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """
        Метод возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, RIGHT, LEFT])

    def get_wrong_apple(self):
        """Метод описывает поведение змеи при поедании неправильного яблока"""
        if self.length >= 3:
            self.last += [self.positions[-2], self.positions[-1]]
            self.positions = self.positions[: -2]
        else:
            self.last += self.positions


def handle_keys(game_object):
    """Функция обработки действий пользователя - из прекода."""
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


def reset_and_new_apples(game_snake, game_apple, game_apple_wr):
    """Функция сбрасывает змейку и меняет позиции яблок."""
    game_snake.reset()
    game_apple.drow_cell(game_apple.position, BOARD_BACKGROUND_COLOR)
    game_apple_wr.drow_cell(game_apple_wr.position, BOARD_BACKGROUND_COLOR)
    game_apple.position = game_apple.randomize_position(game_snake.positions)
    game_apple_wr.position = (
        game_apple_wr.randomize_position(game_snake.positions)
    )


def main():
    """Запускает игру."""
    # Инициализация pg:
    pg.init()
    # Тут создаются экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)
    wrong_apple = Apple(snake.positions, WR_APPLE_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Проверка, съела ли змейка яблоко
        # (если да, увеличивает длину змейки и перемещает яблоко).
        head = snake.get_head_position()
        if head == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)
        # Проверка, съела ли змейка гнилое яблоко
        # (если да, уменьшает длину змейки и перемещает яблоко).
        elif head == wrong_apple.position:
            snake.get_wrong_apple()
            wrong_apple.position = (
                wrong_apple.randomize_position(snake.positions)
            )
            if snake.length >= 3:
                snake.length -= 1
            else:
                reset_and_new_apples(snake, apple, wrong_apple)
        # Проверка столкновения змейки с собой
        # (если столкновение, сброс игры при помощи метода reset()).
        elif head in snake.positions[1:]:
            snake.last += snake.positions[1:]
            reset_and_new_apples(snake, apple, wrong_apple)
        apple.draw()
        wrong_apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
