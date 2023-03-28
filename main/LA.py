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
    lineTokens: list[dict[str, str]] = [{'attr': '', 'value': ''}]
    words = ['']
    for i in range(len(input)):
        lchar = input[i-1:i]
        char = input[i:i+1]
        if char == ' ':
            if lchar == ' ':
                words[-1] += ' '
            else:
                words.extend([' ', ''])
        elif char.isnumeric() and lchar in '+-':
            words[-2] += char
        elif char in '+-*/%<>!=()[]{},.?&|^~:;`"\'\n':
            if char == '=' and lchar in '+-*/%<>!=&|^':
                words[-2] += '='
            elif char == '.':
                if lchar.isnumeric():
                    words[-1] += '.'
                elif lchar in '?.':
                    words[-2] += '.'
                else:
                    words.extend(['.', ''])
            elif char == '/':
                if lchar == '/':
                    words = ['']
                    break
                elif lchar == '*':
                    words[-2] += '/'
                else:
                    words.extend([char, ''])
            elif char == '*' and lchar in '/*':
                words[-2] += '*'
            elif char in '?<>&|' and lchar == char:
                words[-2] += char
            elif char in '+-' and lchar == char:
                words[-2] += char
            elif char == '>' and lchar == '=':
                words[-2] += char
            else:
                words.extend([char, ''])
        else:
            words[-1] += char
    for index in range(len(words)):
        word = words[index]
        lineTokens = l_stringCheck(word, lineTokens[-1]['attr'], lineTokens)
        if lineTokens[-1]['attr'].endswith('Str'):
            continue
        elif word in '`"\'' or word.isspace():
            pass
        elif re.match('^(\-|\+)?[0-9][0-9]*(.[0-9]*)?$', word):
            lineTokens.append({'attr': 'Number', 'value': word})
        else:
            word = word.strip()
            if word in WORDS.keys():
                if WORDS[word] == 'Error':
                    raise InterruptedError(
                        f"不支持该关键字: '{word}', 错误位于{words[index-1:index+2]}")
                lineTokens.append({'attr': WORDS[word], 'value': word})
            else:
                lineTokens.append({'attr': 'Identity', 'value': word})
    return lineTokens[1:]
