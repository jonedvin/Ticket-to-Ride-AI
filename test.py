import enum
import random


class Color(enum.Enum):
    red = enum.auto()
    blue = enum.auto()
    green = enum.auto()
    yellow = enum.auto()
    orange = enum.auto()
    pink = enum.auto()
    white = enum.auto()
    black = enum.auto()
    grey = enum.auto()
    locomotive = enum.auto()


for _ in range(10):
    print(Color(random.randint(1, len(Color))))