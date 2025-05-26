class Number:
    def __init__(self, value): self.value = int(value)
class For:
    def __init__(self, init, cond, step, body):
        self.init, self.cond, self.step, self.body = init, cond, step, body
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
class AssignIndex:
    def __init__(self, list_expr, index_expr, value_expr):
        self.list_expr = list_expr
        self.index_expr = index_expr
        self.value_expr = value_expr