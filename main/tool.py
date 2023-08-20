import re
from os import path
from pprint import pprint


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


DEBUG = True
PROJECT_ROOT = path.split(path.split(__file__)[0])[0]
TEST_DIR = path.join(PROJECT_ROOT, "test/")


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
