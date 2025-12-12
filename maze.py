import random
from typing import List, Tuple, Set
from collections import deque


# Maze generation using recursive backtracking algorithm#
class Maze:
    def __init__(self, width: int, height: int):
        # Initialize maze with given dimensions (must be odd numbers)
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.generate()

    def generate(self):
        # Generate maze using recursive backtracking
        stack = [(1, 1)]
        visited = {(1, 1)}
        self.grid[1][1] = 0
        while stack:
            current = stack[-1]
            neighbors = self._get_unvisited_neighbors(current[0], current[1], visited)
            if neighbors:
                next_cell = random.choice(neighbors)
                wall_x = (current[0] + next_cell[0]) // 2
                wall_y = (current[1] + next_cell[1]) // 2
                self.grid[wall_y][wall_x] = 0
                self.grid[next_cell[1]][next_cell[0]] = 0
                visited.add(next_cell)
                stack.append(next_cell)
            else:
                stack.pop()
        self._create_loops()

    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        # Get unvisited neighbors that are 2 cells away
        neighbors = []
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 < nx < self.width - 1
                and 0 < ny < self.height - 1
                and (nx, ny) not in visited
            ):
                neighbors.append((nx, ny))
        return neighbors

    # Create more loops to improve maze quality
    def _create_loops(self):
        loop_count = (self.width * self.height) // 40
        for _ in range(loop_count):
            # Pick a random point that is a path, not a wall
            x = random.randrange(1, self.width - 1, 2)
            y = random.randrange(1, self.height - 1, 2)

            directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                wx, wy = x + dx, y + dy
                # Added a bounds check to prevent crashing
                if 0 < wx < self.width - 1 and 0 < wy < self.height - 1:
                    if self.grid[wy][wx] == 1:
                        self.grid[wy][wx] = 0
                        break

    def get_random_empty_cell(
        self, exclude: List[Tuple[int, int]] = None
    ) -> Tuple[int, int]:
        # Get a random empty cell position
        exclude = exclude or []
        empty_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0 and (x, y) not in exclude:
                    empty_cells.append((x, y))
        return random.choice(empty_cells) if empty_cells else (1, 1)

    def is_valid_position(self, x: int, y: int) -> bool:
        # Check if position is valid and not a wall
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == 0

    def find_path(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        # Find a path from start to end using BFS (breadth-first search)

        queue = deque([start])
        visited = {start}
        parent = {start: None}
        while queue:
            current = queue.popleft()
            if current == end:
                path = []
                while current:
                    path.append(current)
                    current = parent[current]
                return path[::-1]
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if next_pos not in visited and self.is_valid_position(
                    next_pos[0], next_pos[1]
                ):
                    visited.add(next_pos)
                    parent[next_pos] = current
                    queue.append(next_pos)
        return []
