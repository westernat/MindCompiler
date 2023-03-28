from SP import Env, syntacticParser
from lib import *
from pprint import pprint


def a_labelGener():
    counter = 0
    while True:
        yield f't{counter}'
        counter += 1


LG = a_labelGener()
blocks = []
funcs = {}


def a_block(stmts: list, toSave: list, th=0):
    ENV: Env = stmts[0]
    a_stmts(ENV, stmts[1:], toSave, th)


def a_stmts(env: Env, ls: list, toSave: list, th: int):
    for stmt in ls:
        match stmt[0]:
            case 'assign':
                a_assgin(env, stmt, toSave)
            case 'augassin':
                a_augassin(env, stmt, toSave)
            case 'for':
                a_for(env, stmt, toSave, th+len(toSave))
            case 'function':
                a_func(env, stmt, toSave, th+len(toSave))
            case 'if':
                a_if(env, stmt, toSave, th+len(toSave))
            case 'while':
                a_while(env, stmt, toSave, th+len(toSave))
            case 'import':
                a_import(env, stmt, toSave)
            case 'return':
                a_return(env, stmt, toSave)
            case 'call':
                a_call(env, stmt, toSave)


def a_assgin(env: Env, ls: list, toSave: list):
    ID = ls[1]['value']
    label = f'{ID}@{env.label}'
    env.put(ID)
    if isinstance(ls[2], list) and ls[2][0] == 'assign':
        id1 = a_assgin(env, ls[2], toSave)
        toSave.append(m_set(label, id1))
    else:
        exp = a_exp(env, ls[2], toSave, label, len(toSave))
        if exp != label:
            toSave.append(m_set(label, exp))
    return label


def a_augassin(env: Env, ls: list, toSave: list):
    ID = ls[2]['value']
    if envLabel := env.get(ID):
        label = f'{ID}@{envLabel}'
        exp = a_exp(env, ls[1:], toSave, label)
        if exp != label:
            toSave.append(m_set(label, exp))
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
    fir = []
    for assign in ls[1]:
        a_assgin(env, assign, fir)
    if len(ls[2]) == 1:
        a_compare(env, ls[2][0], fir, th+2)
    else:
        cps = (a_compare(env, cp, toSave, valueMode=True) for cp in ls[2])
        label = next(LG)
        toSave.append(m_set(label, 'true'))
        for cp in cps:
            toSave.append(m_operation(label, 'land', label, cp))
        toSave.append(m_jump(th+1, '!=', label, 'false'))
    start = th+len(fir)-1
    bk = []
    a_block(ls[4], bk, th+len(fir)+1)
    a_stmts(env, ls[3], bk, th+len(fir)+1)
    bk.append(f'set @counter {start}')
    fir.append(f'set @counter {th+len(fir)+len(bk)+1}')
    toSave.extend(fir)
    toSave.extend(bk)


def a_call(env: Env, ls: list, toSave: list):
    ID = ls[1]
    if ID in Builtins:
        paras = tuple(a_exp(env, para, toSave) for para in ls[2])
        toSave.append(eval(f'm_{ID}{paras}'))
        return ID
    else:
        if env.get(ID):
            neoLabel = f"{ID}@{env.label}"
            func = funcs[neoLabel]
            for argu, para in zip(func['argus'], ls[2]):
                label = a_exp(env, para, toSave, argu)
                toSave.append(f'set {argu} {label}')
            toSave.append(f'set {neoLabel}:bak {len(toSave)+2}')
            toSave.append(f"set @counter {func['pos']}")
            return neoLabel+':ret'
        else:
            raise NameError(f"函数名'{ID}'未定义")


def a_func(env: Env, ls: list, toSave: list, th: int):
    ID = ls[1]['value']
    env.put(ID)
    neoLabel = f'{ID}@{env.label}'
    argus = []
    for argu in ls[2]:
        argus.append(f"{argu['value']}@{ls[3][0].label}")
        ls[3][0].put(argu['value'])
    ret = []
    a_block(ls[3], ret, th+1)
    funcs[neoLabel] = {'pos': th+1, 'argus': argus}
    toSave.append(f'set @counter {th+len(ret)+2}')
    toSave.extend(ret)
    toSave.append(f'set @counter {neoLabel}:bak')


def a_return(env: Env, ls: list, toSave: list):
    if len(ls) == 3:
        label = a_exp(env, ls[2], toSave, th=len(toSave))
        toSave.append(f"set {ls[1]}:ret {label}")


def a_elif(env: Env, ls: list, toSave: list, th: int):
    if ls[0] == 'elif':
        if len(ls) == 4:
            cp = []
            a_compare(env, ls[1], cp, th+2)
            bk = []
            a_block(ls[2], bk)
            ef = []
            next = th+len(cp)+len(bk)+2
            out = a_elif(env, ls[3], ef, next)
            toSave.extend(cp)
            toSave.append(f'set @counter {next}')
            toSave.extend(bk)
            toSave.append(f'set @counter {out}')
            toSave.extend(ef)
            return out
        else:
            cp = []
            a_compare(env, ls[1], cp, th+2)
            bk = []
            a_block(ls[2], bk)
            toSave.extend(cp)
            toSave.append(f'set @counter {th+3}')  # out
            toSave.extend(bk)
            return th+3
    else:
        a_block(ls[1], toSave)
        return th+2


def a_if(env: Env, ls: list, toSave: list, th=0):
    if len(ls) == 4:
        cp = []
        a_compare(env, ls[1], cp, th+2)
        bk = []
        a_block(ls[2], bk, th+1)
        ef = []
        next = th+len(cp)+len(bk)+2
        out = a_elif(env, ls[3], ef, next)
        toSave.extend(cp)
        toSave.append(f'set @counter {next}')  # next
        toSave.extend(bk)
        toSave.append(f'set @counter {out}')
        toSave.extend(ef)
    else:
        bk = []
        a_block(ls[2], bk, th+1)
        a_compare(env, ls[1], toSave, -th-len(bk)-1)
        toSave.extend(bk)


def a_while(env: Env, ls: list, toSave: list, th: int):
    bk = []
    a_block(ls[2], bk, th)
    cp = []
    a_compare(env, ls[1], cp, th+2)
    toSave.extend(cp)
    toSave.append(f'set @counter {th+len(cp)+len(bk)+2}')
    toSave.extend(bk)
    toSave.append(f'set @counter {th}')


def a_import(env: Env, ls: list, toSave: list):
    print('暂不支持该功能')


def a_array(env: Env, ls: list, toSave: list, label: str):
    print('暂不支持该功能')


def a_object(env: Env, ls: list, toSave: list, label: str):
    for kvpair in ls[1]:
        if kvpair[0] == 'function':
            # id(argus) {}
            a_func(env, kvpair, toSave, len(toSave))
        else:
            # key: value
            key = kvpair[0]['value']
            neoLabel = f"{key}${label}"
            exp = a_exp(env, kvpair[1], toSave, neoLabel)
            if exp != neoLabel:
                toSave.append(m_set(neoLabel, exp))


def a_attrRef(env: Env, ls: list, toSave: list, label: str):
    print('暂不支持该功能')


def a_lambda(env: Env, ls: list, toSave: list, label: str, th: int):
    ret = []
    env.put(label)
    argus = []
    for argu in ls[1]:
        argus.append(f"{argu['value']}@{ls[2][0].label}")
        ls[2][0].put(argu['value'])
    a_block(ls[2], ret, th+1)
    funcs[label] = {'pos': th+len(ret), 'argus': argus}
    toSave.append(f'set @counter {th+len(toSave)+len(ret)+2}')
    toSave.extend(ret)
    toSave.append(f'set @counter {label}:bak')


def a_exp(env: Env, ls: list | dict, toSave: list, label='', th=0) -> str:
    if isinstance(ls, list):
        if label == '':
            label = next(LG)
        match ls[0]:
            case '+' | '-' | '*' | '/' | '%' | '&' | '|' | '^' | '&&' | '||' | '<<' | '>>':
                l = a_exp(env, ls[1], toSave, label)
                r = a_exp(env, ls[2], toSave, label)
                if l.isnumeric() and r.isnumeric():
                    return str(eval(l+ls[0]+r))
                else:
                    toSave.append(m_operation(
                        label, OperationMode[ls[0]], l, r))
            case 'factor':
                op = ls[1]
                r = a_exp(env, ls[2], toSave)
                if op in '+-':
                    if r.isnumeric():
                        return eval(op+r)
                    toSave.append(m_operation(label, 'mul', r, op+'1'))
                else:
                    toSave.append(m_operation(label, 'flip', r))
            case 'array':
                a_array(env, ls, toSave, label)
            case 'object':
                a_object(env, ls, toSave, label)
            case 'ref:dot' | 'ref:sub':
                a_attrRef(env, ls, toSave, label)
            case 'call':
                return a_call(env, ls, toSave)
            case 'lambda':
                a_lambda(env, ls, toSave, label, th)
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
    AST = syntacticParser(path)
    a_block(AST, blocks)
    blocks.append('stop')
    # print('AST'.center(20, '='))
    # pprint(AST)
    print('blocks'.center(20, '='))
    for i in range(len(blocks)):
        # print(f'{i}:  ', end='')
        print(blocks[i])
    # print('funcs'.center(20, '='))
    # pprint(funcs)
