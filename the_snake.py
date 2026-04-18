import pygame

from random import randint
from typing import List, Optional, Tuple

# Константы для размеров поля и сетки
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP: Tuple[int, int] = (0, -1)
DOWN: Tuple[int, int] = (0, 1)
LEFT: Tuple[int, int] = (-1, 0)
RIGHT: Tuple[int, int] = (1, 0)

# Цвет фона — чёрный
BOARD_BACKGROUND_COLOR: Tuple[int, int, int] = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Tuple[int, int, int] = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Tuple[int, int, int] = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Tuple[int, int, int] = (0, 255, 0)

# Скорость движения змейки
SPEED: int = 20

class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position: Optional[Tuple[int, int]] = None,
        body_color: Optional[Tuple[int, int, int]] = None
    ) -> None:
        """Инициализирует объект на игровом поле."""
        self.position = position or (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color or (255, 255, 255)

    def draw(self, surface: pygame.Surface) -> None:
        """Абстрактный метод для отрисовки объекта на экране."""
        raise NotImplementedError

    def draw_cell(
        self,
        surface: pygame.Surface,
        position: Tuple[int, int],
        color: Optional[Tuple[int, int, int]] = None
    ) -> None:
        """Отрисовывает ячейку на экране."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color or self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко на игровом поле."""

    def __init__(self, snake_positions: List[Tuple[int, int]]) -> None:
        """Инициализирует яблоко на игровом поле."""
        super().__init__(None, APPLE_COLOR)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions: List[Tuple[int, int]]) -> None:
        """Устанавливает случайное положение яблока на игровом поле, избегая змейки."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(surface, self.position)

class Snake(GameObject):
    """Змейка в игре."""

    def __init__(self) -> None:
        """Инициализирует начальное состояние змейки."""
        start_position = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        super().__init__(start_position, SNAKE_COLOR)
        self.length: int = 1
        self.positions: List[Tuple[int, int]] = [self.position]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None

    def update_direction(self, new_direction: Tuple[int, int]) -> None:
        """Обновляет направление движения змейки, запрещая разворот на 180 градусов."""
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.next_direction = new_direction


    def move(self) -> None:
        """Обновляет позицию змейки: добавляет новую голову и удаляет последний сегмент, если длина не увеличилась."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        cur_head = self.positions[0]
        dx, dy = self.direction
        new_head = (
            (cur_head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (cur_head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        # Проверка столкновения с собой
        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            self.draw_cell(surface, position)

        head_position = self.positions[0]
        self.draw_cell(surface, head_position, SNAKE_COLOR)

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки (первый элемент в списке positions)."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние после столкновения с собой."""
        self.length = 1
        start_position = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        self.position = start_position
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None

def handle_keys(snake: Snake) -> None:
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)

def main() -> None:
    """Основная функция, управляющая игровым циклом."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN))
