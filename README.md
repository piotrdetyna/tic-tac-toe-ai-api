<h1 style="text-align: center;"> ⭕ Tic-Tac-Toe AI API ❌ </h1>

API allowing you to play tic-tac-toe against the minimax algorithm (more on this later). The interface is created in FastAPI, and has great tests. In addition, in this repo you can find a sample Tic-Tac-Toe game UI, which is based on this API.

![Demonstration](https://piotr.detyna.pl/tic-tac-toe/ttt.gif)

## 🤖 How the AI works?
The AI is based on the minimax algorithm. In short, the minimax algorithm recursively analyzes all possible moves from the current game state to the final state, **assuming that the opponent is also playing optimally**. After considering these options, AI chooses the best move from the current game state. I won't go into details, but if you are curious how it works, I recommend an article on [geeksforgeeks.org](https://www.geeksforgeeks.org/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/).

The game logic is implemented in the `tictactoe.py` file, which I created when taking the [Harvard CS50’s Introduction to Artificial Intelligence with Python course](https://cs50.harvard.edu/ai).

Note: It is possible to optimize this algorithm by using `alpha-beta pruning`, which allows us to finish resolving moves faster when we know that we will not find a better solution.

## 🛠️ API documentation
<span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span>`/games/`

- Returns all games
- Parameters: No parameters
- Example response: 
    ```
    [
        {
            "ai_symbol": "O",
            "state": [
                [
                    null, null, null
                ],
                [
                    null, "X", null
                ],
                [
                    "O", null, null
                ]
            ],
            "winner": null,
            "current_player": "X"
        },
        ...
    ]
    ```

#
<span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span>`/games/{game_id}`

- Returns a game with given id
- Parameters: `game_id` (_required_)
- Example response: 
    ```
    {
        "ai_symbol": "O",
        "state": [
            [
                null, null, null
            ],
            [
                null, "X", null
            ],
            [
                "O", null, null
            ]
        ],
        "winner": null,
        "current_player": "X"
    }
    ```

#
<span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>`/games/`

- Creates a game
- Parameters: `ai_symbol` (_optional_)
    - `ai_symbol` can be 'O' or 'X', if it's not sent, ai will use `config.DEFAULT_AI_SYMBOL`
- Example request body:
    ```
    {
        "ai_symbol": "O"
    }
    ```
- Example response: 
    ```
    {
        "ai_symbol": "O",
        "state": [
            [
                null, null, null
            ],
            [
                null, null, null
            ],
            [
                null, null, null
            ]
        ],
        "winner": null,
        "current_player": "X",
        "id": "88054A80D0"
    }
    ```
    - Important! Returns the game ID so you can use other endpoints (e.g. for making moves), and in fact, play the game. **Keep your ID private so no one can, for example, reset your game.**

  
#
<span float="left"><img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"></span>`/games/{game_id}/`

- Puts the current player's symbol in the correct place on the board.
- Parameters: `game_id` (_required_), `x`, `y`
    - `x`, `y` are required only when current player is a human, if the AI is taking his turn, those will be ignored.
- Example request body (when it's a human's turn and you want to place your symbol in top-left corner):
    ```
    {
        "x": 0,
        "y": 0
    }
    ```
- Example response: 
    ```
    {
        "ai_symbol": "O",
        "state": [
            [
                "X", null, null
            ],
            [
                null, null, null
            ],
            [
                null, null, null
            ]
        ],
        "winner": null,
        "current_player": "O"
        }
    ```


#
<span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>`/games/{game_id}/`

- Resets game to inital state
- Parameters: `game_id`(_required_), `ai_symbol` (_optional_)
    - `ai_symbol` can be 'O' or 'X', if it's not sent, ai will use `config.DEFAULT_AI_SYMBOL`
- Example request body:
    ```
    {
        "ai_symbol": "X"
    }
    ```
- Example response: 
    ```
    {
        "ai_symbol": "X",
        "state": [
            [
                null, null, null
            ],
            [
                null, null, null
            ],
            [
                null, null, null
            ]
        ],
        "winner": null,
        "current_player": "X",
        "id": "88054A80D0"
    }
    ```
