from SA import sematicAnalyzer
from time import time
import sys
import os


start = time()
if len(sys.argv) == 1:
    sematicAnalyzer(os.getcwd()+r'\test.js', sys.argv[0])
else:
    sematicAnalyzer(sys.argv[1], sys.argv[0])
print('\n程序用时', time()-start, 's')
