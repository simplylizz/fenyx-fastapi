import pydantic


class Move(pydantic.BaseModel):
    row: int
    col: int
    player: str = pydantic.Field(regex="^(x|o)$")
class Game(pydantic.BaseModel):
    id: int
    player_x: int
    player_o: int
    field: list[list[str]] = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_move: str = "x"
    status: str = "new"
    player_x_score: float = 0
    player_o_score: float = 0
