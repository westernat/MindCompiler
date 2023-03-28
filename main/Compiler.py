from SA import sematicAnalyzer
from time import time
import sys
import os


start = time()
if len(sys.argv) == 1:
    sematicAnalyzer(os.getcwd()+r'\test.js')
else:
    sematicAnalyzer(sys.argv[1])
print('\n程序用时', time()-start, 's')
