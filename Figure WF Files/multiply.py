
import json
import sys


def multiply(inputs):
    x = inputs[1]
    with open(x) as f:
        x1 = int(f.read())
    y = int(inputs[2])
    print(x1*y)


if __name__ == '__main__':
    multiply(sys.argv)
