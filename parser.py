from ast_nodes import *

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
            if self.match("LPAREN"):
                args = []
                if not self.peek("RPAREN"):
                    args.append(self.expression())
                    while self.match("COMMA"): args.append(self.expression())
                self.expect("RPAREN")
                return FuncCall(name, args)
            var = Var(name)
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