import pygame
import random
from constants import COLORS, OBSTACLE_MOVE_COOLDOWN


# Obstacle class
class Obstacle:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self.direction = random.choice([(0, -1), (1, 0), (0, 1), (-1, 0)])
        self.move_cooldown = OBSTACLE_MOVE_COOLDOWN

    def update(self, dt: float, maze):
        self.move_cooldown -= dt
        if self.move_cooldown <= 0:
            new_x, new_y = self.x + self.direction[0], self.y + self.direction[1]
            if maze.is_valid_position(new_x, new_y):
                self.x, self.y = new_x, new_y
            else:
                self.direction = (-self.direction[0], -self.direction[1])
            self.move_cooldown = OBSTACLE_MOVE_COOLDOWN

    def draw(self, screen, offset_x: int, offset_y: int, cell_size: int):
        x = offset_x + self.x * cell_size
        y = offset_y + self.y * cell_size
        pygame.draw.rect(
            screen, COLORS["OBSTACLE"], (x + 3, y + 3, cell_size - 6, cell_size - 6)
        )
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (x + 3, y + 3),
            (x + cell_size - 3, y + cell_size - 3),
            2,
        )
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (x + cell_size - 3, y + 3),
            (x + 3, y + cell_size - 3),
            2,
        )
