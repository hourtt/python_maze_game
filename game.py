import pygame as py
from collections import deque
from maze import Maze
from ui import UI
from constants import *
from entities.snake import Snake
from entities.enemy import Enemy
from entities.obstacle import Obstacle


# Game class
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.ui = UI(screen, self.width, self.height)
        self.state = "MENU"
        self.difficulty = "EASY"
        self.game_reset()

        """Reset the game with current difficulty"""

    def game_reset(self):
        settings = DIFFICULTIES[self.difficulty]
        self.maze = Maze(settings["maze_size"][0], settings["maze_size"][1])

        # Define the available width & height
        available_width = self.width
        available_height = self.height - HUD_HEIGHT

        # Calculate cell size based on available space
        cell_size_w = available_width // self.maze.width
        cell_size_h = available_height // self.maze.height
        self.cell_size = min(cell_size_w, cell_size_h)

        # Calculate offset to center the maze
        maze_width = self.maze.width * self.cell_size
        maze_height = self.maze.height * self.cell_size
        self.maze_offset_x = (self.width - maze_width) // 2
        self.maze_offset_y = (self.height - maze_height - HUD_HEIGHT) // 2 + HUD_HEIGHT

        start_pos = self.maze.get_random_empty_cell()
        # Set the player's snake length, speed
        self.player = Snake(start_pos[0], start_pos[1], SNAKE_LENGTH)
        self.player.speed = settings["snake_speed"] / 1000.0
        self.goal = self.maze.get_random_empty_cell([start_pos])

        is_solvable = False
        max_retries = 100
        retries = 0
        while not is_solvable and retries < max_retries:
            self.enemies = []
            self.obstacles = []
            for _ in range(settings["enemy_count"]):
                pos = self.maze.get_random_empty_cell(
                    [start_pos, self.goal] + [(e.x, e.y) for e in self.enemies]
                )
                self.enemies.append(Enemy(pos[0], pos[1], settings["enemy_speed"]))
            for _ in range(settings["obstacle_count"]):
                pos = self.maze.get_random_empty_cell(
                    [start_pos, self.goal]
                    + [(e.x, e.y) for e in self.enemies]
                    + [(o.x, o.y) for o in self.obstacles]
                )
                self.obstacles.append(Obstacle(pos[0], pos[1]))
            if self.is_level_solvable():
                is_solvable = True
            retries += 1

        if not is_solvable:
            print(
                "Warning: Could not generate a provably solvable level after 100 tries."
            )

        self.time_elapsed = 0
        self.time_limit = settings["time_limit"]
        self.score = 0
        self.moves = 0

    def handle_input(self, events):
        # Menu State Input
        if self.state == "MENU":
            for event in events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_1:
                        self.start_game("EASY")
                    elif event.key == py.K_2:
                        self.start_game("MEDIUM")
                    elif event.key == py.K_3:
                        self.start_game("HARD")

        # Playing State Input (for pausing)
        elif self.state == "PLAYING":
            for event in events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        self.state = "PAUSED"

        # Paused State Input
        elif self.state == "PAUSED":
            for event in events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        self.state = "PLAYING"
                    elif event.key == py.K_m:
                        self.state = "MENU"

        # Game Over / Win State Input
        elif self.state in ["GAME_OVER", "WIN"]:
            for event in events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_r:
                        self.start_game(self.difficulty)
                    elif event.key == py.K_m:
                        self.state = "MENU"

        # Continuous key presses (movement)
        keys = py.key.get_pressed()
        if keys[py.K_w] or keys[py.K_UP]:
            self.player.set_direction((0, -1))
        elif keys[py.K_s] or keys[py.K_DOWN]:
            self.player.set_direction((0, 1))
        elif keys[py.K_a] or keys[py.K_LEFT]:
            self.player.set_direction((-1, 0))
        elif keys[py.K_d] or keys[py.K_RIGHT]:
            self.player.set_direction((1, 0))

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.game_reset()
        self.state = "PLAYING"

    def update(self, dt: float, events):
        """Update game state"""
        self.handle_input(events)
        if self.state != "PLAYING":
            return

        self.time_elapsed += dt
        if self.time_limit and self.time_elapsed >= self.time_limit:
            self.state = "GAME_OVER"
            return

        if self.player.update(dt, self.maze):
            self.moves += 1

        player_head = self.player.get_head()

        # Check for collisions with enemies and obstacles
        for entity in self.enemies + self.obstacles:
            if isinstance(entity, Enemy):
                entity.update(dt, self.maze, player_head)
            else:
                entity.update(dt, self.maze)

            if entity.x == player_head[0] and entity.y == player_head[1]:
                self.state = "GAME_OVER"
                return

        # Check if player reached the goal
        if player_head == self.goal:
            self.calculate_score()
            self.state = "WIN"

    def calculate_score(self):
        base_score = 1000
        difficulty_bonus = {"EASY": 1, "MEDIUM": 2, "HARD": 3}[self.difficulty]
        time_bonus = 0
        if self.time_limit:
            time_bonus = int((self.time_limit - self.time_elapsed) * 10)
        efficiency_bonus = max(0, 500 - self.moves * 2)
        self.score = base_score * difficulty_bonus + time_bonus + efficiency_bonus

    def draw(self):
        if self.state == "MENU":
            self.ui.draw_menu(self.difficulty)
        elif self.state in ["PLAYING", "PAUSED", "GAME_OVER", "WIN"]:
            self.draw_game_elements()
            if self.state == "PLAYING":
                time_rem = (
                    self.time_limit - self.time_elapsed if self.time_limit else None
                )
                self.ui.draw_hud(self.difficulty, self.moves, time_rem)
                self.ui.draw_minimap(
                    self.maze,
                    self.player.get_head(),
                    self.goal,
                    self.enemies,
                    self.obstacles,
                )
            elif self.state == "PAUSED":
                self.ui.draw_pause_screen()
            elif self.state == "GAME_OVER":
                self.ui.draw_game_over()
            elif self.state == "WIN":
                self.ui.draw_win_screen(self.score)

    def draw_game_elements(self):
        self.draw_maze()
        self.draw_goal()
        self.player.draw(
            self.screen, self.maze_offset_x, self.maze_offset_y, self.cell_size
        )
        for entity in self.enemies + self.obstacles:
            entity.draw(
                self.screen, self.maze_offset_x, self.maze_offset_y, self.cell_size
            )

    def draw_maze(self):
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = (
                    self.maze_offset_x + x * self.cell_size,
                    self.maze_offset_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                color = COLORS["WALL"] if self.maze.grid[y][x] == 1 else COLORS["PATH"]
                py.draw.rect(self.screen, color, rect)

    def draw_goal(self):
        import math

        x = self.maze_offset_x + self.goal[0] * self.cell_size
        y = self.maze_offset_y + self.goal[1] * self.cell_size
        pulse = abs(math.sin(py.time.get_ticks() * 0.003)) * 0.7 + 0.3
        color = (int(255 * pulse), int(215 * pulse), 0)
        center = (x + self.cell_size // 2, y + self.cell_size // 2)
        radius = self.cell_size // 3
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = radius if i % 2 == 0 else radius // 2
            points.append(
                (center[0] + r * math.cos(angle), center[1] + r * math.sin(angle))
            )
        py.draw.polygon(self.screen, color, points)

    def is_level_solvable(self) -> bool:
        start, end = self.player.get_head(), self.goal
        queue = deque([start])
        visited = {start}
        blocked = {(e.x, e.y) for e in self.enemies} | {
            (o.x, o.y) for o in self.obstacles
        }
        while queue:
            current = queue.popleft()
            if current == end:
                return True
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if (
                    next_pos not in visited
                    and self.maze.is_valid_position(*next_pos)
                    and next_pos not in blocked
                ):
                    visited.add(next_pos)
                    queue.append(next_pos)
        return False
