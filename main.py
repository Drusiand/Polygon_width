import sys
from python.process import get_width
from python.file_manager import read_points
from python.utils import Point


def run(filename: str):
    points = read_points(filename)
    # points = [Point(a, a*a) for a in range(20000)]
    width, line = get_width(points)
    with open('output.txt', 'w') as f:
        for pair in line:
            for vertex in pair:
                rounded_vertex = Point(
                    float(round(vertex.x()) if abs(round(vertex.x(), 7) - vertex.x()) < 10e-7 else vertex.x()),
                    float(round(vertex.y()) if abs(round(vertex.y(), 7) - vertex.y()) < 10e-7 else vertex.y()))
                f.write(str(rounded_vertex))
            f.write('\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        run(file)
        print('Success!\n'
              'Result is saved in \"output.txt\" file')
    else:
        print('Not enough arguments, consider pass input filename as 1st argument!')
