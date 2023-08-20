from SA import sematicAnalyzer
from time import time
from sys import argv
from tool import *


def optimizing(files: dict[str, dict[str, list[list[str] | str]]]):
    def link_helper(links: list[list[str] | str]):
        table = []
        for link in links:
            if isinstance(link, list) and link[0].startswith("m_"):
                linked = []
                for index in range(len(link)):
                    atom = link[index]
                    if atom.startswith("$l") and (to_link := file.get(atom)):
                        linked = link_helper(to_link)
                        link[index] = str(len(table) + len(linked) + 1)
                table.append(eval(f"{link[0]}{tuple(link[1:])}"))
                table.extend(linked)
        return table

    linked_table = []
    console(files, "unlinked")
    for file_name in files:
        file = files[file_name]
        linked_table.append(link_helper(file["$l0"]))

    # 最终拼接
    final_list = []
    for linked in linked_table:
        final_list.extend(linked)

    print("mdtlog".center(20, "="))
    for line in final_list:
        print(line)
    print("printflush message1")


if __name__ == "__main__":
    start = time()
    if len(argv) == 1:
        optimizing(sematicAnalyzer(path.join(TEST_DIR, "for-test.js")))
    else:
        optimizing(sematicAnalyzer(argv[1]))
    stop = time()
    print("\n程序用时", stop - start, "s")
