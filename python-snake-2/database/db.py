from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        # Connect to local MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['snake_game_db']
        self.scores = self.db['scores']

    def add_score(self, name, score, grid_size=10):
        """Add a new score to the database."""
        score_data = {
            'name': name,
            'score': score,
            'grid_size': grid_size,
            'timestamp': datetime.utcnow()
        }
        return self.scores.insert_one(score_data)

    def get_all_scores(self):
        """Get all scores sorted by score in descending order."""
        return list(self.scores.find().sort('score', -1))

    def get_user_scores(self, name):
        """Get all scores for a specific user."""
        return list(self.scores.find({'name': name}).sort('score', -1))

    def update_user_score(self, name, new_score):
        """Update the highest score for a user if the new score is higher."""
        user_scores = self.get_user_scores(name)
        if not user_scores or new_score > user_scores[0]['score']:
            return self.add_score(name, new_score)
        return None

    def delete_user_scores(self, name):
        """Delete all scores for a specific user."""
        return self.scores.delete_many({'name': name})

    def get_leaderboard(self, limit=20):
        """Get top scores for the leaderboard."""
        return list(self.scores.find().sort('score', -1).limit(limit)) 