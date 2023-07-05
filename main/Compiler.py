from SA import sematicAnalyzer
from time import time
from sys import argv
from os import path


PROJECT_ROOT = path.split(path.split(__file__)[0])[0]


if __name__ == '__main__':
    start = time()
    if len(argv) == 1:
        sematicAnalyzer(path.join(PROJECT_ROOT, './test/single.js'))
    else:
        sematicAnalyzer(argv[1])
    stop = time()
    print('\n程序用时', stop-start, 's')
