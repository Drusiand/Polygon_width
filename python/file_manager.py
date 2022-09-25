from typing import List
from python.utils import Point

__PAIR_DELIMITER = ';'
__POINT_DELIMITER = ','


def read_points(filename: str) -> List[Point]:
    points = list()
    with open(filename, 'r') as source:
        raw_data = source.read().split(__PAIR_DELIMITER)[:-1]
    for pair in raw_data:
        raw_point = tuple(float(token) for token in pair.split(__POINT_DELIMITER))
        tmp_point = Point(raw_point[0], raw_point[1])
        points.append(tmp_point)
    return points


def write_result(result: float) -> None:
    with open('output.txt', 'w') as f:
        f.write(str(result))
