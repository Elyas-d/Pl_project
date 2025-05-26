import re

TOKEN_REGEX = [
    ("NUMBER", r"\d+"),
    ("STRING", r'"[^"]*"'),
    ("LET", r"ይዘው"),
    ("FUNC", r"ፋንክሽን"),
    ("RETURN", r"መመለስ"),
    ("IF", r"ከሆነ"),
    ("ELSE", r"ካልሆነ"),
    ("WHILE", r"በማዘጋጀት"),
    ("FOR", r"ለ"),
    ("PRINT", r"አትም"),
    ("INPUT", r"ጠይቅ"),
    ("BOOLEAN", r"እውነት|ሐሰት"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("EQ", r"=="), ("NE", r"!="), ("GE", r">="), ("LE", r"<="),
    ("GT", r">"), ("LT", r"<"),
    ("ASSIGN", r"="),
    ("OP", r"[+\-*/%]"),
    ("LPAREN", r"\("), ("RPAREN", r"\)"),
    ("LBRACE", r"\{"), ("RBRACE", r"\}"),
    ("COMMA", r","), ("SEMICOLON", r";"),
    ("IDENT", r"[a-zA-Z_\u1200-\u135A][a-zA-Z0-9_\u1200-\u135A]*"),
    ("WHITESPACE", r"\s+"),
]

def tokenize(code):
    tokens = []
    while code:
        for token_type, regex in TOKEN_REGEX:
            match = re.match(regex, code)
            if match:
                if token_type != "WHITESPACE":
                    tokens.append((token_type, match.group(0)))
                code = code[match.end():]
                break
        else:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens