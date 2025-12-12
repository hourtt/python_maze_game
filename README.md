# Snake Maze Game

A Python-based arcade game that combines the mechanics of "Snake" with maze exploration, enemy evasion, and puzzle-solving. Built using the **Pygame** library.

## Project Structure & Code Flow

The project is organized into modular files to separate logic, rendering, and configuration. Here is the flow of execution:

### 1. Entry Point (`main.py`)
This file acts as the application bootloader.
* **Initialization:** It initializes Pygame, detects the monitor resolution, and sets up the display (attempting fullscreen first).
* **Game Instance:** It creates a single instance of the `Game` class.
* **Main Loop:** It runs the primary `while running:` loop which:
    1.  Calculates `dt` (Delta Time) to ensure movement speed is independent of framerate.
    2.  Captures inputs (Events) and passes them to `game.update()`.
    3.  Calls `game.draw()` to render the frame.

### 2. The Game Controller (`game.py`)
This class is the "brain" of the application, managing the state machine.
* **State Management:** It handles transitions between `MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`, and `WIN` states.
* **Level Generation:** Upon resetting the game:
    * It initializes the `Maze`.
    * It places the `Snake`, `Enemies`, and `Obstacles`.
    * **Validation:** It runs a critical function `is_level_solvable()` using BFS to ensure a valid path exists from the player to the goal before starting the level.
* **Update Cycle:** It processes collisions (Player vs. Wall/Enemy), tracks the timer, and calculates the score based on efficiency and difficulty.

### 3. The World Generator (`maze.py`)
* **Generation Algorithm:** Uses **Recursive Backtracking** to generate a perfect maze structure.
* **Loop Creation:** Applies a `_create_loops` method to remove random walls, ensuring the maze has multiple paths and isn't purely linear.
* **Pathfinding:** Provides a `find_path` method (using Breadth-First Search) which is utilized by Enemies to hunt the player.

### 4. Entities (The Actors)
* **`snake.py` (Player):**
    * Manages the snake's body segments as a list of coordinates `[(x,y), ...]`.
    * Handles movement logic and direction changes based on user input.
* **`enemy.py` (AI):**
    * **Proximity Logic:** Checks distance to player. If the player is within 10 tiles, it uses the Maze's pathfinding to hunt the player.
    * **Wander Logic:** If the player is far away, it moves in random valid directions.
* **`obstacle.py` (Hazard):**
    * Moves in a straight line until it hits a wall, then reverses direction (bounces).

### 5. Interface (`ui.py`)
* **Responsibility:** Handles all drawing operations to keep the logic files clean.
* **Components:**
    * **HUD:** Displays difficulty, moves, and the countdown timer.
    * **Minimap:** Renders a scaled-down version of the grid, showing walls, player position, and enemies in real-time.
    * **Screens:** Renders the Menu, Pause, Win, and Game Over overlays.

### 6. Configuration (`constants.py`)
* Contains all "Magic Numbers" for easy tuning.
* Includes settings for Colors (RGB), Frame Rate (FPS), and Difficulty presets (Grid sizes, Enemy counts, Speed).

---

## Game Features

* **Dynamic Maps:** Every level is procedurally generated and validated for solvability.
* **Intelligent AI:** Enemies switch between "Wandering" and "Hunting" states based on proximity.
* **Minimap System:** A tactical view to see the whole maze layout.
* **3 Difficulty Modes:**
    * *Easy:* Small maze, no time limit.
    * *Medium:* Medium maze, 4-minute limit.
    * *Hard:* Large maze (31x31), 3-minute limit, high enemy count.

---

## Installation & Requirements

### Prerequisites
* Python 3.x
* Pygame

### Setup
1.  Ensure Python is installed.
2.  Install the required dependency:
    ```bash
    pip install pygame
    ```
3.  Run the game:
    ```bash
    python main.py
    ```

---

## Controls

| Key | Action |
| :--- | :--- |
| **W / A / S / D** | Move Snake |
| **Arrow Keys** | Move Snake |
| **ESC** | Pause Game / Resume |
| **1, 2, 3** | Select Difficulty (in Menu) |
| **M** | Return to Menu (from Pause/End screens) |
| **Q** | Quit Game |

---

## Customization

You can tweak the game balance by editing `constants.py`:
* **Visuals:** Update the `COLORS` dictionary.
* **Performance:** Change `FPS` (Default is 120).
* **Gameplay:** Modify `SNAKE_MOVE_COOLDOWN` or `ENEMY_MOVE_COOLDOWN` to change game speed.
