import re
from os import path, listdir
from pprint import pprint
from time import time


OperationMode = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div",
    "%": "mod",
    "&": "and",
    "|": "or",
    "!": "not",
    "^": "xor",
    "&&": "land",
    "||": "or",
    "**": "pow",
    "<<": "shl",
    ">>": "shr"
}


JumpMode = {
    "true": "allways",
    ">": "greaterThan",
    ">=": "greaterThanEq",
    "<": "lessThan",
    "<=": "lessThanEq",
    "==": "equal",
    #   '===': 'strictEqual',
    "!=": "notEqual",
    "f>": "lessThanEq",
    "f>=": "lessThan",
    "f<": "greaterThanEq",
    "f<=": "greaterThan",
    "f==": "notEqual",
    "f!=": "equal",
}


def m_read(result, _from, at):
    return f"read {result} {_from} {at}"


def m_write(result, to, at):
    return f"write {result} {to} {at}"


def m_draw(mode, a, b, c, d, e, f):
    return f"draw {mode} {a} {b} {c} {d} {e} {f}"


def m_print(msg):
    return f"print {msg}"


def m_drawflush(to):
    return f"drawflush {to}"


def m_printflush(to):
    return f"printflush {to}"


def m_getlink(result, link):
    return f"getlink {result} {link}"


def m_control(_set, of, a, b, c, d):
    return f"control {_set} {of} {a} {b} {c} {d}"


def m_radar(_from, target1, target2, target3, order, sort, output):
    return f"radar {target1} {target2} {target3} {order} {_from} {sort} {output}"


def m_sensor(result, of, at):
    return f"sensor {result} {at} {of}"


def m_set(result, value):
    return f"set {result} {value}"


def m_operation(mode, result, a, b="0"):
    return f"op {mode} {result} {a} {b}"


def m_lookup(result, mode, id):
    return f"lookup {mode} {result} {id}"


def m_packcolor(result, r, g, b, a):
    return f"packcolor {result} {r} {g} {b} {a}"


def m_wait(delay):
    return f"wait {delay}"


def m_stop():
    return "stop"


def m_end():
    return "end"


def m_jump(goto, mode, left, right):
    finalMode = JumpMode[mode]
    if finalMode == "allways":
        return f"set @counter {goto}"
    return f"jump {goto} {finalMode} {left} {right}"


def m_ubind(type):
    return f"ubind {type}"


def m_ucontrol(mode, a, b, c, d, e):
    return f"ucontrol {mode} {a} {b} {c} {d} {e}"


def m_uradar(target1, target2, target3, order, sort, result):
    return f"uradar {target1} {target2} {target3} {sort} 0 {order} {result}"


def m_ulocate(find, *, group, enemy, ore, outX="outx", outY, found, building):
    return f"ulocate {find} {group} {enemy} {ore} {outX} {outY} {found} {building}"


Builtins = {
    "read",
    "write",
    "draw",
    "print",
    "drawflush",
    "printflush",
    "getlink",
    "control",
    "radar",
    "sensor",
    "lookup",
    "packcolor",
    "wait",
    "stop",
    "ubind",
    "ucontrol",
    "uradar",
    "ulocate",
}


DEBUG = False
PROJECT_ROOT = path.split(path.split(__file__)[0])[0]
TEST_DIR = path.join(PROJECT_ROOT, "test/")
HELP = """使用方法: Compiler [option] [file-path]
option:
    -t --test
    -c --compile"""


def couldUse():
    print("可用的测试文件:")
    for file_name in listdir(TEST_DIR):
        print("   ", file_name)


def isNumber(literal: str):
    return re.match("^[-+]?[0-9]+(.[0-9]+)?$", literal)


def labelGener(prefix: str):
    counter = 0
    while True:
        yield f"{prefix}{counter}"
        counter += 1


def console(obj: object, label=""):
    if DEBUG:
        if label == "":
            print(obj)
        else:
            print(label.center(20, "="))
            pprint(obj)


def optimizing(unlinked: dict[str, dict[str, list[list[str]]]]):
    start = time()

    def link_helper(links: list[list[str]]):
        table = []
        for link in links:
            if isinstance(link, list) and link[0].startswith("m_"):
                linked = []
                for index in range(len(link)):
                    atom = link[index]
                    if atom.startswith("$l") and (to_link := module.get(atom)):
                        linked = link_helper(to_link)
                        link[index] = str(len(table) + len(linked) + 1)
                table.append(eval(f"{link[0]}{tuple(link[1:])}"))
                table.extend(linked)
        return table
    # 单个模块内拼接
    linked_table = []
    console(unlinked, "unlinked")
    for module_name in unlinked:
        module = unlinked[module_name]
        linked_table.append(link_helper(module["$l0"]))
    # 多个模块间拼接
    final_list = []
    for linked in linked_table:
        final_list.extend(linked)
    # 输出结果
    console("mdtlog".center(20, "="))
    for line in final_list:
        print(line)
    print("printflush message1")

    stop = time()
    print("\n程序用时", stop - start, "s")
