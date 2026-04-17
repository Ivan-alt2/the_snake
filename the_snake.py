from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр экрана
CENTER_OF_SCREEN = (SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)

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

# Цвет листика
LEAF_COLOR = (0, 128, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position: tuple = CENTER_OF_SCREEN,
        body_color: tuple | None = None
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объекты на экране."""
        raise NotImplementedError

    def draw_rect(self, position, color, border_color=BORDER_COLOR):
        """Отрисовывает прямоугольник."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс для яблока в игре 'Змейка'."""

    def __init__(self, snake_positions: list[tuple[int, int]] = [CENTER_OF_SCREEN]) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(snake_positions)
        
    def randomize_position(self, snake_positions):
        """Определяет случайную позицию для яблока на игровом поле."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self) -> None:
    """Отрисовывает яблоко на экране."""
    self.draw_rect(self.position, self.body_color)


class Snake(GameObject):
    """Змейка в игре."""

    def __init__(
        self,
        length: int = 1,
        direction: tuple[int, int] = RIGHT,
        body_color: tuple[int, int] = SNAKE_COLOR
    ) -> None:
        self.length = length
        self.body_color = body_color
        self.reset()
        self.direction = direction

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [CENTER_OF_SCREEN]
        self.position = self.positions[0]
        self.next_direction = None
        self.last = None


    def move(self) -> None:
    """Перемещает змейку на один сегмент в текущем направлении."""
    head_position = self.get_head_position()
    head_x, head_y = head_position

    direction_x, direction_y = self.direction

    new_head_x = (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
    new_head_y = (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
    new_head_position = (new_head_x, new_head_y)

    self.positions.insert(0, new_head_position)

    if len(self.positions) > self.length:
        self.last = self.positions[-1]
        self.positions.pop()

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]


    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_OF_SCREEN]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            self.draw_rect(position, self.body_color)

        # Отрисовка головы змейки
        self.draw_rect(self.positions[0], self.body_color)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш ."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция, инициализирующая игру и управляющая игровым циклом."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
