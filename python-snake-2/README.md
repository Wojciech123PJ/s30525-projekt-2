# Python Snake Game

A browser-based Snake game with MongoDB score tracking.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB Atlas:
- Create a MongoDB Atlas account
- Create a new cluster
- Get your connection string
- Create a `.env` file in the root directory with:
```
MONGODB_URI=your_mongodb_connection_string
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