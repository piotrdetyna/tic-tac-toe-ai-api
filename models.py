from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TypeDecorator, types
from sqlalchemy.orm import relationship
from uuid import uuid4
from database import Base
import json
import tictactoe as ttt

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
    return uuid4().hex[:10].upper()

class Game(Base):
    __tablename__ = 'games'
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    state = Column(Json, default=ttt.initial_state())
    ai_symbol = Column(String, default='O')
    winner = Column(String)
    player = Column(String, default='X')

