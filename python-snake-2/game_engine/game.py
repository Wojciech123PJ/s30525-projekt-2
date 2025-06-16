from typing import Dict, List, Tuple, Optional
from .engine import Snake, Apple, Position, Direction
import time

class SnakeGame:
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.reset()
        self.last_update_time = time.time()
        self.update_interval = 0.3  # 300ms between updates
        self.has_started_moving = False

    def reset(self) -> None:
        """Reset the game to its initial state."""
        start_pos = Position(self.grid_size // 2, self.grid_size // 2)
        self.snake = Snake(start_pos, self.grid_size)
        self.apple = Apple(self.grid_size)
        self.score = 0
        self.game_over = False
        self.player_name = None
        self.last_update_time = time.time()
        self.pending_direction = None
        self.is_running = False
        self.has_started_moving = False

    def set_player_name(self, name: str) -> None:
        """Set the player's name."""
        self.player_name = name
        self.is_running = True

    def change_direction(self, direction: Tuple[int, int]) -> None:
        """Change the snake's direction."""
        if not self.game_over and self.is_running:
            # Prevent 180-degree turns
            current_direction = self.snake.direction
            if (direction[0] * -1, direction[1] * -1) != current_direction:
                self.snake.change_direction(direction)
                self.has_started_moving = True

    def update(self) -> None:
        """Update the game state."""
        if self.game_over or not self.is_running or not self.has_started_moving:
            return

        current_time = time.time()
        if current_time - self.last_update_time < self.update_interval:
            return

        self.last_update_time = current_time

        # Check if next move will hit wall
        if self.snake.will_hit_wall():
            self.game_over = True
            self.is_running = False
            return

        # Move the snake
        self.snake.move()

        # Check for self collision
        if self.snake.check_collision():
            self.game_over = True
            self.is_running = False
            return

        # Check for apple collision
        if self.snake.body[0] == self.apple.position:
            self.snake.grow()
            self.score += 1
            self.apple.spawn(self.snake.body)

    def get_game_state(self) -> Dict:
        """Get the current game state."""
        return {
            'snake_body': [(pos.x, pos.y) for pos in self.snake.body],
            'apple_position': (self.apple.position.x, self.apple.position.y),
            'score': self.score,
            'game_over': self.game_over,
            'player_name': self.player_name,
            'is_running': self.is_running,
            'has_started_moving': self.has_started_moving
        }

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_over 