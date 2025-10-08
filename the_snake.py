"""Игра 'Змейка', реализованная с использованием Pygame.

Управляйте змейкой с помощью стрелок, собирайте яблоки, избегайте столкновений.
"""

import random

import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN, QUIT

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Змейка')


class GameObject:
    """Базовый класс для игровых объектов, содержащий позицию и цвет."""

    def __init__(self,
                 position: tuple[int, int] = (SCREEN_WIDTH // 2,
                                              SCREEN_HEIGHT // 2),
                 body_color: tuple[int, int, int] = BLACK) -> None:
        """Инициализирует объект с заданной позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Отрисовывает объект на указанной поверхности."""
        raise NotImplementedError('Метод draw должен быть в дочернем классе.')

    def draw_cell(self, position: tuple[int, int]) -> None:
        """Отрисовывает прямоугольную ячейку на заданной позиции."""
        rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)


class Apple(GameObject):
    """Класс для яблока, наследуемый от GameObject."""

    def __init__(self,
                 occupied_positions: list[tuple[int, int]] = None) -> None:
        """Инициализирует яблоко с красным цветом и случайной позицией."""
        super().__init__(body_color=RED)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self,
                           occupied_positions: list[tuple[int, int]]) -> None:
        """Перемещает яблоко в случайную незанятую позицию на сетке."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x, y)
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на указанной поверхности."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для змейки, наследуемый от GameObject.

    Управляет движением, ростом и отрисовкой змейки.
    """

    def __init__(self) -> None:
        """Инициализирует змейку с начальной позицией и направлением."""
        self.reset()

    def update_direction(self, new_direction: tuple[int, int] | None) -> None:
        """Обновляет направление движения змейки."""
        if new_direction is not None:
            opposite = (-self.direction[0], -self.direction[1])
            if new_direction != opposite:
                self.direction = new_direction
        self.next_direction = None

    def move(self) -> None:
        """Перемещает змейку в текущем направлении и обновляет её позиции."""
        head_x, head_y = self.get_head_position()
        new_head = (
            head_x + self.direction[0],
            head_y + self.direction[1]
        )
        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last_segment = self.positions.pop()
        else:
            self.last_segment = None

    def draw(self) -> None:
        """Отрисовывает змейку и стирает последний сегмент, если он есть."""
        for position in self.positions:
            self.draw_cell(position)

        if self.last_segment:
            rect = pygame.Rect(self.last_segment[0],
                               self.last_segment[1],
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BLACK, rect)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку до начального состояния."""
        super().__init__(body_color=GREEN)
        self.length = 1
        self.positions = [self.position]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = None
        self.last_segment = None


def handle_keys(snake: Snake) -> tuple[int, int] | None:
    """Обрабатывает нажатия клавиш для изменения направления змейки."""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                return UP
            elif event.key == K_DOWN:
                return DOWN
            elif event.key == K_LEFT:
                return LEFT
            elif event.key == K_RIGHT:
                return RIGHT
    return None


def main() -> None:
    """Основной цикл игры: инициализация, обновление и отрисовка."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        new_direction = handle_keys(snake)
        snake.next_direction = new_direction
        snake.update_direction(snake.next_direction)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()
