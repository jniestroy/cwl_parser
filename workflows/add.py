import json
import sys


def add(inputs):
    x = inputs[1]
    y = inputs[2]
    print(x+y)


if __name__ == '__main__':
    add(sys.argv)
