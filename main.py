from fastapi import Depends, FastAPI, HTTPException, Path, Body
from sqlalchemy.orm import Session
import tictactoe as ttt
import models as models, schemas as schemas
from typing import Annotated
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from config import *

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/games/', response_model=list[schemas.Game])
def get_games_view(db: Session = Depends(get_db)):
    games = db.query(models.Game).all()
    return games


@app.get('/games/{game_id}', response_model=schemas.Game)
def get_game_view(
        game_id: Annotated[str, Path(min_length=GAME_ID_LENGTH, max_length=GAME_ID_LENGTH)], 
        db: Session = Depends(get_db)
    ):
    game = get_game_or_404(db, game_id)
    return game


@app.post('/games/', response_model=schemas.GameWithId)
def create_game_view(
        game: schemas.CreateGame,
        db: Session = Depends(get_db)
    ):
    new_game = models.Game(ai_symbol=game.ai_symbol)
    save_game(new_game, db)
    db.refresh(new_game)
    return new_game


@app.patch('/games/{game_id}', response_model=schemas.Game)
def game_action_view(
        game_id: Annotated[str, Path(min_length=GAME_ID_LENGTH, max_length=GAME_ID_LENGTH)], 
        action: schemas.Action | None = None, 
        db: Session = Depends(get_db)
    ):

    game = get_game_or_404(db, game_id)
    raise_400_if_game_is_over(game)
    
    player = ttt.player(game.state)
    if player == game.ai_symbol:
        action = get_ai_action(game)
    elif action:
        action = (action.x, action.y)
    else:
        raise HTTPException(status_code=400, detail="You must provide your move's coordinates (x, y)!")
    
    raise_400_if_action_is_invalid(action, game)

    game.state = ttt.result(game.state, action) 
    game.current_player = ttt.player(game.state)
    game.winner = get_game_result(game)
    save_game(game, db)
    return game

@app.put('/games/{game_id}', response_model=schemas.GameWithId)
def game_reset_view(
        game_id: Annotated[str, Path(min_length=GAME_ID_LENGTH, max_length=GAME_ID_LENGTH)], 
        input_game: schemas.CreateGame,
        db: Session = Depends(get_db)
    ):

    game = get_game_or_404(db, game_id)
    game.state = ttt.initial_state()
    game.winner = None
    game.current_player = DEFAULT_FIRST_PLAYER_SYMBOL
    game.ai_symbol = input_game.ai_symbol
    save_game(game, db)
    return game
    
@app.delete('/games/', status_code=204)
def delete_games_view(db: Session = Depends(get_db)):
    delete_all_games(db)
    return

def raise_400_if_game_is_over(game):
    if ttt.terminal(game.state):    
        raise HTTPException(status_code=400, detail="This game is over.")
    
def raise_400_if_action_is_invalid(action, game):
    if action not in ttt.actions(game.state):
        raise HTTPException(status_code=400, detail="Invalid move!")

def get_ai_action(game):
    return ttt.minimax(game.state)

def get_game_result(game):
    winner = None
    is_game_over = ttt.terminal(game.state)
    if is_game_over:
        winner = ttt.winner(game.state)
        if not winner:
            winner = 'draw'
    return winner

def get_game_or_404(db: Session, game_id: str):
    game = db.query(models.Game).filter(models.Game.id==game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game 

def save_game(game, db):
    db.add(game)
    db.commit()

def delete_all_games(db: Session):
    db.query(models.Game).delete()
    db.commit()