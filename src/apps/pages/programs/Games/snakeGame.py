import streamlit as st
import streamlit.components.v1 as components


def snakeGame():
  st.title("Snake Game")

  game_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            canvas { 
                background: black;
                display: block;
                margin: 0 auto;
            }
        </style>
    </head>
    <body>
        <canvas id="gameCanvas" width="600" height="600"></canvas>
        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const gridSize = 30;
            const tileCount = canvas.width / gridSize;

            let speed = 7;
            let score = 0;

            let snake = [
                {x: 10, y: 10}
            ];

            let food = {
                x: Math.floor(Math.random() * tileCount),
                y: Math.floor(Math.random() * tileCount)
            };

            let velocityX = 0;
            let velocityY = 0;

            document.addEventListener('keydown', changeDirection);

            function changeDirection(event) {
                const A_KEY = 65;
                const D_KEY = 68;
                const W_KEY = 87;
                const S_KEY = 83;

                const keyPressed = event.keyCode;
                const goingUp = velocityY === -1;
                const goingDown = velocityY === 1;
                const goingRight = velocityX === 1;
                const goingLeft = velocityX === -1;

                if (keyPressed === A_KEY && !goingRight) {
                    velocityX = -1;
                    velocityY = 0;
                }
                if (keyPressed === W_KEY && !goingDown) {
                    velocityX = 0;
                    velocityY = -1;
                }
                if (keyPressed === D_KEY && !goingLeft) {
                    velocityX = 1;
                    velocityY = 0;
                }
                if (keyPressed === S_KEY && !goingUp) {
                    velocityX = 0;
                    velocityY = 1;
                }
            }

            function drawGame() {
                moveSnake();

                let result = isGameOver();
                if (result) {
                    return;
                }

                clearScreen();
                checkFoodCollision();
                drawFood();
                drawSnake();
                drawScore();

                setTimeout(drawGame, 1000/speed);
            }

            function isGameOver() {
                let gameOver = false;

                if (snake[0].x < 0 || snake[0].x >= tileCount || snake[0].y < 0 || snake[0].y >= tileCount) {
                    gameOver = true;
                }

                for (let i = 1; i < snake.length; i++) {
                    if (snake[i].x === snake[0].x && snake[i].y === snake[0].y) {
                        gameOver = true;
                    }
                }

                if (gameOver) {
                    ctx.fillStyle = "white";
                    ctx.font = "50px Verdana";
                    ctx.fillText("Game Over!", canvas.width / 6.5, canvas.height / 2);
                    ctx.font = "30px Verdana";
                    ctx.fillText("Press Space to Restart", canvas.width / 4, canvas.height / 1.5);
                }

                return gameOver;
            }

            function drawScore() {
                ctx.fillStyle = "white";
                ctx.font = "30px Verdana";
                ctx.fillText("Score: " + score, canvas.width - 150, 40);
            }

            function clearScreen() {
                ctx.fillStyle = "black";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            function drawSnake() {
                ctx.fillStyle = "lime";
                for (let i = 0; i < snake.length; i++) {
                    ctx.fillRect(snake[i].x * gridSize, snake[i].y * gridSize, gridSize - 2, gridSize - 2);
                }
            }

            function moveSnake() {
                const head = {
                    x: snake[0].x + velocityX,
                    y: snake[0].y + velocityY
                };

                snake.unshift(head);
                if (!eatFood()) {
                    snake.pop();
                }
            }

            function drawFood() {
                ctx.fillStyle = "red";
                ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
            }

            function eatFood() {
                if (snake[0].x === food.x && snake[0].y === food.y) {
                    food = {
                        x: Math.floor(Math.random() * tileCount),
                        y: Math.floor(Math.random() * tileCount)
                    };
                    score += 10;
                    return true;
                }
                return false;
            }

            function checkFoodCollision() {
                if (snake[0].x === food.x && snake[0].y === food.y) {
                    food = {
                        x: Math.floor(Math.random() * tileCount),
                        y: Math.floor(Math.random() * tileCount)
                    };
                    score += 10;
                }
            }

            document.addEventListener('keydown', function(event) {
                if (event.keyCode === 32) {
                    snake = [{x: 10, y: 10}];
                    food = {
                        x: Math.floor(Math.random() * tileCount),
                        y: Math.floor(Math.random() * tileCount)
                    };
                    velocityX = 0;
                    velocityY = 0;
                    score = 0;
                    drawGame();
                }
            });

            drawGame();
        </script>
    </body>
    </html>
    """

  components.html(game_html, height=650)

  st.markdown(
    """
    <style>
        .stMarkdown {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
  )
