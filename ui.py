import pygame as py
from constants import *


"""UI components for the Snake Maze Game"""


# This UI class manage all on-screen text and graphical elements
class UI:
    def __init__(self, screen, width, height):
        """Initialize UI components"""

        # Dynamic screen dimensions
        self.width = width
        self.height = height

        # Store the main screen surface
        self.screen = screen

        # Initialize fonts
        self.font = py.font.Font(None, FONT_SIZE)
        self.title_font = py.font.Font(None, TITLE_FONT_SIZE)
        self.small_font = py.font.Font(None, SMALL_FONT_SIZE)
        self.medium_font = py.font.Font(None, MEDIUM_FONT_SIZE)

    # Menu
    def draw_menu(self, difficulty):
        """Draw main menu"""
        # Title
        title = self.font.render(
            "SNAKE MAZE GAME", True, COLORS["TEXT"]
        )  # render() method is used to render the text into a surface object
        title_rect = title.get_rect(center=(self.width // 2, self.height * 0.25))
        self.screen.blit(
            title, title_rect
        )  # blit the text surface to main display surface

        # Subtitle
        subtitle = self.font.render(
            "Navigate the snake through the maze to reach the goal!",
            True,
            COLORS["TEXT"],
        )
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height * 0.3))
        self.screen.blit(subtitle, subtitle_rect)
        # Instructions
        instructions = [
            "Choose Difficulty:",
            "Press 1 > EASY (Small maze, no time limit)",
            "Press 2 > MEDIUM (Medium maze, 3 minute time limit)",
            "Press 3 > HARD (Large maze, 2 minute time limit)",
            "",
            "Controls:",
            "W/A/S/D or Arrow Keys - Move Snake",
            "ESC - Pause Game",
            "Q - Quit Game",
            "",
            "Avoid enemies" + " (red)" + " and obstacles" + " (purple)" + "!",
            "Reach the golden star to win!",
        ]

        y_offset = self.height * 0.35
        for line in instructions:
            if line.startswith("Choose Difficulty:") or line.startswith("Controls:"):
                text = self.font.render(line, True, COLORS["MAIN_DISPLAY_TEXT"])
            else:
                text = self.font.render(line, True, COLORS["TEXT"])
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

    # Hud
    def draw_hud(self, difficulty, moves, time_remaining=None):
        """Draw heads-up display"""
        # Background
        py.draw.rect(self.screen, COLORS["HUD_BG"], (0, 0, self.width, HUD_HEIGHT))

        # Difficulty
        diff_text = self.font.render(f"Difficulty: {difficulty}", True, COLORS["TEXT"])
        self.screen.blit(diff_text, (20, 20))

        # Moves
        moves_text = self.font.render(f"Moves: {moves}", True, COLORS["TEXT"])
        self.screen.blit(moves_text, (20, 50))

        # Timer
        if time_remaining is not None:
            minutes = int(time_remaining // 60)
            seconds = int(time_remaining % 60)
            timer_color = COLORS["TEXT"] if time_remaining > 30 else COLORS["ENEMY"]
            timer_text = self.font.render(
                f"Time: {minutes:02d}:{seconds:02d}", True, timer_color
            )
            timer_rect = timer_text.get_rect(center=(self.width // 2, 35))
            self.screen.blit(timer_text, timer_rect)

        # Controls reminder
        controls = "W/A/S/D: Move | ESC: Pause"
        controls_text = self.small_font.render(controls, True, COLORS["TEXT"])
        controls_rect = controls_text.get_rect(right=self.width - 20, top=20)
        self.screen.blit(controls_text, controls_rect)

    # Minimap
    def draw_minimap(self, maze, player_pos, goal_pos, enemies, obstacles):
        # Draw the minimap at the right corner
        minimap_x = self.width - MINIMAP_SIZE - 20
        minimap_y = HUD_HEIGHT + 20

        # Background
        py.draw.rect(
            self.screen,
            COLORS["HUD_BG"],
            (minimap_x - 5, minimap_y - 5, MINIMAP_SIZE + 10, MINIMAP_SIZE + 10),
        )

        # Calculate cell size for minimap
        cell_size = MINIMAP_SIZE // max(maze.width, maze.height)

        # Draw maze structure
        for y in range(maze.height):
            for x in range(maze.width):
                rect_x = minimap_x + x * cell_size
                rect_y = minimap_y + y * cell_size

                if maze.grid[y][x] == 1:  # Wall
                    py.draw.rect(
                        self.screen,
                        COLORS["MINIMAP_WALL"],
                        (rect_x, rect_y, cell_size, cell_size),
                    )
                else:  # Path
                    py.draw.rect(
                        self.screen,
                        COLORS["MINIMAP_PATH"],
                        (rect_x, rect_y, cell_size, cell_size),
                    )

        # Goal
        goal_x = minimap_x + goal_pos[0] * cell_size
        goal_y = minimap_y + goal_pos[1] * cell_size
        py.draw.rect(
            self.screen, COLORS["MINIMAP_GOAL"], (goal_x, goal_y, cell_size, cell_size)
        )

        # Draw enemies
        for enemy in enemies:
            enemy_x = minimap_x + enemy.x * cell_size
            enemy_y = minimap_y + enemy.y * cell_size
            py.draw.rect(
                self.screen,
                COLORS["MINIMAP_ENEMY"],
                (enemy_x, enemy_y, cell_size, cell_size),
            )

        # Draw player
        player_x = minimap_x + player_pos[0] * cell_size
        player_y = minimap_y + player_pos[1] * cell_size
        py.draw.rect(
            self.screen,
            COLORS["MINIMAP_PLAYER"],
            (player_x, player_y, cell_size, cell_size),
        )

        # Minimap
        label = self.small_font.render("MAP", True, COLORS["TEXT"])
        label_rect = label.get_rect(
            center=(minimap_x + MINIMAP_SIZE // 2, minimap_y - 15)
        )
        self.screen.blit(label, label_rect)

    def draw_pause_screen(self):
        """Draw pause screen overlay"""
        # Semi-transparent overlay
        overlay = py.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.title_font.render("PAUSED", True, COLORS["TEXT"])
        pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(pause_text, pause_rect)

        # Instructions
        resume_text = self.font.render("Press ESC to Resume", True, COLORS["TEXT"])
        resume_rect = resume_text.get_rect(
            center=(self.width // 2, self.height // 2 + 100)
        )
        self.screen.blit(resume_text, resume_rect)

        # Draw the "Menu" instruction
        menu_text = self.medium_font.render(
            "Press M for Main Menu", True, (200, 200, 200)
        )
        menu_rect = menu_text.get_rect(center=(self.width // 2, self.height // 2 + 60))
        self.screen.blit(menu_text, menu_rect)

        # Draw the "Quit" instruction
        menu_text = self.medium_font.render("Press Q for Quit", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
        self.screen.blit(menu_text, menu_rect)

    def draw_game_over(self):
        # Title
        game_over = self.title_font.render("GAME OVER", True, COLORS["ENEMY"])
        game_over_rect = game_over.get_rect(
            center=(self.width // 2, self.height // 2 - 50)
        )
        self.screen.blit(game_over, game_over_rect)

        # Options
        options = ["Press R to Retry", "Press M to Return to Menu", "Press Q to Quit"]

        y_offset = self.height // 2 + 20
        for option in options:
            text = self.font.render(option, True, COLORS["TEXT"])
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40

    def draw_win_screen(self, score):
        """Draw win screen"""
        # Title
        win_text = self.title_font.render("VICTORY!", True, COLORS["GOAL"])
        win_rect = win_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(win_text, win_rect)

        # Score
        score_text = self.title_font.render(f"Score: {score}", True, COLORS["TEXT"])
        score_rect = score_text.get_rect(
            center=(self.width // 2, self.height // 2 - 30)
        )
        self.screen.blit(score_text, score_rect)

        # Congratulations message
        congrats = self.font.render(
            "Congratulations! You found the goal!", True, COLORS["TEXT"]
        )
        congrats_rect = congrats.get_rect(
            center=(self.width // 2, self.height // 2 + 30)
        )
        self.screen.blit(congrats, congrats_rect)

        # Options
        options = [
            "Press R to Play Again",
            "Press M to Return to Menu",
            "Press Q to Quit",
        ]

        y_offset = self.height // 2 + 80
        for option in options:
            text = self.font.render(option, True, COLORS["TEXT"])
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 35
