from pydantic import BaseModel, conint, constr
from enum import Enum

class Symbol(str, Enum):
    O = 'O'
    X = 'X'

class Action(BaseModel):
    x: conint(ge=0, le=2)
    y: conint(ge=0, le=2)

class Game(BaseModel):
    state: list[list[str | None]]
    ai_symbol: str = 'O'
    winner: str | None = None
    player: str = 'X'

class GameWithId(Game):
    id: str
