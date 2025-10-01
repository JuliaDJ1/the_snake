import pygame
import random

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
    """Содержит позицию и цвет объекта, а также метод для отрисовки."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), body_color=BLACK):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на указанной поверхности."""
        pass


class Apple(GameObject):
    """Класс для яблока, наследуемый от GameObject."""

    def __init__(self):
        super().__init__(body_color=RED)
        self.randomize_position()

    def randomize_position(self):
        """Перемещает яблоко в случайную позицию на сетке."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на указанной поверхности."""
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс для змейки, наследуемый от GameObject.

    Управляет движением, ростом и отрисовкой змейки.
    """

    def __init__(self):
        """Инициализирует змейку с начальной позицией и направлением."""
        super().__init__(body_color=GREEN)
        self.length = 1
        self.positions = [self.position]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = None
        self.last_segment = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки, если новое направление допустимо."""
        if new_direction is not None:
            opposite = (-self.direction[0], -self.direction[1])
            if new_direction != opposite:
                self.direction = new_direction
        self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении и обновляет её позиции."""
        head_x, head_y = self.get_head_position()
        new_head = (
            head_x + self.direction[0],
            head_y + self.direction[1]
        )
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last_segment = self.positions.pop()
        else:
            self.last_segment = None

    def draw(self, surface):
        """Отрисовывает змейку и стирает последний сегмент, если он есть."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

        if self.last_segment:
            rect = pygame.Rect(
                self.last_segment[0],
                self.last_segment[1],
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, BLACK, rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку до начального состояния."""
        self.__init__()


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления змейки.

    Args:
        snake: Объект змейки, направление которой обновляется.

    Returns:
        Кортеж с новым направлением или None, если направление не изменилось.
    """
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


def main():
    """Основной цикл игры: инициализация, обновление и отрисовка."""
    snake = Snake()
    apple = Apple()

    while True:
        new_direction = handle_keys(snake)
        snake.next_direction = new_direction
        snake.update_direction(snake.next_direction)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()