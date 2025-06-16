# Python Snake Game

A browser-based Snake game with MongoDB score tracking.

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

1. Start the Flask server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:5005
```

## Game Controls

- Use Arrow Keys or WASD to control the snake
- Press Space to start a new game
- Enter your name before starting the game
- Your score will be saved automatically when the game ends

## Project Structure

- `database/`: MongoDB connection and models
- `game_engine/`: Core game logic and Flask server
- `tests/`: Unit tests
- `ui/`: Frontend files (HTML, CSS, JavaScript) 
