from pydantic import BaseModel, conint, Field
from enum import Enum
from config import *
from typing import Annotated


class Symbol(str, Enum):
    O = 'O'
    X = 'X'

class Result(str, Enum):
    O = 'O'
    X = 'X'
    draw = 'draw'

class Action(BaseModel):
    x: conint(ge=0, le=2)
    y: conint(ge=0, le=2)

STATE_ROW = Annotated[
    list[
        Symbol | None
    ], Field(min_length=3, max_length=3)]

class GameBase(BaseModel):
    ai_symbol: Symbol = Field(
        default=DEFAULT_AI_SYMBOL, 
        description=f'Symbol ("O" or "X"), default: {DEFAULT_AI_SYMBOL} which is used by the AI')

class Game(GameBase):
    state: Annotated[list[STATE_ROW], Field(min_length=3, max_length=3)] = Field(
        description='A 3x3 grid representing current state of the game'
    )
    
    winner: Result | None = Field(
        default=None,
        description='If the game is over, this field\'value is "X", "O", or "draw", otherwise None'
    )
    current_player: Symbol = Field(
        default=DEFAULT_FIRST_PLAYER_SYMBOL,
        description='Symbol ("O" or "X") of the player whose next move belongs'
    )

class CreateGame(GameBase):
    pass

class GameWithId(Game):
    id: str
