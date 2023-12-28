<h1 style="text-align: center;"> ⭕ Tic-Tac-Toe AI API ❌ </h1>

API allowing you to play tic-tac-toe against the minimax algorithm (more on this later). The API is created in FastAPI. In addition, there is a sample UI using this API.

![Demonstration](https://piotr.detyna.pl/tic-tac-toe/ttt.gif)

## 🤖 How the AI works?
The AI is based on the minimax algorithm. In short, the minimax algorithm recursively analyzes all possible moves from the current game state to the final state, **assuming that the opponent is also playing optimally**. After considering these options, AI chooses the best move from the current game state. I won't go into details, but if you are curious how it works, I recommend an article on [geeksforgeeks.org](https://www.geeksforgeeks.org/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/).

The game logic is implemented in the `tictactoe.py` file, which I created when taking the [Harvard CS50’s Introduction to Artificial Intelligence with Python course](https://cs50.harvard.edu/ai).

Note: It is possible to optimize this algorithm by using `alpha-beta pruning`, which allows us to finish resolving moves faster when we know that we will not find a better solution.

