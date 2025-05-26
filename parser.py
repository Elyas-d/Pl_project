from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens, self.pos = tokens, 0

    def peek(self, t=None):
        if self.pos >= len(self.tokens):
            return None
        token = self.tokens[self.pos]
        if t is None or token[0] == t:
            return token
        return None

    def match(self, t):
        token = self.peek(t)
        if token:
            self.pos += 1
        return token

    def expect(self, t):
        token = self.match(t)
        if not token:
            raise SyntaxError(f"Expected {t}")
        return token[1]

    def parse(self):
        stmts = []
        while self.peek():
            stmts.append(self.statement())
        return Block(stmts)

    def statement(self):
        if self.match("LET"):
            # Variable declaration statement
            name = self.expect("IDENT")
            self.expect("ASSIGN")
            expr = self.assignment()  # use our assignment expression grammar
            self.expect("SEMICOLON")
            return Assign(name, expr)
        elif self.match("PRINT"):
            expr = self.assignment()
            self.expect("SEMICOLON")
            return Print(expr)
        elif self.match("IF"):
            self.expect("LPAREN")
            cond = self.assignment()
            self.expect("RPAREN")
            then = self.block()
            else_ = self.block() if self.match("ELSE") else None
            return If(cond, then, else_)
        elif self.match("WHILE"):
            self.expect("LPAREN")
            cond = self.assignment()
            self.expect("RPAREN")
            return While(cond, self.block())
        elif self.match("FOR"):
            self.expect("LPAREN")
            if self.peek("LET"):
                self.match("LET")
                name = self.expect("IDENT")
                self.expect("ASSIGN")
                expr = self.assignment()
                init = Assign(name, expr)
                self.expect("SEMICOLON")
            else:
                init = self.assignment()
                self.expect("SEMICOLON")
            cond = self.assignment()
            self.expect("SEMICOLON")
            step = self.assignment()
            self.expect("RPAREN")
            body = self.block()
            return For(init, cond, step, body)
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
            val = self.assignment()
            self.expect("SEMICOLON")
            return Return(val)
        else:
            expr = self.assignment()
            self.expect("SEMICOLON")
            return expr

    def block(self):
        self.expect("LBRACE")
        stmts = []
        while not self.match("RBRACE"):
            stmts.append(self.statement())
        return Block(stmts)

    # ----- Expression parsing -----
    # We add an assignment grammar so that e.g. "አ = አ + 1" can appear as an expression.
    def assignment(self):
        expr = self.equality()
        # Handle simple assignment
        if self.peek("ASSIGN"):
            self.match("ASSIGN")
            value = self.assignment()
            if isinstance(expr, Var):
                return Assign(expr.name, value)
            elif isinstance(expr, Index):
                return AssignIndex(expr.list_expr, expr.index_expr, value)
            else:
                raise SyntaxError("Invalid assignment target")
        # Handle compound assignments, e.g., a += 1 or a -= 2
        elif self.peek("PLUS_ASSIGN") or self.peek("MINUS_ASSIGN"):
            if self.peek("PLUS_ASSIGN"):
                self.match("PLUS_ASSIGN")
                op = "+"
            else:
                self.match("MINUS_ASSIGN")
                op = "-"
            value = self.assignment()
            # Desugar: a += 1 becomes a = a + 1
            if isinstance(expr, Var):
                return Assign(expr.name, BinOp(expr, op, value))
            elif isinstance(expr, Index):
                return AssignIndex(expr.list_expr, expr.index_expr, BinOp(expr, op, value))
            else:
                raise SyntaxError("Invalid assignment target")
        return expr

    def equality(self):
        expr = self.term()
        while self.peek() and self.peek()[0] in {"EQ", "NE", "GT", "LT", "GE", "LE", "OP"}:
            # If an operator is found, but note: We want to reserve '=' for assignment.
            # Here we assume 'OP' does not include '='.
            op = self.match(self.peek()[0])[1]
            right = self.term()
            expr = BinOp(expr, op, right)
        return expr

    def term(self):
        token = self.peek()
        if token[0] == "NUMBER":
            return Number(self.match("NUMBER")[1])
        if token[0] == "STRING":
            return String(self.match("STRING")[1])
        if token[0] == "BOOLEAN":
            # Consume the token and create a Boolean node
            value = True if self.match("BOOLEAN")[1] == "እውነት" else False
            return Boolean(value)
        if token[0] == "INPUT":
            self.match("INPUT")
            self.expect("LPAREN")
            prompt = self.assignment()
            self.expect("RPAREN")
            return Input(prompt)
        if token[0] == "IDENT":
            name = self.match("IDENT")[1]
            if self.match("LPAREN"):
                args = []
                if not self.peek("RPAREN"):
                    args.append(self.assignment())
                    while self.match("COMMA"):
                        args.append(self.assignment())
                self.expect("RPAREN")
                return FuncCall(name, args)
            var = Var(name)
            while self.match("LBRACKET"):
                idx_expr = self.assignment()
                self.expect("RBRACKET")
                var = Index(var, idx_expr)
            return var
        if token[0] == "LBRACKET":
            self.match("LBRACKET")
            elements = []
            if not self.peek("RBRACKET"):
                elements.append(self.assignment())
                while self.match("COMMA"):
                    elements.append(self.assignment())
            self.expect("RBRACKET")
            return ListLiteral(elements)
        if token[0] == "LPAREN":
            self.match("LPAREN")
            expr = self.assignment()
            self.expect("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected token: {token}")