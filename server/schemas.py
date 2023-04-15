import pydantic


class Move(pydantic.BaseModel):
    row: int
    col: int
    player: str = pydantic.Field(regex="^(x|o)$")
