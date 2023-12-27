from fastapi import Depends, FastAPI, HTTPException, Path, Body
from sqlalchemy.orm import Session
import tictactoe as ttt
import models as models, schemas as schemas
from typing import Annotated
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_game_or_404(db: Session, game_id: str):
    game = db.query(models.Game).filter(models.Game.id==game_id).first()
    if game == None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game 


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/games/', response_model=list[schemas.Game])
def get_games(db: Session = Depends(get_db)):
    games = db.query(models.Game).all()
    return games

@app.get('/games/{game_id}', response_model=schemas.Game)
def get_game(
        game_id: Annotated[str, Path(min_length=10, max_length=10)], 
        db: Session = Depends(get_db)
    ):
    game = get_game_or_404(db, game_id)
    return game

@app.post('/games/', response_model=schemas.GameWithId)
def create_game(
        ai_symbol: Annotated[schemas.Symbol | None, Body(embed=True)] = None,
        db: Session = Depends(get_db)
    ):
    new_game = models.Game(ai_symbol=ai_symbol)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game

@app.patch('/games/{game_id}', response_model=schemas.Game)
def game_action(
        game_id: Annotated[str, Path(min_length=10, max_length=10)], 
        action: schemas.Action | None = None, 
        db: Session = Depends(get_db)
    ):

    game = get_game_or_404(db, game_id)
    if ttt.terminal(game.state):    
        raise HTTPException(status_code=400, detail="This game is over.")
    
    player = ttt.player(game.state)
    if player == game.ai_symbol:
        action = ttt.minimax(game.state)
    elif action:
        action = (action.x, action.y)
    else:
        raise HTTPException(status_code=400, detail="You must provide your move's coordinates (x, y)!")
    
    if action not in ttt.actions(game.state):
        raise HTTPException(status_code=400, detail="Invalid move!")
    
    game.state = ttt.result(game.state, action) 
    
    game.player = ttt.player(game.state)
    is_game_over = ttt.terminal(game.state)

    if is_game_over:
        game.winner = ttt.winner(game.state)
        if game.winner is None:
            game.winner = 'draw'
    db.add(game)
    db.commit()
    return game

@app.put('/games/{game_id}', response_model=schemas.Game)
def game_reset(
        game_id: Annotated[str, Path(min_length=10, max_length=10)], 
        ai_symbol: Annotated[schemas.Symbol | None, Body(embed=True)] = None,
        db: Session = Depends(get_db)
    ):

    game = get_game_or_404(db, game_id)
    game.state = ttt.initial_state()
    game.winner = None
    game.player = 'X'
    game.ai_symbol = ai_symbol
    db.add(game)
    db.commit()
    return game
    



