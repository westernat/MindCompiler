from SP import Env, syntacticParser
from tool import labelGener, Builtins, TEST_DIR, DEBUG, isNumber
from pprint import pprint
from sys import argv
from os import path

variableLabelGener = labelGener('t')
linkLabelGener = labelGener('$link')
blocks = {
    'main': {}
}
funcs = {}
imports = {}


def a_block(stmts: list, toSave: list):
    ENV: Env = stmts[0]
    a_stmts(ENV, stmts[1:], toSave)


def a_stmts(env: Env, ls: list, toSave: list):
    for stmt in ls:
        label = next(linkLabelGener)
        table = blocks[env.getTop()]
        table[label] = []
        match stmt[0]:
            case 'assign':
                a_assgin(env, stmt, table[label])
            case 'augassin':
                a_augassin(env, stmt, table[label])
            case 'for':
                a_for(env, stmt, table[label])
            case 'function':
                a_func(env, stmt, table[label])
            case 'if':
                a_if(env, stmt, table[label])
            case 'while':
                a_while(env, stmt, table[label])
            case 'import' | 'import *':
                a_import(env, stmt, table[label])
            case 'export':
                a_export(env, stmt, table[label])
            case 'return':
                a_return(env, stmt, table[label])
            case 'call':
                a_call(env, stmt, table[label])


def a_assgin(env: Env, ls: list, toSave: list):
    ID = ls[1]['value']
    label = f'{ID}@{env.label}'
    env.put(ID)
    if isinstance(ls[2], list) and ls[2][0] == 'assign':
        id1 = a_assgin(env, ls[2], toSave)
        toSave.append(['m_set', label, id1])
    else:
        exp = a_exp(env, ls[2], toSave, label)
        if exp != label:
            toSave.append(['m_set', label, exp])
    return label


def a_augassin(env: Env, ls: list, toSave: list):
    ID = ls[2]['value']
    if envLabel := env.get(ID):
        label = f'{ID}@{envLabel}'
        exp = a_exp(env, ls[1:], toSave, label)
        if exp != label:
            toSave.append(['m_set', label, exp])
    else:
        raise NameError(f"变量名'{ID}'未定义")


def a_compare(env: Env, ls: list, toSave: list, goto=0, valueMode=False):
    OP = ls[0]
    l = a_exp(env, ls[1], toSave)
    r = a_exp(env, ls[2], toSave)
    if valueMode:
        label = next(variableLabelGener)
        toSave.append(['m_operation', label, OP, l ,r])
        return label
    else:
        mode = 'f'+OP if goto < 0 else OP
        toSave.append(['m_jump', -1, mode, l, r])
        return mode


def a_for(env: Env, ls: list, toSave: list):
    fir = []
    for assign in ls[1]:
        a_assgin(env, assign, fir)
    if len(ls[2]) == 1:
        a_compare(env, ls[2][0], fir, -1)
    else:
        cps = (a_compare(env, cp, toSave, valueMode=True) for cp in ls[2])
        label = next(variableLabelGener)
        toSave.append(['m_set', label, 'true'])
        for cp in cps:
            toSave.append(['m_operation', label, 'land', label, cp])
        toSave.append(['m_jump', -1, '!=', label, 'false'])
    bk = []
    a_block(ls[4], bk)
    a_stmts(env, ls[3], bk)
    bk.append(['m_set', '@counter', -1])
    fir.append(['m_set', '@counter', -1])
    toSave.extend(fir)
    toSave.extend(bk)


def a_call(env: Env, ls: list, toSave: list):
    ID = ls[1]
    if ID in Builtins:
        toSave.append([f'm_{ID}', *(a_exp(env, para, toSave) for para in ls[2])])
        return ID
    else:
        neoLabel: str
        if env_label := env.get(ID):
            neoLabel = f"{ID}@{env_label}"
        elif ID in imports:
            neoLabel = f"{ID}@{imports[ID]}"
        else:
            raise NameError(f"函数名'{ID}'未定义")
        func = funcs[neoLabel]
        for argu, para in zip(func['argus'], ls[2]):
            label = a_exp(env, para, toSave, argu)
            toSave.append(['m_set', argu, label])
        toSave.append(['m_set', neoLabel+':back', -1])
        toSave.append(['m_set', '@counter', func['pos']])
        return f"{neoLabel}:return"


def a_func(env: Env, ls: list, toSave: list):
    ID = ls[1]['value']
    env.put(ID)
    neoLabel = f'{ID}@{env.label}'
    argus = []
    for argu in ls[2]:
        argus.append(f"{argu['value']}@{ls[3][0].label}")
        ls[3][0].put(argu['value'])
    ret = []
    a_block(ls[3], ret)
    funcs[neoLabel] = {
        'pos': -1,
        'argus': argus,
        'at': env.getTop()
    }
    toSave.append(['m_set', '@counter', -1])
    toSave.extend(ret)
    toSave.append(['m_set', '@counter', neoLabel+':back'])


def a_return(env: Env, ls: list, toSave: list):
    if len(ls) == 3:
        label = a_exp(env, ls[2], toSave)
        toSave.append(['m_set', ls[1]+':return', label])


def a_elif(env: Env, ls: list, toSave: list):
    if ls[0] == 'elif':
        if len(ls) == 4:
            cp = []
            a_compare(env, ls[1], cp)
            bk = []
            a_block(ls[2], bk)
            ef = []
            out = a_elif(env, ls[3], ef)
            toSave.extend(cp)
            toSave.append(['m_set', '@counter', -1])
            toSave.extend(bk)
            toSave.append(['m_set', '@counter', out])
            toSave.extend(ef)
            return out
        else:
            cp = []
            a_compare(env, ls[1], cp)
            bk = []
            a_block(ls[2], bk)
            toSave.extend(cp)
            toSave.append(['m_set', '@counter', -1])  # out
            toSave.extend(bk)
            return -1
    else:
        a_block(ls[1], toSave)
        return -1


def a_if(env: Env, ls: list, toSave: list):
    if len(ls) == 4:
        cp = []
        a_compare(env, ls[1], cp)
        bk = []
        a_block(ls[2], bk)
        ef = []
        out = a_elif(env, ls[3], ef)
        toSave.extend(cp)
        toSave.append(['m_set', '@counter', -1])  # next
        toSave.extend(bk)
        toSave.append(['m_set', '@counter', out])
        toSave.extend(ef)
    else:
        bk = []
        a_block(ls[2], bk)
        a_compare(env, ls[1], toSave, -1)
        toSave.extend(bk)


def a_while(env: Env, ls: list, toSave: list):
    bk = []
    a_block(ls[2], bk)
    cp = []
    a_compare(env, ls[1], cp)
    toSave.extend(cp)
    toSave.append(['m_set', '@counter', -1])
    toSave.extend(bk)
    toSave.append(['m_set', '@counter', -1])


def a_import(env: Env, ls: list, toSave: list):
    where: dict[str, str] = ls[2]
    literal = where['value']
    if (literal[-4:-1] == '.ts'):
        return
    if (literal[-4:-1] != ".js"):
        raise ImportError(
            f"不允许的格式, 错误位于 row: {where['row']}, column: {where['column']}")
    moduleName = path.split(literal[1:-1])[1]
    modulePath = path.join(TEST_DIR if len(argv) == 1 else path.split(argv[1])[0], moduleName)
    module_ast = syntacticParser(modulePath, Env(moduleName))
    blocks[moduleName] = {}
    table = blocks[moduleName]
    label = next(linkLabelGener)
    table[label] = []
    a_block(module_ast, table[label])
    table[label].append('#'+env.getTop())
    module_env = module_ast[0]
    if (ls[0] == 'import'):
        for argu in ls[1]:
            ID = argu['value']
            if env_label := module_env.get(ID+":export"):
                imports[ID] = env_label
    else:  # == 'import *'
        # 这个得tmd写a_attrRef()
        pass
    if DEBUG:
        print(moduleName.center(20, '='))
        pprint(module_ast)
        print("imports".center(20, '='))
        pprint(imports)


def a_export(env: Env, ls: list, toSave: list):
    for argu in ls[1]:
        env.put(argu['value']+":export")


def a_array(env: Env, ls: list, toSave: list, label: str):
    raise InterruptedError("暂不支持'array'功能")


def a_object(env: Env, ls: list, toSave: list, label: str):
    for kvpair in ls[1]:
        if kvpair[0] == 'function':
            # id(argus) {}
            a_func(env, kvpair, toSave)
        else:
            # key: value
            key = kvpair[0]['value']
            neoLabel = f"{key}${label}"
            exp = a_exp(env, kvpair[1], toSave, neoLabel)
            if exp != neoLabel:
                toSave.append(['m_set', neoLabel, exp])


def a_attrRef(env: Env, ls: list, toSave: list, label: str):
    print('暂不支持该功能')


def a_lambda(env: Env, ls: list, toSave: list, label: str):
    ret = []
    env.put(label)
    argus = []
    for argu in ls[1]:
        argus.append(f"{argu['value']}@{ls[2][0].label}")
        ls[2][0].put(argu['value'])
    a_block(ls[2], ret)
    funcs[label] = {'pos': -1, 'argus': argus}
    toSave.append(['m_set', '@counter', -1])
    toSave.extend(ret)
    toSave.append(['m_set', '@counter', label+':back'])


def a_exp(env: Env, ls: list | dict, toSave: list, label='') -> str:
    if isinstance(ls, list):
        if label == '':
            label = next(variableLabelGener)
        match ls[0]:
            case '+' | '-' | '*' | '/' | '%' | '&' | '|' | '^' | '&&' | '||' | '<<' | '>>':
                l = a_exp(env, ls[1], toSave, label)
                r = a_exp(env, ls[2], toSave, label)
                if isNumber(l) and isNumber(r):
                    return str(eval(l+ls[0]+r))
                else:
                    toSave.append(['m_operation', label, ls[0], l, r])
            case 'factor':
                op = ls[1]
                r = a_exp(env, ls[2], toSave)
                if op in '+-':
                    if isNumber(r):
                        return op+r
                    toSave.append(['m_operation', label, 'mul', r, op+'1'])
                else:
                    toSave.append(['m_operation', label, 'flip', r])
            case 'array':
                a_array(env, ls, toSave, label)
            case 'object':
                a_object(env, ls, toSave, label)
            case 'ref:dot' | 'ref:sub':
                a_attrRef(env, ls, toSave, label)
            case 'call':
                return a_call(env, ls, toSave)
            case 'lambda':
                a_lambda(env, ls, toSave, label)
            case _:
                raise SyntaxError(f"遇到了未支持的方法: '{ls[0]}'")
        return label
    else:
        ID = ls['value']
        if ls['attr'] == 'Identity':
            if envLabel := env.get(ID):
                return f"{ID}@{envLabel}"
            raise NameError(f"变量名'{ID}'未定义")
        else:
            return ID


def sematicAnalyzer(path: str):
    AST = syntacticParser(path, Env('main'))
    label = next(linkLabelGener)
    table = blocks['main']
    table[label] = []
    a_block(AST, table[label])
    table[label].append(['m_stop'])
    if DEBUG:
        print('main AST'.center(20, '='))
        pprint(AST)
        print('funcs'.center(20, '='))
        pprint(funcs)
        print('blocks'.center(20, '='))
        for part in blocks:
            block = blocks[part]
            print(f"{part}:")
            for links in block:
                print(f"    {links}:")
                for link in block[links]:
                    print(f"        {link}")
    return blocks
