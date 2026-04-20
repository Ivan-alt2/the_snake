from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр экрана
CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
LEAF_COLOR = (0, 128, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Словарь направлений
DIRECTION_MAP = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT
}


class GameObject:
    """Игровой объект."""

    def __init__(self, position=CENTER_OF_SCREEN, body_color=None):
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
    """Предмет, который змейка может съесть."""

    def __init__(self, snake_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        # Если snake_positions не передан, использовать пустой список
        if snake_positions is None:
            snake_positions = []
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Определяет случайную позицию для яблока на игровом поле."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_rect(self.position, self.body_color)


class Snake(GameObject):
    """Змейка в игре."""

    def __init__(self, length=1, direction=None, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.length = length
        self.positions = [CENTER_OF_SCREEN]
        self.direction = direction if direction else choice(
            [UP, DOWN, LEFT, RIGHT])
        self.last = None

    def move(self):
        """Перемещает змейку на один сегмент в текущем направлении."""
        cur_head_pos = self.get_head_position()
        x, y = cur_head_pos

        new_head_pos = (x + self.direction[0] * GRID_SIZE,
                        y + self.direction[1] * GRID_SIZE)

        self.positions.insert(0, new_head_pos)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_OF_SCREEN]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            self.draw_rect(position, self.body_color)

    def update_direction(self, new_direction):
        """Обновляет направление змейки."""
        if (new_direction[0] + self.direction[0] != 0) or \
           (new_direction[1] + self.direction[1] != 0):
            self.direction = new_direction


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            new_direction = DIRECTION_MAP.get(event.key)
            if new_direction:
                snake.update_direction(new_direction)


def main():
    """Основная функция, инициализирующая игру и управляющая игровым циклом."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)  # Передайте начальную позицию змейки

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        head_position = snake.get_head_position()
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if head_position in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
