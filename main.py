import sys
from python.process import get_width
from python.file_manager import read_points


def run(filename: str):
    points = read_points(filename)
    width, line = get_width(points)
    with open('output.txt', 'w') as f:
        for pair in line:
            for vertex in pair:
                f.write(str(vertex))
            f.write('\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        run(file)
        print('Success!\n'
              'Result is saved in \"output.txt\" file')
    else:
        print('Not enough arguments, consider pass input filename as 1st argument!')
