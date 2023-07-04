from LA import lexicalAnalyzer


def error(index: int):
    token = tokens[index-1]
    return f", 错误位于 row: {token['row']}, column: {token['column']}"


def p_labelGener():
    counter = 0
    while True:
        yield f'B{counter}'
        counter += 1


LG = p_labelGener()


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


index = 0
TOP = Env(None)
AST = [TOP]


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


def p_paras(env: Env):
    ret = [p_exp(env)]
    while p_match(','):
        ret.append(p_exp(env))
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


def p_atom(env: Env):
    global index
    c = index
    if p_match('('):
        exp = p_exp(env)
        if p_match(')'):
            return exp
        raise SyntaxError("缺少')'" + error(index))
    # call
    if (id1 := p_attr('Identity')) and p_match('('):
        paras = p_paras(env)
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
        paras = p_paras(env)
        if p_match(']'):
            return ['array', paras]
        raise SyntaxError("缺少']'" + error(index))
    # object
    if p_match('{'):
        kvpairs = [p_kvpair(env)]
        while p_match(',') and (kv := p_kvpair(env)):
            kvpairs.append(kv)
        if p_match('}'):
            return ['object', kvpairs]
        raise SyntaxError("缺少'}'" + error(index))
    return


def p_kvpair(env: Env):
    global index
    c = index
    if p_next(':'):
        if key := (p_attr('Identity') or p_string()):
            index += 1
            if value := p_exp(env):
                return [key, value]
        raise SyntaxError("键值对错误" + error(index))
    if (id1 := p_attr('Identity')) and p_match('('):
        argus = p_argus()
        if p_match(')') and (bk := Block(env)):
            return ['function', id1, argus, bk]
    index = c
    return


def p_primary(env: Env):
    return p_atom(env)
    # p_subscription(env)
    # slicing(env)


def p_power(env: Env):
    l = p_primary(env)
    if p_match('**'):
        return ['power', l, p_factor(env)]
    return l


def p_factor(env: Env):
    if op := (p_match('+') or p_match('-') or p_match('~')):
        return ['factor', op, p_power(env)]
    return p_power(env)


def p_term(env: Env):
    l = p_factor(env)
    if op := p_attr('TermOp'):
        return [op['value'], l, p_term(env)]
    return l


def p_sum(env: Env):
    l = p_term(env)
    if op1 := (p_match('+') or p_match('-')):
        return [op1, l, p_sum(env)]
    return l


def p_shiftOp(env: Env):
    l = p_sum(env)
    if op := p_attr('ShiftOp'):
        return [op['value'], l, p_sum(env)]
    return l


def p_bitOp(env: Env):
    l = p_shiftOp(env)
    if op := p_attr('BitOp'):
        return [op['value'], l, p_shiftOp(env)]
    return l


def p_compareOp(env: Env):
    l = p_bitOp(env)
    if op := p_attr('CompareOp'):
        return [op['value'], l, p_bitOp(env)]
    return l


def p_inversion(env: Env):
    if p_match('!'):
        return ['!', p_compareOp(env)]
    return p_compareOp(env)


def p_binaryOp(env: Env):
    l = p_inversion(env)
    if op := p_attr('BinaryOp'):
        return [op['value'], l, p_binaryOp(env)]
    return l


def p_attrRef(env: Env):
    global index
    c = index
    if (atom := p_atom(env)):
        if p_match('.'):
            return ['ref:dot', atom, p_exp(env)]
        if p_match('[') and (str1 := p_string()) and p_match(']'):
            return ['ref:sub', atom, str1]
    index = c
    return


def p_lambda(env: Env):
    global index
    c = index
    if p_match('function') and p_match('('):
        argus = p_argus()
        if p_match(')') and (bk := Block(env)):
            return ['lambda', argus, bk]
        raise SyntaxError("不符合'lambda'函数的语法" + error(index))
    if p_match('('):
        argus = p_argus()
        if p_match(')') and p_match('=>'):
            if bk := Block(env):
                return ['lambda', argus, bk]
            raise SyntaxError("'=>'后缺少语句块" + error(index))
    index = c
    if p_next('=>'):
        if id1 := p_attr('Identity'):
            index += 1
            if bk := Block(env):
                return ['lambda', id1, bk]
            raise SyntaxError("'=>'后缺少语句块" + error(index))
        raise SyntaxError("'=>'前不是标识符" + error(index))
    return


def p_exp(env: Env):
    return p_lambda(env) or p_attrRef(env) or p_binaryOp(env)


def p_assign(env: Env):
    global index, func
    c = index
    if p_match('let'):
        if (id1 := p_attr('Identity')) and p_match('='):
            func = f"{id1['value']}@{env.label}"
            if stmt := p_stmt(env):
                return ['assign', id1, stmt]
        raise SyntaxError("你要'let'什么" + error(index))
    if (id1 := p_attr('Identity')) and p_match('='):
        if stmt := p_stmt(env):
            return ['assign', id1, stmt]
        raise SyntaxError("没有值可以赋" + error(index))
    index = c
    if (id1 := p_attr('Identity')) and (op := p_attr('Augassin')):
        if exp := p_exp(env):
            return ['augassin', op['value'][:-1], id1, exp]
        raise SyntaxError("没有值可以赋" + error(index))
    index = c
    return


def p_return(env: Env):
    if p_match('return'):
        return ['return', func, p_exp(env)]
    return


def p_import():
    global index
    c = index
    if p_match('import'):
        if p_match('{'):
            argus = p_argus()
            if p_match('}') and p_match('from') and (where := p_string()):
                return ['import', argus, where]
            raise SyntaxError("不符合'import'语法" + error(index))
        if (id1 := p_attr('Identity')) and p_match('from') and (where := p_string()):
            return ['import', id1, where]
        index = c
        if p_match('*') and p_match('as') and (id1 := p_attr('Identity')) and \
                p_match('from') and (where := p_string()):
            return ['import', '*', id1, where]
    return


def p_symStmt(env: Env):
    return p_assign(env) or \
        p_return(env) or \
        p_import()


def p_func(env: Env):
    global func
    if p_match('function'):
        if (id1 := p_attr('Identity')) and p_match('('):
            argus = p_argus()
            func = f"{id1['value']}@{env.label}"
            if p_match(')') and (bk := Block(env)):
                return ['function', id1, argus, bk]
        raise SyntaxError("不符合'function'语法" + error(index))
    return


def p_else(env: Env):
    if p_match('else'):
        if bk := Block(env):
            return ['else', bk]
        raise SyntaxError("'else'后未接语句块" + error(index))
    return


def p_elif(env: Env):
    global index
    c = index
    if p_match('else') and p_match('if') and p_match('('):
        if (cp := p_binaryOp(env)) and p_match(')'):
            if bk := Block(env):
                ret = ['elif', cp, bk]
                ef, hasElse = p_elif(env)
                if ef:
                    ret.append(ef)
                if not hasElse and (el := p_else(env)):
                    ret.append(el)
                return ret, True
            raise SyntaxError("'else if'后未接语句块" + error(index))
        raise SyntaxError("条件语句错误" + error(index))
    index = c
    return None, None


def p_if(env: Env):
    if p_match('if') and p_match('('):
        if (cp := p_binaryOp(env)) and p_match(')'):
            if bk := Block(env):
                ret = ['if', cp, bk]
                ef, hasElse = p_elif(env)
                if ef:
                    ret.append(ef)
                if not hasElse and (el := p_else(env)):
                    ret.append(el)
                return ret
            raise SyntaxError("'if'后未接语句块" + error(index))
        raise SyntaxError("条件语句错误" + error(index))
    return


def p_for(env: Env):
    if p_match('for') and p_match('('):
        ret = ['for', [], [], []]
        if ag1 := p_assign(env):
            ret[1].append(ag1)
            while p_match(',') and (ag2 := p_assign(env)):
                ret[1].append(ag2)
        if p_match(';'):
            if cp1 := p_binaryOp(env):
                ret[2].append(cp1)
                while p_match(',') and (cp2 := p_binaryOp(env)):
                    ret[2].append(cp2)
        else:
            raise SyntaxError("缺少第一个';'" + error(index))
        if p_match(';'):
            if stmt1 := p_stmt(env):
                ret[3].append(stmt1)
                while p_match(',') and (stmt2 := p_stmt(env)):
                    ret[3].append(stmt2)
        else:
            raise SyntaxError("缺少第二个';'" + error(index))
        if p_match(')') and (bk := Block(env)):
            ret.append(bk)
            return ret
        raise SyntaxError("'for'后未接语句块" + error(index))
    return


def p_while(env: Env):
    if p_match('while') and p_match('('):
        if (cp := p_binaryOp(env)) and p_match(')'):
            if bk := Block(env):
                return ['while', cp, bk]
            raise SyntaxError("'while'后未接语句块" + error(index))
        raise SyntaxError("缺少条件判断语句" + error(index))
    return


def p_comStmt(env: Env):
    return p_func(env) or \
        p_if(env) or \
        p_for(env) or \
        p_while(env)


def p_stmt(env: Env):
    return p_symStmt(env) or \
        p_comStmt(env) or \
        p_exp(env)


class Block:
    def __new__(cls, env) -> list:
        if p_match('{'):
            stmts = []
            neo = Env(env)
            stmts.append(neo)
            while stmt := p_stmt(neo):
                if isinstance(stmt, dict):
                    raise SyntaxError("该语句似乎没有任何作用?" + error(index))
                stmts.append(stmt)
                p_match(';')
            if p_match('}'):
                return stmts
            raise SyntaxError("缺少'}'" + error(index))
        if stmt := p_stmt(env):
            return [stmt]
        raise SyntaxError("未匹配任何有效语法" + error(index))


def syntacticParser(path: str):
    global tokens
    with open(path, encoding='utf-8') as Js:
        tokens = lexicalAnalyzer(Js.read())
    while index < len(tokens):
        AST.extend(Block(TOP))
        p_match(';')
    return AST
