from dataclasses import dataclass
from typing import List, Tuple, Optional
import random

@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self, start_pos: Position, grid_size: int):
        self.body = [start_pos]
        self.direction = Direction.RIGHT
        self.grid_size = grid_size
        self.growing = False

    def move(self) -> None:
        """Move the snake in the current direction."""
        head = self.body[0]
        new_head = Position(
            head.x + self.direction[0],
            head.y + self.direction[1]
        )
        self.body.insert(0, new_head)
        if not self.growing:
            self.body.pop()
        self.growing = False

    def change_direction(self, new_direction: Tuple[int, int]) -> None:
        """Change the snake's direction if the new direction is valid."""
        # Prevent 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow(self) -> None:
        """Make the snake grow on the next move."""
        self.growing = True

    def check_collision(self) -> bool:
        """Check if the snake has collided with itself or the walls."""
        head = self.body[0]
        # Check wall collision
        if (head.x < 0 or head.x >= self.grid_size or
            head.y < 0 or head.y >= self.grid_size):
            return True
        # Check self collision
        return head in self.body[1:]

    def will_hit_wall(self) -> bool:
        """Check if the next move will hit a wall."""
        head = self.body[0]
        next_x = head.x + self.direction[0]
        next_y = head.y + self.direction[1]
        return (next_x < 0 or next_x >= self.grid_size or
                next_y < 0 or next_y >= self.grid_size)

class Apple:
    def __init__(self, grid_size: int):
        self.grid_size = grid_size
        self.position = None
        self.spawn()

    def spawn(self, snake_body: Optional[List[Position]] = None) -> None:
        """Spawn the apple in a random position not occupied by the snake."""
        while True:
            self.position = Position(
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1)
            )
            if snake_body is None or self.position not in snake_body:
                break

def is_within_bounds(pos: Position, grid_size: int) -> bool:
    """Check if a position is within the grid bounds."""
    return (0 <= pos.x < grid_size and 0 <= pos.y < grid_size)

def check_collision(pos1: Position, pos2: Position) -> bool:
    """Check if two positions are the same."""
    return pos1 == pos2 