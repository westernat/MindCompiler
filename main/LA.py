import re


WORDS = {
    "import": "Keyword",
    "as": "Keyword",
    "from": "Keyword",
    "let": "Keyword",
    "const": "Error",
    "var": "Error",
    "if": "Keyword",
    "else": "Keyword",
    "new": "Keyword",
    "try": "Error",
    "catch": "Error",
    "finally": "Error",
    "return": "Keyword",
    "void": "Error",
    "null": "Keyword",
    "undefined": "Error",
    "for": "Keyword",
    "continue": "Keyword",
    "switch": "Keyword",
    "case": "Keyword",
    "default": "Keyword",
    "break": "Keyword",
    "do": "Keyword",
    "while": "Keyword",
    "function": "Keyword",
    "this": "Keyword",
    "with": "Error",
    "throw": "Error",
    "delete": "Keyword",
    "in": "Keyword",
    "of": "Keyword",
    "instranceof": "Error",
    "typeof": "Error",
    "+": "add",
    "++": "Error",
    "-": "sub",
    "--": "Error",
    "*": "TermOp",
    "**": "pow",
    "/": "TermOp",
    "%": "TermOp",
    "!": "not",
    "!=": "CompareOp",
    "==": "CompareOp",
    "&": "BitOp",
    "&&": "BinaryOp",
    "|": "BitOp",
    "||": "BinaryOp",
    "<": "CompareOp",
    ">": "CompareOp",
    "<<": "ShiftOp",
    ">>": "ShiftOp",
    "~": "flip",
    "^": "BitOp",
    "??": "Merge",
    "?.": "OptChain",
    ".": "AttrRef",
    "...": "Spread",
    "+=": "Augassin",
    "-=": "Augassin",
    "*=": "Augassin",
    "/=": "Augassin",
    "%=": "Augassin",
    "**=": "Augassin",
    "!==": "Error",
    "===": "Error",
    "&=": "Augassin",
    "&&=": "Error",
    "|=": "Augassin",
    "||=": "Error",
    "<=": "CompareOp",
    ">=": "CompareOp",
    "<<=": "Augassin",
    ">>=": "Augassin",
    "~=": "Augassin",
    "^=": "Augassin",
    "=": "Symbol",
    "(": "Symbol",
    ")": "Symbol",
    "{": "Symbol",
    "}": "Symbol",
    "[": "Symbol",
    "]": "Symbol",
    ",": "Symbol",
    ":": "Symbol",
    ";": "Symbol",
    "=>": "Symbol",
    "true": "Boolean",
    "false": "Boolean",
    "/*": "Comment",
    "*/": "Comment"
}


def l_stringCheck(word: str, lattr: str, lineTokens: list[dict[str, str]]):
    if word in '`"\'':
        for char, attr in zip('`"\'', ('FormatStr', 'DoubleStr', 'SingleStr')):
            if word == char:
                if lattr == attr:
                    # 如果是闭合符
                    lineTokens[-1]['attr'] = attr + 'End'
                    lineTokens[-1]['value'] += word
                else:
                    # 否则是开始符
                    lineTokens.append({'attr': attr, 'value': word})
                break
    elif lattr.find('Str') != -1 and not lattr.endswith('End'):
        lineTokens[-1]['value'] += word
    elif word.isspace():
        pass
    return lineTokens


def lexicalAnalyzer(input: str):
    '''
    词法分析模块
    input -> tokens
    '''
    row = 1
    column = 1
    wordBase = lambda l='': {'literal': l, 'row': row, 'column': column}
    words = [wordBase()]
    for i in range(len(input)):
        lchar = input[i-1:i]
        char = input[i:i+1]
        if char == ' ':
            if lchar == ' ':
                words[-1]['literal'] += ' '
            else:
                words.extend([wordBase(' '), wordBase()])
        elif char.isnumeric() and lchar in '+-':
            words[-2]['literal'] += char
        elif char in '+-*/%<>!=()[]{},.?&|^~:;`"\'\n':
            if char == '=' and lchar in '+-*/%<>!=&|^':
                words[-2]['literal'] += '='
            elif char == '.':
                if lchar.isnumeric():
                    words[-1]['literal'] += '.'
                elif lchar in '?.':
                    words[-2]['literal'] += '.'
                else:
                    words.extend([wordBase('.'), wordBase()])
            elif char == '/':
                if lchar == '/':
                    words = [wordBase()]
                    break
                elif lchar == '*':
                    words[-2]['literal'] += '/'
                else:
                    words.extend([wordBase(char), wordBase()])
            elif char == '*' and lchar in '/*':
                words[-2]['literal'] += '*'
            elif char in '?<>&|' and lchar == char:
                words[-2]['literal'] += char
            elif char in '+-' and lchar == char:
                words[-2]['literal'] += char
            elif char == '>' and lchar == '=':
                words[-2]['literal'] += char
            elif char == '\n':
                row += 1
                column = 0
            else:
                words.extend([wordBase(char), wordBase()])
        else:
            words[-1] = wordBase(words[-1]['literal'] + char)
        column += 1

    def tokenBase(a, w): return {
        'attr': a, 'value': w['literal'], 'row': w['row'], 'column': w['column']}
    lineTokens = [tokenBase('', wordBase())]
    WORDKEYS = WORDS.keys()
    for index in range(len(words)):
        word = words[index]
        literal: str = word['literal']
        lineTokens = l_stringCheck(literal, lineTokens[-1]['attr'], lineTokens)
        if lineTokens[-1]['attr'].endswith('Str'):
            continue
        elif literal in '`"\'' or literal.isspace():
            pass
        elif re.match('^(\-|\+)?[0-9][0-9]*(.[0-9]*)?$', literal):
            lineTokens.append(tokenBase('Number', word))
        else:
            literal = literal.strip()
            word['literal'] = literal
            if literal in WORDKEYS:
                if WORDS[literal] == 'Error':
                    raise InterruptedError(
                        f"不支持该关键字: '{literal}', 错误位于 row: {word['row']}, column: {word['column']}")
                lineTokens.append(tokenBase(WORDS[literal], word))
            else:
                lineTokens.append(tokenBase('Identity', word))
    return lineTokens[1:]
