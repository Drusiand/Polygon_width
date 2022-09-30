import sys
from math import degrees, atan2, sqrt
from typing import List, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from numpy import cos, sin
from python.utils import Point
import math

__eps = 10e-11


def find_borders(points: List[Point]):
    top_point, bot_point = Point(0, 0), Point(sys.float_info.max, sys.float_info.max)
    top_ind, bot_ind = 0, 0
    for i, point in enumerate(points):
        if point.y() > top_point.y():
            top_point = point
            top_ind = i
        elif point.y() == top_point.y():
            if point.x() > top_point.x():
                top_point = point
                top_ind = i
        if point.y() < bot_point.y():
            bot_point = point
            bot_ind = i
        elif point.y() == bot_point.y():
            if point.x() < top_point.x():
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
    return 360 - abs(ang) if abs(ang) >= 180 else abs(ang)


def draw_plot(points: List[Point], pairs: List[Tuple[Point, Point]]):
    xs, ys = [points[-1].x()], [points[-1].y()]
    for point in points:
        xs.append(point.x())
        ys.append(point.y())
    plt.plot(xs, ys, c='black')
    for pair in pairs:
        plt.plot([pair[0].x(), pair[1].x()], [pair[0].y(), pair[1].y()])
    plt.show()


def draw_plot(polygon: List[Point], top_line: Tuple[Point, Point], bot_line: Tuple[Point, Point]):
    fig, ax = plt.subplots()

    # The "clip_on" here specifies that we _don't_ want to clip the line
    # to the extent of the axes
    ax.axline([top_line[0].x(), top_line[0].y()], [top_line[1].x(), top_line[1].y()], lw=1, c='red')
    ax.axline([bot_line[0].x(), bot_line[0].y()], [bot_line[1].x(), bot_line[1].y()], lw=1, c='red')
    patch_polygon = [(p.x(), p.y()) for p in polygon]
    poly = Polygon(patch_polygon)
    ax.add_patch(poly)
    ax.scatter(top_line[0].x(), top_line[0].y(), c='green')
    ax.scatter(top_line[1].x(), top_line[1].y(), c='black')
    ax.scatter(bot_line[0].x(), bot_line[0].y(), c='green')
    ax.scatter(bot_line[1].x(), bot_line[1].y(), c='black')
    manager = plt.get_current_fig_manager()
    # manager.window.showMaximized()
    plt.tight_layout()
    plt.show()


def check_pairs(pairs: List) -> bool:
    return (pairs[-1][0] == pairs[0][0] and pairs[-1][1] == pairs[0][1]) or (
            pairs[-1][0] == pairs[0][1] and pairs[-1][1] == pairs[0][0])


def get_pairs(points: List[Point]) -> List[Tuple[Point]]:
    top, bot = find_borders(points)
    top_point, top_ind, bot_point, bot_ind = top[0], top[1], bot[0], bot[1]
    pairs = [(top_point, bot_point)]
    lines = []
    tmp_top_point = Point(top_point.x() + 1, top_point.y())
    tmp_bot_point = Point(bot_point.x() - 1, bot_point.y())
    lines.append(((top_point, tmp_top_point), (bot_point, tmp_bot_point)))
    while True:
        # for point in pairs[-1]:
        #     print(point, end=' ')
        # print()
        # draw_plot(points, lines[-1][0], lines[-1][1])
        top_angle = get_angle(tmp_top_point, top_point, points[top_ind - 1])
        bot_angle = get_angle(tmp_bot_point, bot_point, points[bot_ind - 1])
        # if abs(top_angle - bot_angle) < __eps:
        if math.isclose(top_angle, bot_angle, rel_tol=10e-20):
            if bot_point != points[top_ind - 1]:
                pairs.append((bot_point, points[top_ind - 1]))
                lines.append(((top_point, points[top_ind - 1]), (bot_point, points[bot_ind - 1])))
                if check_pairs(pairs):
                    return pairs, lines
            if points[bot_ind - 1] != points[top_ind - 1]:
                pairs.append((points[bot_ind - 1], points[top_ind - 1]))
                lines.append(((top_point, points[top_ind - 1]), (bot_point, points[bot_ind - 1])))
                if check_pairs(pairs):
                    return pairs, lines
            if points[bot_ind - 1] != top_point:
                pairs.append((points[bot_ind - 1], top_point))
                lines.append(((top_point, points[top_ind - 1]), (bot_point, points[bot_ind - 1])))
                if check_pairs(pairs):
                    return pairs, lines
            top_point = points[top_ind - 1]
            bot_point = points[bot_ind - 1]
            top_point, tmp_top_point = rotate_line(top_point, np.deg2rad(180), top_point, points[top_ind])
            bot_point, tmp_bot_point = rotate_line(bot_point, np.deg2rad(180), bot_point, points[bot_ind])
            top_ind = top_ind - 1
            bot_ind = bot_ind - 1
            continue
        elif top_angle > bot_angle:
            if points[bot_ind - 1] != top_point:
                pairs.append((points[bot_ind - 1], top_point))
                top_point, tmp_top_point = rotate_line(top_point, np.deg2rad(bot_angle), top_point, tmp_top_point)
                bot_point = points[bot_ind - 1]
                bot_point, tmp_bot_point = rotate_line(bot_point, np.deg2rad(180), bot_point, points[bot_ind])
                delta_point = Point(tmp_bot_point.x() - bot_point.x(), tmp_bot_point.y() - bot_point.y())
                tmp_top_point = Point(top_point.x() - delta_point.x(), top_point.y() - delta_point.y())
                bot_ind = bot_ind - 1
                lines.append(((top_point, tmp_top_point), (bot_point, tmp_bot_point)))
        elif top_angle < bot_angle:
            if bot_point != points[top_ind - 1]:
                pairs.append((bot_point, points[top_ind - 1]))
                bot_point, tmp_bot_point = rotate_line(bot_point, np.deg2rad(top_angle), bot_point, tmp_bot_point)
                top_point = points[top_ind - 1]
                top_point, tmp_top_point = rotate_line(top_point, np.deg2rad(180), top_point, points[top_ind])
                delta_point = Point(tmp_top_point.x() - top_point.x(), tmp_top_point.y() - top_point.y())
                tmp_bot_point = Point(bot_point.x() - delta_point.x(), bot_point.y() - delta_point.y())
                top_ind = top_ind - 1
                lines.append(((top_point, tmp_top_point), (bot_point, tmp_bot_point)))

        if check_pairs(pairs):
            return pairs, lines


def line_distance(lines):
    line_1, line_2 = lines[0], lines[1]
    p1_1, p1_2 = line_1[0], line_1[1]
    p2_1, p2_2 = line_2[0], line_2[1]
    length_1 = sqrt((p1_2.x() - p1_1.x()) ** 2 + (p1_2.y() - p1_1.y()) ** 2)
    length_2 = sqrt((p2_2.x() - p2_1.x()) ** 2 + (p2_2.y() - p2_1.y()) ** 2)
    rho_1 = (p1_1.x() * p1_2.y() - p1_2.x() * p1_1.y()) / length_1
    rho_2 = -1 * ((p2_1.x() * p2_2.y() - p2_2.x() * p2_1.y()) / length_2)
    return abs(rho_1 - rho_2)


def distance(pair: Tuple[Point]) -> float:
    p1, p2 = pair[0], pair[1]
    return sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)


def get_width(points: List[Point]):
    pairs, lines = get_pairs(points)
    width = sys.float_info.max
    result_line = 0
    for pair, line in zip(pairs, lines):
        if line_distance(line) < width:
            width = line_distance(line)
            result_line = line
    # draw_plot(points, result_line[0], result_line[1])
    return width, result_line
