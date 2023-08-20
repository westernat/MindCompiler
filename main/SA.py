from SP import Env, syntacticParser
from tool import labelGener, OperationMode, Builtins, TEST_DIR, isNumber, console
from sys import argv
from os import path

variableLabelGener = labelGener("v")
linkLabelGener = labelGener("$l")
blocks = {"main": {}}
functions = {}
imports = {}


def a_block(stmts: list):
    env: Env = stmts[0]
    label = next(linkLabelGener)
    table = blocks[env.getTop()]
    table[label] = []
    a_stmts(env, stmts[1:], table[label])
    return label


def a_stmts(env: Env, ls: list, toSave: list):
    for stmt in ls:
        match stmt[0]:
            case "assign":
                a_assgin(env, stmt, toSave)
            case "augassin":
                a_augassin(env, stmt, toSave)
            case "for":
                a_for(env, stmt, toSave)
            case "function":
                a_func(env, stmt, toSave)
            case "if":
                a_if(env, stmt, toSave)
            case "while":
                a_while(env, stmt, toSave)
            case "import" | "import *":
                a_import(env, stmt, toSave)
            case "export":
                a_export(env, stmt, toSave)
            case "return":
                a_return(env, stmt, toSave)
            case "call":
                a_call(env, stmt, toSave)


def a_assgin(env: Env, ls: list, toSave: list):
    ID = ls[1]["value"]
    label = f"{ID}@{env.label}"
    env.put(ID)
    if isinstance(ls[2], list) and ls[2][0] == "assign":
        id1 = a_assgin(env, ls[2], toSave)
        toSave.append(["m_set", label, id1])
    else:
        exp = a_exp(env, ls[2], toSave, label)
        if exp != label:
            toSave.append(["m_set", label, exp])
    return label


def a_augassin(env: Env, ls: list, toSave: list):
    ID = ls[2]["value"]
    if envLabel := env.get(ID):
        label = f"{ID}@{envLabel}"
        exp = a_exp(env, ls[1:], toSave, label)
        if exp != label:
            toSave.append(["m_set", label, exp])
    else:
        raise NameError(f"变量名'{ID}'未定义")


def a_compare(
    env: Env, ls: list, toSave: list, goto="label", valueMode=False, flipMode=False
):
    OP = ls[0]
    l = a_exp(env, ls[1], toSave)
    r = a_exp(env, ls[2], toSave)
    if valueMode:
        label = next(variableLabelGener)
        toSave.append(["m_operation", OP, label, l, r])
        return label
    else:
        toSave.append(["m_jump", goto, "f" + OP if flipMode else OP, l, r])
        return goto


def a_for(env: Env, ls: list, toSave: list):
    """for assign compare express block"""
    for assign in ls[1]:
        a_assgin(env, assign, toSave)

    link_to = a_block(ls[4])

    # 处理compare
    if len(ls[2]) == 1:  # 只有一个比较
        a_compare(env, ls[2][0], toSave, link_to, flipMode=True)
    else:  # 含有多个比较
        compares = (
            a_compare(env, compare, toSave, valueMode=True) for compare in ls[2]
        )
        label = next(variableLabelGener)
        toSave.append(["m_set", label, "true"])
        for compare in compares:
            toSave.append(["m_operation", "land", label, label, compare])
        toSave.append(["m_jump", link_to, "!=", label, "false"])

    links: list[list[str]] = blocks[env.getTop()][link_to]
    for express in ls[3]:
        a_exp(env, express, links)
    links.append(["m_set", "@counter", str(len(toSave) - 1)])


def a_call(env: Env, ls: list, toSave: list):
    ID = ls[1]
    if ID in Builtins:
        toSave.append([f"m_{ID}", *(a_exp(env, para, toSave) for para in ls[2])])
        return ID
    else:
        neoLabel: str
        if env_label := env.get(ID):
            neoLabel = f"{ID}@{env_label}"
        elif ID in imports:
            neoLabel = f"{ID}@{imports[ID]}"
        else:
            raise NameError(f"函数名'{ID}'未定义")
        func = functions[neoLabel]
        for argu, para in zip(func["argus"], ls[2]):
            label = a_exp(env, para, toSave, argu)
            toSave.append(["m_set", argu, label])
        toSave.append(["m_set", neoLabel + ":back", "label"])
        toSave.append(["m_set", "@counter", func["pos"]])
        return f"{neoLabel}:return"


def a_func(env: Env, ls: list, toSave: list):
    ID = ls[1]["value"]
    env.put(ID)
    neoLabel = f"{ID}@{env.label}"
    argus = []
    for argu in ls[2]:
        argus.append(f"{argu['value']}@{ls[3][0].label}")
        ls[3][0].put(argu["value"])
    ret = []
    a_block(ls[3])
    functions[neoLabel] = {"pos": "label", "argus": argus, "at": env.getTop()}
    toSave.append(["m_set", "@counter", "label"])
    toSave.extend(ret)
    toSave.append(["m_set", "@counter", neoLabel + ":back"])


def a_return(env: Env, ls: list, toSave: list):
    if len(ls) == 3:
        label = a_exp(env, ls[2], toSave)
        toSave.append(["m_set", ls[1] + ":return", label])


def a_elif(env: Env, ls: list, toSave: list):
    """
    elif block compare [else|elif]

    else block
    """
    if ls[0] == "elif":
        if len(ls) == 4:
            compare = []
            elif_block = []
            link_to = a_block(ls[1])
            a_compare(env, ls[2], compare, link_to, flipMode=True)
            a_elif(env, ls[3], elif_block)
            toSave.extend(compare)
            toSave.extend(elif_block)
        else:
            compare = []
            link_to = a_block(ls[1])
            a_compare(env, ls[2], compare, link_to, flipMode=True)
            toSave.extend(compare)
    else:  # ls[0] == 'else'
        a_block(ls[1])


def a_if(env: Env, ls: list, toSave: list):
    """if block compare [else|elif]"""
    if len(ls) == 4:
        compare = []
        elif_block = []
        link_to = a_block(ls[1])
        a_compare(env, ls[2], compare, link_to, flipMode=True)
        a_elif(env, ls[3], elif_block)
        toSave.extend(compare)
        toSave.extend(elif_block)
    else:
        link_to = a_block(ls[1])
        a_compare(env, ls[2], toSave, link_to, flipMode=True)


def a_while(env: Env, ls: list, toSave: list):
    block = []
    a_block(ls[2])
    compare = []
    a_compare(env, ls[1], compare)
    toSave.extend(compare)
    toSave.append(["m_set", "@counter", "label"])
    toSave.extend(block)
    toSave.append(["m_set", "@counter", "label"])


def a_import(env: Env, ls: list, toSave: list):
    where: dict[str, str] = ls[2]
    literal = where["value"]
    if literal[-4:-1] == ".ts":
        return
    if literal[-4:-1] != ".js":
        raise ImportError(
            f"不允许的格式, 错误位于 row: {where['row']}, column: {where['column']}"
        )
    moduleName = path.split(literal[1:-1])[1]
    modulePath = path.join(
        TEST_DIR if len(argv) == 1 else path.split(argv[1])[0], moduleName
    )
    module_ast = syntacticParser(modulePath, Env(moduleName))
    blocks[moduleName] = {}
    table = blocks[moduleName]
    label = next(linkLabelGener)
    table[label] = []
    a_block(module_ast)
    table[label].append("#" + env.getTop())
    module_env = module_ast[0]
    if ls[0] == "import":
        for argu in ls[1]:
            ID = argu["value"]
            if env_label := module_env.get(ID + ":export"):
                imports[ID] = env_label
    else:  # == 'import *'
        # 这个得tmd写a_attrRef()
        pass
    console(module_ast, moduleName)
    console(imports, "imports")


def a_export(env: Env, ls: list, toSave: list):
    for argu in ls[1]:
        env.put(argu["value"] + ":export")


def a_array(env: Env, ls: list, toSave: list, label: str):
    raise InterruptedError("暂不支持'array'功能")


def a_object(env: Env, ls: list, toSave: list, label: str):
    for kvpair in ls[1]:
        if kvpair[0] == "function":
            # id(argus) {}
            a_func(env, kvpair, toSave)
        else:
            # key: value
            key = kvpair[0]["value"]
            neoLabel = f"{key}${label}"
            exp = a_exp(env, kvpair[1], toSave, neoLabel)
            if exp != neoLabel:
                toSave.append(["m_set", neoLabel, exp])


def a_attrRef(env: Env, ls: list, toSave: list, label: str):
    print("暂不支持该功能")


def a_lambda(env: Env, ls: list, toSave: list, label: str):
    ret = []
    env.put(label)
    argus = []
    for argu in ls[1]:
        argus.append(f"{argu['value']}@{ls[2][0].label}")
        ls[2][0].put(argu["value"])
    a_block(ls[2])
    functions[label] = {"pos": "label", "argus": argus}
    toSave.append(["m_set", "@counter", "label"])
    toSave.extend(ret)
    toSave.append(["m_set", "@counter", label + ":back"])


def a_exp(env: Env, ls: list | dict, toSave: list, label="") -> str:
    if isinstance(ls, list):
        if label == "":
            label = next(variableLabelGener)
        id = ls[0]
        match id:
            case "+" | "-" | "*" | "/" | "%" | "&" | "|" | "^" | "&&" | "||" | "**" | "<<" | ">>":
                l = a_exp(env, ls[1], toSave, label)
                r = a_exp(env, ls[2], toSave, label)
                if isNumber(l) and isNumber(r):
                    return str(eval(l + id + r))
                else:
                    toSave.append(["m_operation", OperationMode[id], label, l, r])
            case "factor":
                op = ls[1]
                r = a_exp(env, ls[2], toSave)
                if op == "-":
                    if isNumber(r):
                        return "-" + r
                    toSave.append(["m_operation", "mul", label, r, "-1"])
                elif op == "~":
                    toSave.append(["m_operation", "flip", label, r])
            case "augassin":
                l = a_exp(env, ls[2], toSave, label)
                r = a_exp(env, ls[3], toSave, label)
                toSave.append(["m_operation", OperationMode[ls[1]], l, l, r])
            case "array":
                a_array(env, ls, toSave, label)
            case "object":
                a_object(env, ls, toSave, label)
            case "ref:dot" | "ref:sub":
                a_attrRef(env, ls, toSave, label)
            case "call":
                return a_call(env, ls, toSave)
            case "lambda":
                a_lambda(env, ls, toSave, label)
            case _:
                raise SyntaxError(f"遇到了未支持的方法: '{id}'")
        return label
    else:
        ID = ls["value"]
        if ls["attr"] == "Identity":
            if envLabel := env.get(ID):
                return f"{ID}@{envLabel}"
            raise NameError(f"变量名'{ID}'未定义")
        else:
            return ID


def sematicAnalyzer(path: str):
    AST = syntacticParser(path, Env("main"))
    a_block(AST)
    console(AST, "main AST")
    console(functions, "functions")
    return blocks
