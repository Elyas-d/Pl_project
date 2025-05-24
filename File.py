import re

# ===== LEXER =====
TOKEN_REGEX = [
    ("NUMBER", r"\d+"),
    ("STRING", r'"[^"]*"'),
    ("LET", r"ይዘው"),
    ("FUNC", r"ፋንክሽን"),
    ("RETURN", r"መመለስ"),
    ("IF", r"ከሆነ"),
    ("ELSE", r"ካልሆነ"),
    ("WHILE", r"በማዘጋጀት"),
    ("PRINT", r"አትም"),
    ("INPUT", r"ጠይቅ"),
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

# ===== AST CLASSES =====
class Number:
    def __init__(self, value): self.value = int(value)
class String:
    def __init__(self, value): self.value = value.strip('"')
class Var:
    def __init__(self, name): self.name = name
class BinOp:
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
class Assign:
    def __init__(self, name, expr): self.name, self.expr = name, expr
class Print:
    def __init__(self, expr): self.expr = expr
class Input:
    def __init__(self, prompt): self.prompt = prompt
class If:
    def __init__(self, cond, then, else_): self.cond, self.then, self.else_ = cond, then, else_
class While:
    def __init__(self, cond, body): self.cond, self.body = cond, body
class Block:
    def __init__(self, stmts): self.stmts = stmts
class FuncDef:
    def __init__(self, name, params, body): self.name, self.params, self.body = name, params, body
class FuncCall:
    def __init__(self, name, args): self.name, self.args = name, args
class Return:
    def __init__(self, value): self.value = value
class ListLiteral:
    def __init__(self, elements): self.elements = elements
class Index:
    def __init__(self, list_expr, index_expr): self.list_expr, self.index_expr = list_expr, index_expr

# ===== PARSER =====
class Parser:
    def __init__(self, tokens): self.tokens, self.pos = tokens, 0

    def peek(self, t=None):
        if self.pos >= len(self.tokens): return None
        token = self.tokens[self.pos]
        return token if t is None or token[0] == t else None

    def match(self, t):
        token = self.peek(t)
        if token: self.pos += 1
        return token

    def expect(self, t):
        token = self.match(t)
        if not token: raise SyntaxError(f"Expected {t}")
        return token[1]

    def parse(self):
        stmts = []
        while self.peek():
            stmts.append(self.statement())
        return Block(stmts)

    def statement(self):
        if self.match("LET"):
            name = self.expect("IDENT")
            self.expect("ASSIGN")
            expr = self.expression()
            self.expect("SEMICOLON")
            return Assign(name, expr)
        elif self.match("PRINT"):
            expr = self.expression()
            self.expect("SEMICOLON")
            return Print(expr)
        elif self.match("IF"):
            self.expect("LPAREN")
            cond = self.expression()
            self.expect("RPAREN")
            then = self.block()
            else_ = self.block() if self.match("ELSE") else None
            return If(cond, then, else_)
        elif self.match("WHILE"):
            self.expect("LPAREN")
            cond = self.expression()
            self.expect("RPAREN")
            return While(cond, self.block())
        elif self.match("FUNC"):
            name = self.expect("IDENT")
            self.expect("LPAREN")
            params = []
            if self.peek("IDENT"):
                params.append(self.expect("IDENT"))
                while self.match("COMMA"):
                    params.append(self.expect("IDENT"))
            self.expect("RPAREN")
            return FuncDef(name, params, self.block())
        elif self.match("RETURN"):
            val = self.expression()
            self.expect("SEMICOLON")
            return Return(val)
        else:
            expr = self.expression()
            self.expect("SEMICOLON")
            return expr

    def block(self):
        self.expect("LBRACE")
        stmts = []
        while not self.match("RBRACE"):
            stmts.append(self.statement())
        return Block(stmts)

    def expression(self):
        if self.match("INPUT"):
            self.expect("LPAREN")
            prompt = self.expression()
            self.expect("RPAREN")
            return Input(prompt)

        left = self.term()
        while self.peek() and self.peek()[0] in {"OP", "EQ", "NE", "GT", "LT", "GE", "LE"}:
            op = self.match(self.peek()[0])[1]
            right = self.term()
            left = BinOp(left, op, right)
        return left

    def term(self):
        token = self.peek()
        if token[0] == "NUMBER": return Number(self.match("NUMBER")[1])
        if token[0] == "STRING": return String(self.match("STRING")[1])
        if token[0] == "IDENT":
            name = self.match("IDENT")[1]
            # Function call or variable or index
            if self.match("LPAREN"):
                args = []
                if not self.peek("RPAREN"):
                    args.append(self.expression())
                    while self.match("COMMA"): args.append(self.expression())
                self.expect("RPAREN")
                return FuncCall(name, args)
            var = Var(name)
            # Indexing: var[expr]
            while self.match("LBRACKET"):
                index_expr = self.expression()
                self.expect("RBRACKET")
                var = Index(var, index_expr)
            return var
        if token[0] == "LBRACKET":
            self.match("LBRACKET")
            elements = []
            if not self.peek("RBRACKET"):
                elements.append(self.expression())
                while self.match("COMMA"):
                    elements.append(self.expression())
            self.expect("RBRACKET")
            return ListLiteral(elements)
        if token[0] == "LPAREN":
            self.match("LPAREN")
            expr = self.expression()
            self.expect("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected token: {token}")

# ===== INTERPRETER =====
class Interpreter:
    def __init__(self):
        self.globals = {}
        self.functions = {}

    def eval(self, node, env=None):
        if env is None: env = self.globals
        if isinstance(node, Number): return node.value
        if isinstance(node, String): return node.value
        if isinstance(node, ListLiteral): return [self.eval(e, env) for e in node.elements]
        if isinstance(node, Index):
            lst = self.eval(node.list_expr, env)
            idx = self.eval(node.index_expr, env)
            return lst[idx]
        if isinstance(node, Var): 
            if node.name in env:
                return env[node.name]
            else:
                raise NameError(f"Undefined variable '{node.name}'")
        if isinstance(node, Input):
            prompt = self.eval(node.prompt, env)
            return input(prompt)
        if isinstance(node, BinOp):
            l, r = self.eval(node.left, env), self.eval(node.right, env)
            if node.op == '+':
                if isinstance(l, str) or isinstance(r, str):
                    return str(l) + str(r)
                return l + r
            return {
                '-': l - r, '*': l * r, '/': l // r, '%': l % r,
                '==': l == r, '!=': l != r, '>': l > r, '<': l < r,
                '>=': l >= r, '<=': l <= r,
            }[node.op]
        if isinstance(node, Assign): 
            env[node.name] = self.eval(node.expr, env)
        if isinstance(node, Print): 
            print(self.eval(node.expr, env))
        if isinstance(node, If):
            if self.eval(node.cond, env): return self.eval(node.then, env)
            elif node.else_: return self.eval(node.else_, env)
        if isinstance(node, While):
            while self.eval(node.cond, env): self.eval(node.body, env)
        if isinstance(node, Block):
            local_env = dict(env)
            for stmt in node.stmts:
                result = self.eval(stmt, local_env)
                if isinstance(result, tuple) and result[0] == 'return': return result
        if isinstance(node, FuncDef): self.functions[node.name] = node
        if isinstance(node, FuncCall):
            func = self.functions.get(node.name)
            if not func: raise NameError(f"Undefined function {node.name}")
            local_env = {param: self.eval(arg, env) for param, arg in zip(func.params, node.args)}
            result = self.eval(func.body, local_env)
            if isinstance(result, tuple) and result[0] == 'return': return result[1]
        if isinstance(node, Return): return ('return', self.eval(node.value, env))

# ===== RUNNER =====
def run(code):
    tokens = tokenize(code)
    tree = Parser(tokens).parse()
    Interpreter().eval(tree)

# ===== SAMPLE AMHARIC PROGRAM =====
program = """
ይዘው ዝ = [1, 2, 3, 4];
አትም(ዝ[0]);
አትም(ዝ[2] + ዝ[3]);
"""

run(program)