from sqlalchemy import Column, String, TypeDecorator, types
from uuid import uuid4
from database import Base
import json
import tictactoe as ttt
from config import *

class Json(TypeDecorator):

    @property
    def python_type(self):
        return object

    impl = types.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
        
def generate_uuid():
    return uuid4().hex[:GAME_ID_LENGTH].upper()

class Game(Base):
    __tablename__ = 'games'
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    state = Column(Json, default=ttt.initial_state())
    ai_symbol = Column(String, default=DEFAULT_AI_SYMBOL)
    winner = Column(String)
    current_player = Column(String, default=DEFAULT_FIRST_PLAYER_SYMBOL)

