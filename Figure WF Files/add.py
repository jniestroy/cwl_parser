import json
import sys


def add(inputs):
    x = int(inputs[1])
    y = int(inputs[2])
    print(x+y)


if __name__ == '__main__':
    add(sys.argv)
