import pydantic


class Move(pydantic.BaseModel):
    row: int
    col: int
    player: str = pydantic.Field(regex="^(x|o)$")
    player_id: int
    player_side: str = pydantic.Field(regex="^(x|o)$")


class Player(pydantic.BaseModel):
    player_id: int
