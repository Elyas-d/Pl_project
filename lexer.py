import re

TOKEN_REGEX = [
    ("MLCOMMENT", r"/\*[\s\S]*?\*/"),
    ("COMMENT", r"(//[^\n]*|#[^\n]*)"),
    ("PLUS_ASSIGN", r"\+\="),
    ("MINUS_ASSIGN", r"\-\="),
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
    pos = 0
    while pos < len(code):
        match = None
        for token_type, pattern in TOKEN_REGEX:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                # Skip whitespace, single-line comments, and multi-line comments.
                if token_type not in {"WHITESPACE", "COMMENT", "MLCOMMENT"}:
                    tokens.append((token_type, match.group(0)))
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f"Illegal character: {code[pos]}")
    return tokens