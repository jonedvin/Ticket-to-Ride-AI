import enum

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

class MyClass():
    def __init__(self):
        self.name = "myname"


print(str(Color.red).split(".")[1])

# mydict = dict[str, MyClass]
# mydict["test"] = MyClass()
# # mydict[Color.red] = 3

# print(mydict)
