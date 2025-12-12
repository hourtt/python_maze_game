# Window Frame rate (My laptop is 120 FPS, if your laptop is FPS is 60, you can simply disable the 120 FPS and enable the 60 FPS)
# Its not much different from the 120 FPS
# FPS = 60
FPS = 120

# Colors (RGB code)
COLORS = {
    "BACKGROUND": (136, 99, 85),  # Change the background color
    "WALL": (60, 60, 80),  # Change the wall color
    "PATH": (40, 40, 50),  # Change the path color
    "SNAKE_HEAD": (50, 200, 50),  # Change the snake head color
    "SNAKE_BODY": (30, 150, 30),  # Change the snake body color
    "GOAL": (255, 215, 0),  # Change the goal color
    "MAIN_DISPLAY_TEXT": (255, 215, 0),  # Change the main display color
    "ENEMY": (200, 50, 50),  # Change the enemy color
    "OBSTACLE": (150, 50, 150),  # Change the obstacle color
    "TEXT": (255, 255, 255),  # Change the text color
    "BUTTON": (70, 70, 90),  # Change the button color
    "BUTTON_HOVER": (90, 90, 110),  # Change the button hover color
    "HUD_BG": (30, 30, 40),  # Change the HUD background color
    "MINIMAP_WALL": (100, 100, 120),  # Change the minimap wall color
    "MINIMAP_PATH": (60, 60, 70),  # Change the minimap path color
    "MINIMAP_PLAYER": (100, 255, 100),  # Change the minimap player color
    "MINIMAP_GOAL": (255, 255, 100),  # Change the minimap goal color
    "MINIMAP_ENEMY": (255, 100, 100),  # Change the minimap enemy color
}

# Difficulty settings
DIFFICULTIES = {
    "EASY": {
        "maze_size": (18, 18),  # customize the maze size
        "enemy_count": 2,  # customize the enemy count
        "enemy_speed": 50,  # customize the enemy speed
        "obstacle_count": 3,  # customize the obstacle count
        "time_limit": None,  # No time limit for easy mode
        "snake_speed": 150,  # customize the snake speed
    },
    "MEDIUM": {
        "maze_size": (21, 21),  # customize the maze size
        "enemy_count": 4,  # customize the enemy count
        "enemy_speed": 75,  # customize the enemy speed
        "obstacle_count": 5,  # customize the obstacle count
        "time_limit": 240,  # 4 minutes time limit
        "snake_speed": 180,  # customize the snake speed
    },
    "HARD": {
        "maze_size": (31, 31),  # customize the maze size
        "enemy_count": 6,  # customize the enemy count
        "enemy_speed": 100,  # customize the enemy speed
        "obstacle_count": 8,  # customize the obstacle count
        "time_limit": 180,  # 3 minutes time limit
        "snake_speed": 200,  # customize the snake speed
    },
}

# Game settings ( You can customize by your own)
SNAKE_LENGTH = 2  # Snake length
SNAKE_MOVE_COOLDOWN = (
    0.5  # Seconds between moves (The less the number, the faster the snake moves)
)
ENEMY_MOVE_COOLDOWN = (
    0.2  # Seconds between enemy moves (The less the number, the faster the enemy moves)
)
OBSTACLE_MOVE_COOLDOWN = 0.5  # Seconds between obstacle moves (The less the number, the faster the obstacle moves)

# UI settings (you can customize by your own)
HUD_HEIGHT = 100  # Height of the HUD area
MINIMAP_SIZE = 200  # Size of the minimap
BUTTON_WIDTH = 200  # Width of buttons
BUTTON_HEIGHT = 50  # Height of buttons
FONT_SIZE = 24  # General font size
TITLE_FONT_SIZE = 48  # Title font size
SMALL_FONT_SIZE = 18  # Small font size
MEDIUM_FONT_SIZE = 24  # Medium font size
