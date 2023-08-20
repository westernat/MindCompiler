from LA import lexicalAnalyzer
from tool import labelGener, DEBUG


def error(index: int):
    token = tokens[index-1]
    return f", 错误位于 row: {token['row']}, column: {token['column']}"


LG = labelGener('B')
funcQueue: list[str] = []


class Env:
    def __init__(self, prev):
        self.table = []
        self.prev = prev
        self.label = next(LG)

    def put(self, value: str):
        self.table.append(value)

    def get(self, key: str):
        if key in self.table:
            return self.label
        prev = self.prev
        while isinstance(prev, Env):
            if key in prev.table:
                return prev.label
            prev = prev.prev
        return False
    
    def getTop(self) -> str:
        prev = self.prev
        while isinstance(prev, Env):
            prev = prev.prev
        return prev


def p_match(input: str):
    global index
    if index < len(tokens):
        this = tokens[index]
        if input == this['value']:
            index += 1
            return input
    return


def p_next(input: str):
    global index
    if (index+1) < len(tokens) and input == tokens[index+1]['value']:
        return input
    return


def p_attr(input: str):
    global index
    if index < len(tokens):
        this = tokens[index]
        if input == this['attr']:
            index += 1
            return this
    return


def p_argus():
    ret = [p_attr('Identity')]
    while p_match(','):
        ret.append(p_attr('Identity'))
    return list(_ for _ in ret if _ != None)


def p_paras():
    ret = [p_exp()]
    while p_match(','):
        ret.append(p_exp())
    return list(_ for _ in ret if _ != None)


def p_string():
    global index
    this = tokens[index]
    if 'Str' in this['attr']:
        index += 1
        if this['attr'] == 'SingleStrEnd':
            this['value'] = '"'+this['value'][1:-1]+'"'
            return this
        if this['attr'] == 'FormatStrEnd':
            raise TypeError("暂不支持Format字符串" + error(index))
        return this
    return


def p_atom():
    global index
    c = index
    if p_match('('):
        exp = p_exp()
        if p_match(')'):
            return exp
        raise SyntaxError("缺少')'" + error(index))
    # call
    if (id1 := p_attr('Identity')) and p_match('('):
        paras = p_paras()
        if p_match(')'):
            return ['call', id1['value'], paras]
        raise SyntaxError("缺少')'" + error(index))
    index = c
    if or3 := (p_attr('Number') or
               p_string() or
               p_attr('Identity') or
               p_attr('Boolean')):
        return or3
    index = c
    # array
    if p_match('['):
        paras = p_paras()
        if p_match(']'):
            return ['array', paras]
        raise SyntaxError("缺少']'" + error(index))
    # object
    if p_match('{'):
        kvpairs = [p_kvpair()]
        while p_match(',') and (kv := p_kvpair()):
            kvpairs.append(kv)
        if p_match('}'):
            return ['object', kvpairs]
        raise SyntaxError("缺少'}'" + error(index))
    return


def p_kvpair():
    global index
    c = index
    if p_next(':'):
        if key := (p_attr('Identity') or p_string()):
            index += 1
            if value := p_exp():
                return [key, value]
        raise SyntaxError("键值对错误" + error(index))
    if (id1 := p_attr('Identity')) and p_match('('):
        argus = p_argus()
        if p_match(')') and (block := Block(prev_env)):
            return ['function', id1, argus, block]
    index = c
    return


def p_primary():
    return p_atom()
    # p_subscription()
    # slicing()


def p_power():
    cache = p_primary()
    while p_match('**'):
        cache = ['**', cache, p_primary()]
    return cache


def p_factor():
    cache = p_power()
    while op := (p_match('+') or p_match('-') or p_match('~')):
        cache = [op, cache, p_power()]
    return cache


def p_term():
    cache = p_factor()
    while op := p_attr('TermOp'):
        cache = [op['value'], cache, p_factor()]
    return cache


def p_sum():
    cache = p_term()
    while op := (p_match('+') or p_match('-')):
        cache = [op, cache, p_term()]
    return cache


def p_shiftOp():
    cache = p_sum()
    while op := p_attr('ShiftOp'):
        cache = [op['value'], cache, p_sum()]
    return cache


def p_bitOp():
    cache = p_shiftOp()
    while op := p_attr('BitOp'):
        cache = [op['value'], cache, p_shiftOp()]
    return cache


def p_compareOp():
    cache = p_bitOp()
    while op := p_attr('CompareOp'):
        cache = [op['value'], cache, p_bitOp()]
    return cache


def p_inversion():
    if p_match('!'):
        return ['!', p_compareOp()]
    return p_compareOp()


def p_binaryOp():
    cache = p_inversion()
    while op := p_attr('BinaryOp'):
        cache = [op['value'], cache, p_inversion()]
    return cache


def p_attrRef():
    global index
    c = index
    if (pri := p_primary()):
        if p_match('.'):
            return ['ref:dot', pri, p_exp()]
        if p_match('[') and (str1 := p_string()) and p_match(']'):
            return ['ref:sub', pri, str1]
    index = c
    return


def p_lambda():
    global index
    c = index
    if p_match('function') and p_match('('):
        argus = p_argus()
        if p_match(')') and (block := Block(prev_env)):
            return ['lambda', argus, block]
        raise SyntaxError("不符合'lambda'函数的语法" + error(index))
    if p_match('('):
        argus = p_argus()
        if p_match(')') and p_match('=>'):
            if block := Block(prev_env):
                return ['lambda', argus, block]
            raise SyntaxError("'=>'后缺少语句块" + error(index))
    index = c
    if p_next('=>'):
        if id1 := p_attr('Identity'):
            index += 1
            if block := Block(prev_env):
                return ['lambda', id1, block]
            raise SyntaxError("'=>'后缺少语句块" + error(index))
        raise SyntaxError("'=>'前不是标识符" + error(index))
    return


def p_exp():
    return p_lambda() or p_attrRef() or p_binaryOp()


def p_assign():
    global index
    c = index
    if p_match('let') and (id1 := p_attr('Identity')) and p_match('='):
        if exp := p_exp():
            return ['assign', id1, exp]
        raise SyntaxError("你要'let'什么" + error(index))
    if (id1 := p_attr('Identity')) and p_match('='):
        if stmt := p_stmt():
            return ['assign', id1, stmt]
        raise SyntaxError("没有值可以赋" + error(index))
    index = c
    if (id1 := p_attr('Identity')) and (op := p_attr('Augassin')):
        if exp := p_exp():
            return ['augassin', op['value'][:-1], id1, exp]
        raise SyntaxError("没有值可以赋" + error(index))
    index = c
    return


def p_return():
    if p_match('return'):
        if len(funcQueue) > 0:
            return ['return', funcQueue.pop(), p_exp()]
        return ['return', None]
    return


def p_import():
    if p_match('import'):
        if p_match('{'):
            argus = p_argus()
            if p_match('}') and p_match('from') and (where := p_string()):
                return ['import', argus, where]
        if p_match('*') and p_match('as') and (id1 := p_attr('Identity')) and \
                p_match('from') and (where := p_string()):
            return ['import *', id1, where]
        raise SyntaxError("不符合'import'语法" + error(index))
    return


def p_export():
    if p_match('export'):
        if p_match('{'):
            argus = p_argus()
            if p_match('}'):
                return ['export', argus]
        raise SyntaxError("不符合'export'语法" + error(index))
    return


def p_symStmt():
    return p_assign() or \
        p_return() or \
        p_import() or \
        p_export()


def p_func():
    if p_match('function'):
        if (id1 := p_attr('Identity')) and p_match('('):
            argus = p_argus()
            funcQueue.append(f"{id1['value']}@{prev_env.label}")
            if p_match(')') and (block := Block(prev_env)):
                return ['function', id1, argus, block]
        raise SyntaxError("不符合'function'语法" + error(index))
    return


def p_else():
    if p_match('else'):
        if block := Block(prev_env):
            return ['else', block]
        raise SyntaxError("'else'后未接语句块" + error(index))
    return


def p_elif():
    global index
    c = index
    if p_match('else') and p_match('if') and p_match('('):
        if (compare := p_binaryOp()) and p_match(')'):
            if block := Block(prev_env):
                ret = ['elif', block, compare]
                elif_block, hasElse = p_elif()
                if elif_block:
                    ret.append(elif_block)
                if not hasElse and (el := p_else()):
                    ret.append(el)
                return ret, True
            raise SyntaxError("'else if'后未接语句块" + error(index))
        raise SyntaxError("条件语句错误" + error(index))
    index = c
    return None, False


def p_if():
    if p_match('if') and p_match('('):
        if (compare := p_binaryOp()) and p_match(')'):
            if block := Block(prev_env):
                ret = ['if', block, compare]
                elif_block, hasElse = p_elif()
                if elif_block:
                    ret.append(elif_block)
                if not hasElse and (el := p_else()):
                    ret.append(el)
                return ret
            raise SyntaxError("'if'后未接语句块" + error(index))
        raise SyntaxError("条件语句错误" + error(index))
    return


def p_for():
    if p_match('for') and p_match('('):
        ret = ['for', [], [], []]
        if ag1 := p_assign():
            ret[1].append(ag1)
            while p_match(',') and (ag2 := p_assign()):
                ret[1].append(ag2)
        if p_match(';'):
            if compare1 := p_binaryOp():
                ret[2].append(compare1)
                while p_match(',') and (compare2 := p_binaryOp()):
                    ret[2].append(compare2)
        else:
            raise SyntaxError("缺少第一个';'" + error(index))
        if p_match(';'):
            if stmt1 := p_stmt():
                ret[3].append(stmt1)
                while p_match(',') and (stmt2 := p_stmt()):
                    ret[3].append(stmt2)
        else:
            raise SyntaxError("缺少第二个';'" + error(index))
        if p_match(')') and (block := Block(prev_env)):
            ret.append(block)
            return ret
        raise SyntaxError("'for'后未接语句块" + error(index))
    return


def p_while():
    if p_match('while') and p_match('('):
        if (compare := p_binaryOp()) and p_match(')'):
            if block := Block(prev_env):
                return ['while', compare, block]
            raise SyntaxError("'while'后未接语句块" + error(index))
        raise SyntaxError("缺少条件判断语句" + error(index))
    return


def p_comStmt():
    return p_func() or \
        p_if() or \
        p_for() or \
        p_while()


def p_stmt():
    return p_symStmt() or \
        p_comStmt() or \
        p_exp()


class Block:
    def __new__(cls, env) -> list:
        global prev_env
        if p_match('{'):
            stmts = []
            prev_env = Env(env)
            stmts.append(prev_env)
            while stmt := p_stmt():
                stmts.append(stmt)
                p_match(';')
            if p_match('}'):
                return stmts
            raise SyntaxError("缺少'}'" + error(index))
        prev_env = env
        if stmt := p_stmt():
            return [stmt]
        raise SyntaxError("未匹配任何有效语法" + error(index))


def syntacticParser(path: str, top: Env):
    global tokens, index
    index = 0
    AST = [top]
    with open(path, 'r', encoding='utf-8') as Js:
        tokens = lexicalAnalyzer(Js.read())
    while index < len(tokens):
        AST.extend(Block(top))
        p_match(';')
    return AST
