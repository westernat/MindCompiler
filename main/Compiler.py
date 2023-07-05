from SA import sematicAnalyzer
from time import time
from sys import argv
from tool import TEST_FILE


def optimizing(blocks: dict[str, dict]):
    pass


if __name__ == '__main__':
    start = time()
    if len(argv) == 1:
        optimizing(sematicAnalyzer(TEST_FILE))
    else:
        optimizing(sematicAnalyzer(argv[1]))
    stop = time()
    print('\n程序用时', stop-start, 's')
