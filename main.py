import pygame as py
import sys
from game import Game
from constants import FPS, COLORS


def main():
    # Main function to run the
    py.init()
    py.display.set_caption("Snake Maze Game")

    try:
        # Get the current monitor's resolution
        info = py.display.Info()
        # Set screen width & height
        screen_width, screen_height = info.current_w, info.current_h

        # Create a fullscreen display using the detected resolution
        screen = py.display.set_mode((screen_width, screen_height), py.FULLSCREEN)
    except py.error as e:
        print(f"Could not set fullscreen display: {e}")
        # Fallback to a default windowed size if fullscreen fails
        screen = py.display.set_mode((1280, 720))

    clock = py.time.Clock()

    # Create game instance
    game = Game(screen)

    # Game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
        events = (
            py.event.get()
        )  # Events can be anything from a mouse click to a keypress or the user closing the window
        for event in events:
            # event,type => an attribute of the event object that stores the type of event that occurred
            if event.type == py.KEYDOWN:
                if event.key == py.K_q:
                    if game.state in ["MENU", "PAUSED", "GAME_OVER", "WIN"]:
                        running = False

        game.update(dt, events)

        # Draw everything
        screen.fill(COLORS["BACKGROUND"])
        game.draw()

        py.display.flip()

    py.quit()
    sys.exit()


if __name__ == "__main__":
    main()
