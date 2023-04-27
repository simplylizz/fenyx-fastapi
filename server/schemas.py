import pydantic
from typing import Optional


class Move(pydantic.BaseModel):
    row: int
    col: int
    player_id: str

class Player(pydantic.BaseModel):
    name: str
    id: Optional[str]
    wins: int = 0
    
class JoinGame((pydantic.BaseModel)):
    game_id: str
    player_id: str