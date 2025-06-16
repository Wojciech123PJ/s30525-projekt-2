from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .game import SnakeGame
from database.db import Database
import json
import os
import threading
import time

# Get the absolute path to the ui directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = os.path.join(BASE_DIR, 'ui')

app = Flask(__name__)
CORS(app)

# Initialize game and database
game = SnakeGame()
db = Database()

# Game update thread
def game_update_thread():
    """Background thread to update game state."""
    while True:
        game.update()
        time.sleep(0.05)  # 50ms sleep to prevent excessive CPU usage

# Start the game update thread
update_thread = threading.Thread(target=game_update_thread, daemon=True)
update_thread.start()

@app.route('/')
def index():
    return send_from_directory(UI_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(UI_DIR, path)

@app.route('/api/game/start', methods=['POST'])
def start_game():
    data = request.get_json()
    name = data.get('name', 'GUEST')
    game.reset()
    game.set_player_name(name)
    return jsonify(game.get_game_state())

@app.route('/api/game/move', methods=['POST'])
def move():
    data = request.get_json()
    direction = data.get('direction')
    
    # Map direction strings to tuples
    direction_map = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }
    
    if direction and direction in direction_map:
        game.change_direction(direction_map[direction])
    
    return jsonify(game.get_game_state())

@app.route('/api/game/state', methods=['GET'])
def get_state():
    return jsonify(game.get_game_state())

@app.route('/api/scores/leaderboard', methods=['GET'])
def get_leaderboard():
    scores = db.get_leaderboard(limit=20)
    return jsonify([{
        'name': score['name'],
        'score': score['score'],
        'timestamp': score['timestamp'].isoformat()
    } for score in scores])

@app.route('/api/scores/add', methods=['POST'])
def add_score():
    if not game.is_game_over():
        return jsonify({'error': 'Game is not over'}), 400
    
    data = request.get_json()
    name = data.get('name', game.player_name)
    score = game.score
    
    if not name:
        return jsonify({'error': 'Player name is required'}), 400
    
    db.add_score(name, score)
    return jsonify({'message': 'Score added successfully'})

@app.route('/api/scores/user/<name>', methods=['GET'])
def get_user_scores(name):
    scores = db.get_user_scores(name)
    return jsonify([{
        'score': score['score'],
        'timestamp': score['timestamp'].isoformat()
    } for score in scores])

if __name__ == '__main__':
    app.run(debug=True, port=5005) 