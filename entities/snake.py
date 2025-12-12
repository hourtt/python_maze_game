import pygame
from typing import Tuple
from constants import COLORS, SNAKE_MOVE_COOLDOWN


class Snake:
    def __init__(self, x: int, y: int, length: int = 3):
        self.segments = [(x, y)]
        self.length = length
        self.direction = (0, 0)
        self.SNAKE_MOVE_COOLDOWN = 0
        self.speed = SNAKE_MOVE_COOLDOWN

    def update(self, dt: float, maze):
        self.SNAKE_MOVE_COOLDOWN -= dt
        if self.SNAKE_MOVE_COOLDOWN <= 0 and self.direction != (0, 0):
            head = self.segments[0]
            new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
            if maze.is_valid_position(new_head[0], new_head[1]):
                self.segments.insert(0, new_head)
                if len(self.segments) > self.length:
                    self.segments.pop()
                self.SNAKE_MOVE_COOLDOWN = self.speed
                return True
        return False

    # Snake movement
    def set_direction(self, direction: Tuple[int, int]):
        """Set snake movement direction, allowing reversal."""
        self.direction = direction

    def get_head(self) -> Tuple[int, int]:
        return self.segments[0]

    def draw(self, screen, offset_x: int, offset_y: int, cell_size: int):
        for i, segment in enumerate(self.segments):
            x = offset_x + segment[0] * cell_size
            y = offset_y + segment[1] * cell_size
            if i == 0:
                pygame.draw.rect(
                    screen,
                    COLORS["SNAKE_HEAD"],
                    (x + 2, y + 2, cell_size - 4, cell_size - 4),
                )
                eye_size = max(1, cell_size // 6)
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (x + cell_size // 3, y + cell_size // 3),
                    eye_size,
                )
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (x + 2 * cell_size // 3, y + cell_size // 3),
                    eye_size,
                )
            else:
                pygame.draw.rect(
                    screen,
                    COLORS["SNAKE_BODY"],
                    (x + 4, y + 4, cell_size - 8, cell_size - 8),
                )
