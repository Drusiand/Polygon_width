import sys
from math import degrees, atan2, sqrt
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin
from python.utils import Point

__eps = 10e-9


def find_borders(points: List[Point]):
    top_point, bot_point = Point(0, 0), Point(sys.float_info.max, sys.float_info.max)
    top_ind, bot_ind = 0, 0
    for i, point in enumerate(points):
        if point.y() > top_point.y():
            top_point = point
            top_ind = i
        if point.y() < bot_point.y():
            bot_point = point
            bot_ind = i
    return (top_point, top_ind), (bot_point, bot_ind)


def rotate_line(c: Point, angle: float, p1: Point, p2: Point):
    x1 = ((p1.x() - c.x()) * cos(angle) + (p1.y() - c.y()) * sin(angle)) + c.x()
    y1 = (-(p1.x() - c.x()) * sin(angle) + (p1.y() - c.y()) * cos(angle)) + c.y()

    x2 = ((p2.x() - c.x()) * cos(angle) + (p2.y() - c.y()) * sin(angle)) + c.x()
    y2 = (-(p2.x() - c.x()) * sin(angle) + (p2.y() - c.y()) * cos(angle)) + c.y()

    return Point(x1, y1), Point(x2, y2)


def get_angle(a: Point, b: Point, c: Point):
    ang = degrees(atan2(c.y() - b.y(), c.x() - b.x()) - atan2(a.y() - b.y(), a.x() - b.x()))
    return abs(ang) - 180 if abs(ang) >= 180 else abs(ang)


def draw_plot(points: List[Point], pairs: List[Tuple[Point, Point]]):
    xs, ys = [points[-1].x()], [points[-1].y()]
    for point in points:
        xs.append(point.x())
        ys.append(point.y())
    plt.plot(xs, ys, c='black')
    for pair in pairs:
        plt.plot([pair[0].x(), pair[1].x()], [pair[0].y(), pair[1].y()])
    plt.show()


def get_pairs(points: List[Point]) -> List[Tuple[Point]]:
    top, bot = find_borders(points)
    top_point, top_ind, bot_point, bot_ind = top[0], top[1], bot[0], bot[1]
    pairs = [(top_point, bot_point)]
    tmp_top_point = Point(top_point.x() + 1, top_point.y())
    tmp_bot_point = Point(bot_point.x() - 1, bot_point.y())
    while True:
        top_angle = get_angle(tmp_top_point, top_point, points[top_ind - 1])
        bot_angle = get_angle(tmp_bot_point, bot_point, points[bot_ind - 1])

        if abs(top_angle - bot_angle) < __eps:
            pairs.append((bot_point, points[top_ind - 1]))
            pairs.append((points[bot_ind - 1], points[top_ind - 1]))
            pairs.append((points[bot_ind - 1], top_point))
            top_point = points[top_ind - 1]
            bot_point = points[bot_ind - 1]
            top_point, tmp_top_point = rotate_line(top_point, np.deg2rad(180), top_point, points[top_ind])
            bot_point, tmp_bot_point = rotate_line(bot_point, np.deg2rad(180), bot_point, points[bot_ind])
            top_ind = top_ind - 1
            bot_ind = bot_ind - 1
            continue
        if top_angle > bot_angle:
            tmp_pair = (points[bot_ind - 1], top_point)
            pairs.append(tmp_pair)
            top_point, tmp_top_point = rotate_line(top_point, np.deg2rad(bot_angle), top_point, tmp_top_point)
            bot_point = points[bot_ind - 1]
            bot_point, tmp_bot_point = rotate_line(bot_point, np.deg2rad(180), bot_point, points[bot_ind])
            bot_ind = bot_ind - 1
        elif top_angle < bot_angle:
            tmp_pair = (points[top_ind - 1], bot_point)
            pairs.append(tmp_pair)
            bot_point, tmp_bot_point = rotate_line(bot_point, np.deg2rad(top_angle), bot_point, tmp_bot_point)
            top_point = points[top_ind - 1]
            top_point, tmp_top_point = rotate_line(top_point, np.deg2rad(180), top_point, points[top_ind])
            top_ind = top_ind - 1

        if (pairs[-1][0] == pairs[0][0] and pairs[-1][1] == pairs[0][1]) or (
                pairs[-1][0] == pairs[0][1] and pairs[-1][1] == pairs[0][0]):
            return pairs


def distance(pair: Tuple[Point]) -> float:
    p1, p2 = pair[0], pair[1]
    return sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)


def get_width(points: List[Point]) -> float:
    pairs = get_pairs(points)
    width = sys.float_info.max
    for pair in pairs:
        if distance(pair) < width:
            width = distance(pair)
    # draw_plot(points, pairs)
    return width
