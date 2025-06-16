import pytest
from game_engine.engine import Snake, Apple, Position, Direction

def test_snake_initialization():
    start_pos = Position(5, 5)
    snake = Snake(start_pos, 10)
    assert len(snake.body) == 1
    assert snake.body[0] == start_pos
    assert snake.direction == Direction.RIGHT

def test_snake_movement():
    start_pos = Position(5, 5)
    snake = Snake(start_pos, 10)
    snake.move()
    assert snake.body[0] == Position(6, 5)  # Moved right

def test_snake_growth():
    start_pos = Position(5, 5)
    snake = Snake(start_pos, 10)
    initial_length = len(snake.body)
    snake.grow()
    snake.move()
    assert len(snake.body) == initial_length + 1

def test_snake_collision():
    start_pos = Position(5, 5)
    snake = Snake(start_pos, 10)
    # Move to wall
    for _ in range(5):
        snake.move()
    assert snake.check_collision()  # Should collide with wall

def test_apple_spawn():
    apple = Apple(10)
    assert apple.position is not None
    assert 0 <= apple.position.x < 10
    assert 0 <= apple.position.y < 10

def test_apple_spawn_not_on_snake():
    snake = Snake(Position(5, 5), 10)
    apple = Apple(10)
    apple.spawn(snake.body)
    assert apple.position not in snake.body 