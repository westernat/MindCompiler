from SP import Env, syntacticParser
from lib import *

def a_labelGener():
    counter = 0
    while True:
        yield f't{counter}'
        counter += 1


LG = a_labelGener()
blocks = []
funcs = {}
imports = {}


def a_block(stmts: list, toSave: list, th=0):
    ENV: Env = stmts[0]
    a_stmts(ENV, stmts[1:], toSave, th)


def a_stmts(env: Env, ls: list, toSave: list, th=0):
    for stmt in ls:
        match stmt[0]:
            case 'assign':
                a_assgin(env, stmt, toSave)
            case 'augassin':
                a_augassin(env, stmt, toSave)
            case 'for':
                a_for(env, stmt, toSave, th)
            case 'call':
                a_call(env, stmt, toSave, th)
            case 'function':
                a_func(env, stmt, toSave, th)
            case 'if':
                a_if(env, stmt, toSave, th)
            case 'while':
                a_while(env, stmt, toSave, th)
            case 'import':
                a_import(env, stmt, toSave)
            case 'array':
                a_array(env, stmt, toSave)
            case 'object':
                a_object(env, stmt, toSave)
            case 'ref:dot' | 'ref:sub':
                a_attrRef(env, stmt, toSave)
    return env.label


def a_assgin(env: Env, ls: list, toSave: list):
    ID = ls[1]['value']
    label = f'{ID}@{env.label}'
    env.put(ID)
    if isinstance(ls[2], list) and ls[2][0] == 'assign':
        id1 = a_assgin(env, ls[2], toSave)
        toSave.append(m_set(label, id1))
    else:
        EXP = a_exp(env, ls[2], toSave, label)
        if EXP != label:
            toSave.append(m_set(label, EXP))
    return label


def a_augassin(env: Env, ls: list, toSave: list):
    ID = ls[2]['value']
    if envLabel := env.get(ID):
        label = f'{ID}@{envLabel}'
        EXP = a_exp(env, ls[1:], toSave, label)
        if EXP != label:
            toSave.append(m_set(label, EXP))
    else:
        raise NameError(f"变量名'{ID}'未定义")


def a_compare(env: Env, ls: list, toSave: list, goto=0, valueMode=False):
    OP = ls[0]
    l = a_exp(env, ls[1], toSave)
    r = a_exp(env, ls[2], toSave)
    if valueMode:
        label = next(LG)
        toSave.append(m_operation(label, JumpMode[OP], l, r))
        return label
    else:
        mode = JumpMode['f'+OP] if goto < 0 else JumpMode[OP]
        toSave.append(m_jump(len(toSave)+abs(goto), mode, l, r))
        return mode


def a_for(env: Env, ls: list, toSave: list, th: int):
    for assign in ls[1]:
        a_assgin(env, assign, toSave)
    start = th+len(toSave)+1
    if len(ls[2]) == 1:
        a_compare(env, ls[2][0], toSave, th+len(toSave)+1)
    else:
        cps = (a_compare(env, cp, toSave, valueMode=True) for cp in ls[2])
        label = next(LG)
        toSave.append(m_set(label, 'true'))
        for cp in cps:
            toSave.append(m_operation(label, 'land', label, cp))
        toSave.append(m_jump(th+1, '!=', label, 'false'))
    ret = []
    a_block(ls[4], ret, th)
    a_stmts(env, ls[3], ret)
    ret.append(f'set @counter {start}')
    toSave.append(f'set @counter {th+len(toSave)+len(ret)+1}')
    toSave.extend(ret)


def a_call(env: Env, ls: list, toSave: list, th: int):
    ID = ls[1]
    if ID in Builtins:
        paras = tuple(a_exp(env, para, toSave) for para in ls[2])
        toSave.append(eval(f'm_{ID}{paras}'))
    else:
        if env.get(ID):
            func = funcs[f"{ID}@{env.label}"]
            for argu, para in zip(func['argus'], ls[2]):
                label = a_exp(env, para, toSave, argu)
                toSave.append(f'set {argu} {label}')
            toSave.append(f'set {ID}:back {th+len(toSave)+2}')
            toSave.append(f"set @counter {func['pos']}")
        else:
            raise NameError(f"函数名'{ID}'未定义")


def a_func(env: Env, ls: list, toSave: list, th: int):
    ret = []
    ID = ls[1]['value']
    env.put(ID)
    argus = []
    for argu in ls[2]:
        argus.append(f"{argu['value']}@{ls[3][0].label}")
        ls[3][0].put(argu['value'])
    a_block(ls[3], ret, th+1)
    funcs[f'{ID}@{env.label}'] = {'pos': th+1, 'argus': argus}
    toSave.append(f'set @counter {th+len(toSave)+len(ret)+2}')
    toSave.extend(ret)
    toSave.append(f'set @counter {ID}:back')


def a_elif(env: Env, ls: list, toSave: list, th: int):
    if ls[0] == 'elif':
        bk = []
        a_block(ls[2], bk)
        if len(ls) == 4:
            ef = []
            a_compare(env, ls[1], toSave, th+len(bk)+1)
            next = th+len(toSave)+len(bk)+2
            out = a_elif(env, ls[3], ef, next)
            toSave.append(f'set @counter {next}')
            toSave.extend(bk)
            toSave.append(f'set @counter {out}')
            toSave.extend(ef)
            return out
        else:
            a_compare(env, ls[1], toSave, th+len(bk)+1)
            toSave.append(f'set @counter {th+len(toSave)+len(bk)+1}')  # out
            toSave.extend(bk)
            return th+len(toSave)
    else:
        a_block(ls[1], toSave)
        return th+len(toSave)


def a_if(env: Env, ls: list, toSave: list, th=0):
    bk = []
    a_block(ls[2], bk, th+len(toSave)+1)
    if len(ls) == 4:
        ef = []
        a_compare(env, ls[1], toSave, th+len(bk)+1)
        next = len(toSave)+len(bk)+2
        out = a_elif(env, ls[3], ef, next)
        toSave.append(f'set @counter {next}')  # next
        toSave.extend(bk)
        toSave.append(f'set @counter {out}')
        toSave.extend(ef)
    else:
        a_compare(env, ls[1], toSave, -th-len(bk)-1)
        toSave.extend(bk)


def a_while(env: Env, ls: list, toSave: list, th=0):
    bk = []
    start = len(toSave)
    a_block(ls[2], bk)
    a_compare(env, ls[1], toSave, len(bk)+1)
    toSave.append(f'set @counter {len(toSave)+len(bk)+2}')
    toSave.extend(bk)
    toSave.append(f'set @counter {start}')


def a_import(env: Env, ls: list, toSave: list):
    if ls[1] == '*':
        ID = ls[3]
        env.put(ID)
        where = ls[4]
    else:
        for argu in ls[1]:
            env.put(argu)
        where = ls[2]


def a_array(env: Env, ls: list, toSave: list):
    pass


def a_object(env: Env, ls: list, toSave: list):
    pass


def a_attrRef(env: Env, ls: list, toSave: list):
    pass


def a_exp(env: Env, ls: list | dict, toSave: list, label='') -> str:
    if isinstance(ls, list):
        OP = ls[0]
        if label == '':
            label = next(LG)
        if OP in ('+', '-', '*', '/', '%', '&', '|', '^', '&&', '||', '<<', '>>'):
            l = a_exp(env, ls[1], toSave, label)
            r = a_exp(env, ls[2], toSave, label)
            if l.isnumeric() and r.isnumeric():
                return str(eval(l+OP+r))
            else:
                toSave.append(m_operation(label, OperationMode[OP], l, r))
                return label
        elif OP == 'factor':
            op = ls[1]
            r = a_exp(env, ls[2], toSave)
            if op in '+-':
                if r.isnumeric():
                    return eval(op+r)
                else:
                    toSave.append(m_operation(label, 'mul', r, op+'1'))
            else:
                toSave.append(m_operation(label, 'flip', r))
            return label
        else:
            raise SyntaxError(f"遇到了未支持的方法: '{OP}'")
    else:
        ID = ls['value']
        if ls['attr'] == 'Identity':
            if envLabel := env.get(ID):
                return f"{ID}@{envLabel}"
            raise NameError(f"变量名'{ID}'未定义")
        else:
            return ID


def sematicAnalyzer(path: str, compiler):
    imports['compiler'] = compiler
    imports['main'] = path
    AST = syntacticParser(path)
    a_block(AST, blocks)
    blocks.append('stop')
    print('AST'.center(20, '='))
    print(AST)
    print('blocks'.center(20, '='))
    for stmt in blocks:
        print(stmt)
    print('funcs'.center(20, '='))
    for load in funcs:
        print(load, funcs[load])
    print('imports'.center(20, '='))
    for load in imports:
        print(load, imports[load])
