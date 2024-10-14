from json import loads
from typing import List, Self

class Color:
    def __init__(self, red: int, green: int, blue: int):
        if red < 0 or red > 255:
            raise ValueError("red must be between 0 and 255")
        if green < 0 or green > 255:
            raise ValueError("green must be between 0 and 255")
        if blue < 0 or blue > 255:
            raise ValueError("blue must be between 0 and 255")
        self.red = red
        self.green = green
        self.blue = blue

    def hex_code(self) -> str:
        return f'#{self.red:02x}{self.green:02x}{self.blue:02x}'

class CardColor:
    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color

class TrackColor:
    def __init__(self, name: str, color: Color, acceptable_card_colors: List[CardColor]):
        self.name = name
        self.color = color
        self.acceptable_card_colors = acceptable_card_colors

class TrainCard:
    def __init__(self, ):
        pass

class Model:
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def from_bytes(cls, b: bytes) -> Self:
        model = loads(b)
        name = model['name']
        return cls(name)