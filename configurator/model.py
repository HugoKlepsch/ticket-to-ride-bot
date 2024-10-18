from enum import Enum
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


class CardColor(Enum):
    def __init__(self, name: str, color: Color|None):
        self.name = name
        self.color = color

    RAINBOW = ('Rainbow', None)
    PINK = ('Pink', None)
    BLUE = ('Blue', None)
    GREEN = ('Green', None)
    YELLOW = ('Yellow', None)
    ORANGE = ('Orange', None)
    RED = ('Red', None)
    WHITE = ('White', None)
    BLACK = ('Black', None)


class TrackColor(Enum):
    def __init__(self, name: str, color: Color|None, acceptable_card_colors: List[CardColor]):
        self.name = name
        self.color = color
        self.acceptable_card_colors = acceptable_card_colors

    GREY = ('Grey', None, [CardColor.RAINBOW,
                           CardColor.PINK,
                           CardColor.BLUE,
                           CardColor.GREEN,
                           CardColor.YELLOW,
                           CardColor.ORANGE,
                           CardColor.RED,
                           CardColor.WHITE,
                           CardColor.BLACK])
    PINK = ('Pink', None, [CardColor.RAINBOW, CardColor.PINK])
    BLUE = ('Blue', None, [CardColor.RAINBOW, CardColor.BLUE])
    GREEN = ('Green', None, [CardColor.RAINBOW, CardColor.GREEN])
    YELLOW = ('Yellow', None, [CardColor.RAINBOW, CardColor.YELLOW])
    ORANGE = ('Orange', None, [CardColor.RAINBOW, CardColor.ORANGE])
    RED = ('Red', None, [CardColor.RAINBOW, CardColor.RED])
    WHITE = ('White', None, [CardColor.RAINBOW, CardColor.WHITE])
    BLACK = ('Black', None, [CardColor.RAINBOW, CardColor.BLACK])


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