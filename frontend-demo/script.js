let grid = null
let cells = {}
let aiSymbol = null
let gameId = null
let gameState = null
let currentPlayer = null
let winner = null

document.addEventListener('DOMContentLoaded', async () => {
    grid = document.querySelector('.tic-tac-toe');
    let startGameButton = document.querySelector('#start-game');
    let restartGameButton = document.querySelector('#restart-game');

    populateCellsObject();
    grid.onclick = send_info_message_if_game_is_not_started
    

    startGameButton.onclick = async () => {
        startGameButton.innerHTML = 'Restart game';
        await initializeGame();
        updateGridState();
        game();
        startGameButton.classList.add('hidden');
        restartGameButton.classList.remove('hidden');
    };

    restartGameButton.onclick = async () => {
        grid.removeEventListener('click', gridClickEventListener)
        await restartGame();
        updateGridState();
        game();
    };
});


async function game() {
    do {
        if (currentPlayer == aiSymbol) {
            markAllCellsDisabled()
            await makeAIMove()
            
            await sleep(500)
            updateGridState()
        }
        else {
            markAllCellsEnabled()
            let humanMove = await waitForPlayerMove()
            await makeHumanMove(humanMove)
            updateGridState();
        }

    } while(!winner)
    sendMessage(winner !== 'draw' ? `${winner} has won!` : 'We have a draw!');
}


async function initializeGame() {
    const response = await fetch('http://127.0.0.1:8000/games/', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'ai_symbol': document.querySelector('#who-starts').value
        })
        
    })
    let data = await response.json()
    if (response.ok) {
        gameId = data.id
        gameState = data.state
        currentPlayer = data.current_player
        aiSymbol = data.ai_symbol
        winner = data.winner
    }
    else {
        sendMessage(data.detail)
    }
    
    return gameId
}

async function restartGame() {
    const response = await fetch(`http://127.0.0.1:8000/games/${gameId}`, {
        method: 'PUT',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'ai_symbol': document.querySelector('#who-starts').value
        })
    })
    let data = await response.json()
    if (response.ok) {
        gameState = data.state
        currentPlayer = data.current_player
        aiSymbol = data.ai_symbol
        winner = data.winner
    }
    else {
        sendMessage(data.detail)
    }
    
    return gameId
}

async function makeAIMove() {
    const response = await fetch(`http://127.0.0.1:8000/games/${gameId}`, {method: 'PATCH'})
    let data = await response.json()
    if (response.ok) {
        gameState = data.state
        currentPlayer = data.current_player
        winner = data.winner
    }
    else {
        sendMessage(data.detail)
    }
    return gameId
}

async function makeHumanMove(humanMove) {
    const response = await fetch(`http://127.0.0.1:8000/games/${gameId}`, {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'x': parseInt(humanMove[0]),
            'y': parseInt(humanMove[2])
        })
    })

    data = await response.json()
    if (response.ok) {
        gameState = data.state
        currentPlayer = data.current_player
        winner = data.winner
    }
    else {
        sendMessage(data.detail)
    }
    
    return gameId
}


function sendMessage(message) {
    messageElement = document.querySelector('#message')
    messageElement.innerHTML = message
    setTimeout(() => {messageElement.innerHTML = ''}, 3000)
}

function sleep(n) {
    return new Promise(resolve => setTimeout(resolve, n));
}

function populateCellsObject() {
    grid.querySelectorAll('.cell').forEach(cell => {
        cells[[cell.dataset.x, cell.dataset.y]] = cell
    })
}

function updateGridState() {
    for (let i=0; i<3; i++) {
        for (let j=0; j<3; j++) {
            cells[[j, i]].innerHTML = gameState[j][i]
        }
    }
}

function markAllCellsDisabled() {
    Object.entries(cells).forEach(cell => {
        let cellElement = cell[1];
        cellElement.classList.add('disabled')
    });
}

function markAllCellsEnabled() {
    Object.entries(cells).forEach(cell => {
        let cellElement = cell[1];
        cellElement.classList.remove('disabled')
    });
}

async function waitForPlayerMove() {
    return new Promise((resolve) => {
        gridClickEventListener = event => {
            console.log(event.target.classList)
            if (Array.from(event.target.classList).includes('cell')) {
                resolve(event.target.dataset.x + ',' + event.target.dataset.y);
            } else {
                grid.addEventListener('click', gridClickEventListener);
            }
        };
        grid.addEventListener('click', gridClickEventListener, { once: true });
    });
}

function send_info_message_if_game_is_not_started() {
    if (!gameId) {
        sendMessage('Start a game first!') 
    }
    else {
        grid.onclick = null
    }
}

