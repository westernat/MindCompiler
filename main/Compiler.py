from sys import argv
from tool import *
from SA import sematicAnalyzer


if __name__ == "__main__":
    length = len(argv)
    if length == 1:
        print("缺少选项与文件路径!")
        print(HELP)
        print(COULD_USE)
    else:
        opt = argv[1]
        if opt.startswith("-"):
            match opt:
                case "-t" | "--test":
                    if length == 3:
                        if argv[2] in ("-a", "--all"):
                            for file_name in listdir(TEST_DIR):
                                print(file_name.center(40, "@"))
                                optimizing(sematicAnalyzer(path.join(TEST_DIR, file_name)))
                        else:
                            optimizing(sematicAnalyzer(path.join(TEST_DIR, argv[2])))
                    else:
                        print(COULD_USE)
                case "-c" | "--compile":
                    if length == 3:
                        optimizing(sematicAnalyzer(argv[2]))
                    else:
                        print("缺少文件路径!")
                        print(COULD_USE)
        else:
            print("缺少选项!")
            print(HELP)
