const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const gameOverElement = document.getElementById('gameOver');

const GRID_SIZE = 20;
const GRID_COUNT = 20;
const GAME_SPEED = 150; // Lower number = faster game

let snake = [{ x: 10, y: 10 }];
let food = null;
let direction = { x: 1, y: 0 };
let score = 0;
let gameLoop = null;
let gameOver = false;

function generateFood() {
    while (true) {
        const newFood = {
            x: Math.floor(Math.random() * GRID_COUNT),
            y: Math.floor(Math.random() * GRID_COUNT)
        };
        
        // Check if food spawns on snake
        if (!snake.some(segment => segment.x === newFood.x && segment.y === newFood.y)) {
            return newFood;
        }
    }
}

function drawSquare(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(
        x * (canvas.width / GRID_COUNT),
        y * (canvas.height / GRID_COUNT),
        (canvas.width / GRID_COUNT) - 1,
        (canvas.height / GRID_COUNT) - 1
    );
}

function draw() {
    // Clear canvas
    ctx.fillStyle = '#2c3e50';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw snake
    snake.forEach((segment, i) => {
        drawSquare(segment.x, segment.y, i === 0 ? '#27ae60' : '#2ecc71');
    });

    // Draw food
    if (food) {
        drawSquare(food.x, food.y, '#e74c3c');
    }
}

function update() {
    if (gameOver) return;

    // Calculate new head position
    const newHead = {
        x: (snake[0].x + direction.x + GRID_COUNT) % GRID_COUNT,
        y: (snake[0].y + direction.y + GRID_COUNT) % GRID_COUNT
    };

    // Check collision with self
    if (snake.some(segment => segment.x === newHead.x && segment.y === newHead.y)) {
        endGame();
        return;
    }

    // Move snake
    snake.unshift(newHead);

    // Check food collision
    if (food && newHead.x === food.x && newHead.y === food.y) {
        score += 1;
        scoreElement.textContent = `Score: ${score}`;
        food = generateFood();
    } else {
        snake.pop();
    }

    draw();
}

function endGame() {
    gameOver = true;
    clearInterval(gameLoop);
    gameOverElement.style.display = 'block';
}

function resetGame() {
    snake = [{ x: 10, y: 10 }];
    direction = { x: 1, y: 0 };
    score = 0;
    gameOver = false;
    food = generateFood();
    scoreElement.textContent = `Score: ${score}`;
    gameOverElement.style.display = 'none';
    
    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(update, GAME_SPEED);
}

// Handle keyboard input
document.addEventListener('keydown', (event) => {
    const key = event.key;
    
    if (gameOver && key.toLowerCase() === 'r') {
        resetGame();
        return;
    }

    const newDirection = {
        'ArrowUp': { x: 0, y: -1 },
        'ArrowDown': { x: 0, y: 1 },
        'ArrowLeft': { x: -1, y: 0 },
        'ArrowRight': { x: 1, y: 0 }
    }[key];

    if (newDirection && 
        !(newDirection.x === -direction.x && newDirection.y === -direction.y)) {
        direction = newDirection;
    }
});

// Start game
resetGame();
