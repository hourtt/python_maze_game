import pygame
import random
from typing import Tuple
from constants import COLORS, ENEMY_MOVE_COOLDOWN


# Enemy class
class Enemy:
    def __init__(self, x: int, y: int, speed: float = 100):
        self.x, self.y = x, y
        self.move_cooldown = 0

    def update(self, dt: float, maze, player_pos: Tuple[int, int]):
        self.move_cooldown -= dt
        if self.move_cooldown <= 0:
            player_distance = abs(player_pos[0] - self.x) + abs(player_pos[1] - self.y)
            if player_distance < 10:
                path = maze.find_path((self.x, self.y), player_pos)
                if len(path) > 1:
                    self.x, self.y = path[1]
            else:
                directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                random.shuffle(directions)
                for dx, dy in directions:
                    new_x, new_y = self.x + dx, self.y + dy
                    if maze.is_valid_position(new_x, new_y):
                        self.x, self.y = new_x, new_y
                        break
            self.move_cooldown = ENEMY_MOVE_COOLDOWN

    def draw(self, screen, offset_x: int, offset_y: int, cell_size: int):
        x = offset_x + self.x * cell_size
        y = offset_y + self.y * cell_size
        pygame.draw.circle(
            screen,
            COLORS["ENEMY"],
            (x + cell_size // 2, y + cell_size // 2),
            cell_size // 2 - 2,
        )
        eye_size = max(1, cell_size // 8)
        pygame.draw.circle(
            screen, (255, 255, 255), (x + cell_size // 3, y + cell_size // 3), eye_size
        )
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (x + 2 * cell_size // 3, y + cell_size // 3),
            eye_size,
        )
