const API_BASE_URL = 'http://localhost:5005/api';
const GRID_SIZE = 10;
let gameInterval;
let gameActive = false;
let lastDirection = null;

// DOM Elements
const gameGrid = document.getElementById('game-grid');
const scoreElement = document.getElementById('score');
const finalScoreElement = document.getElementById('final-score');
const gameOverElement = document.getElementById('game-over');
const gameSetupElement = document.getElementById('game-setup');
const waitingMessageElement = document.getElementById('waiting-message');
const playerNameInput = document.getElementById('player-name');
const startGameButton = document.getElementById('start-game');
const playAgainButton = document.getElementById('play-again');
const leaderboardBody = document.getElementById('leaderboard-body');

// Initialize game grid
function initializeGrid() {
    gameGrid.innerHTML = '';
    for (let i = 0; i < GRID_SIZE * GRID_SIZE; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        gameGrid.appendChild(cell);
    }
}

// Update game display
function updateDisplay(gameState) {
    // Clear previous state
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.className = 'cell';
    });

    // Update snake
    gameState.snake_body.forEach((pos, index) => {
        const cellIndex = pos[1] * GRID_SIZE + pos[0];
        cells[cellIndex].classList.add(index === 0 ? 'snake-head' : 'snake-body');
    });

    // Update apple
    const applePos = gameState.apple_position;
    const appleIndex = applePos[1] * GRID_SIZE + applePos[0];
    cells[appleIndex].classList.add('apple');

    // Update score
    scoreElement.textContent = gameState.score;

    // Update waiting message visibility
    if (gameState.is_running && !gameState.has_started_moving) {
        waitingMessageElement.classList.remove('hidden');
    } else {
        waitingMessageElement.classList.add('hidden');
    }

    // Check game over
    if (gameState.game_over) {
        handleGameOver(gameState.score);
    }
}

// Start game
async function startGame() {
    const playerName = playerNameInput.value.trim() || 'GUEST';
    
    try {
        const response = await fetch(`${API_BASE_URL}/game/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: playerName }),
        });

        if (!response.ok) throw new Error('Failed to start game');

        gameSetupElement.classList.add('hidden');
        gameOverElement.classList.add('hidden');
        waitingMessageElement.classList.remove('hidden');
        gameActive = true;
        lastDirection = null;

        // Start game loop
        if (gameInterval) clearInterval(gameInterval);
        gameInterval = setInterval(gameLoop, 50); // Faster polling for smoother movement
    } catch (error) {
        console.error('Error starting game:', error);
        alert('Failed to start game. Please try again.');
    }
}

// Game loop
async function gameLoop() {
    if (!gameActive) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/game/state`);
        if (!response.ok) throw new Error('Failed to fetch game state');
        
        const gameState = await response.json();
        updateDisplay(gameState);
    } catch (error) {
        console.error('Error in game loop:', error);
    }
}

// Send move command
async function sendMove(direction) {
    if (!gameActive) return;

    try {
        const response = await fetch(`${API_BASE_URL}/game/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ direction }),
        });

        if (!response.ok) throw new Error('Failed to send move');
    } catch (error) {
        console.error('Error sending move:', error);
    }
}

// Update leaderboard
async function updateLeaderboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/scores/leaderboard`);
        if (!response.ok) throw new Error('Failed to fetch leaderboard');
        
        const scores = await response.json();
        leaderboardBody.innerHTML = '';
        
        scores.forEach((score, index) => {
            const row = document.createElement('tr');
            const date = new Date(score.timestamp).toLocaleDateString();
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${score.name}</td>
                <td>${score.score}</td>
                <td>${date}</td>
            `;
            leaderboardBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error updating leaderboard:', error);
    }
}

// Handle game over
async function handleGameOver(finalScore) {
    gameActive = false;
    clearInterval(gameInterval);
    finalScoreElement.textContent = finalScore;
    gameOverElement.classList.remove('hidden');
    waitingMessageElement.classList.add('hidden');
    
    // Submit score to database
    try {
        const response = await fetch(`${API_BASE_URL}/scores/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: playerNameInput.value.trim() || 'GUEST',
                score: finalScore
            }),
        });
        
        if (!response.ok) throw new Error('Failed to submit score');
        
        // Update leaderboard after submitting score
        updateLeaderboard();
    } catch (error) {
        console.error('Error submitting score:', error);
    }
}

// Event Listeners
startGameButton.addEventListener('click', startGame);
playAgainButton.addEventListener('click', () => {
    gameOverElement.classList.add('hidden');
    gameSetupElement.classList.remove('hidden');
    waitingMessageElement.classList.add('hidden');
});

// Keyboard controls
document.addEventListener('keydown', (event) => {
    if (!gameActive) return;

    const keyMap = {
        'ArrowUp': 'UP',
        'ArrowDown': 'DOWN',
        'ArrowLeft': 'LEFT',
        'ArrowRight': 'RIGHT',
        'w': 'UP',
        'W': 'UP',
        's': 'DOWN',
        'S': 'DOWN',
        'a': 'LEFT',
        'A': 'LEFT',
        'd': 'RIGHT',
        'D': 'RIGHT'
    };

    const direction = keyMap[event.key];
    if (direction) {
        event.preventDefault();
        sendMove(direction);
    }
});

// Initialize
initializeGrid();
updateLeaderboard(); 