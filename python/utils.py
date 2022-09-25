from itertools import cycle


class Point:
    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y

    def x(self) -> float:
        return self.__x

    def y(self) -> float:
        return self.__y

    def __str__(self):
        return '(' + str(self.__x) + ', ' + str(self.__y) + ')'

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y


class Polygon:
    def __init__(self, points, top, bot):
        self.__points = cycle(points)
        self.__top, self.__bot = top, bot
