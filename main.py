import sys
from python.process import get_width
from python.file_manager import read_points


def run(filename: str):
    points = read_points(filename)
    width = get_width(points)
    with open('output.txt', 'w') as f:
        f.write(str(width))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        run(file)
        print('Success!\n'
              'Result is saved in \"output.txt\" file')
    else:
        print('Not enough arguments, consider pass input filename as 1st argument!')
