from ast_nodes import *

class Interpreter:
    def __init__(self):
        self.globals = {}
        self.functions = {}

    def eval(self, node, env=None):
        if env is None:
            env = self.globals
        if isinstance(node, Number):
            return node.value
        if isinstance(node, String):
            return node.value
        if isinstance(node, ListLiteral):
            return [self.eval(e, env) for e in node.elements]
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
            l = self.eval(node.left, env)
            r = self.eval(node.right, env)
            if node.op == '+':
                if isinstance(l, str) or isinstance(r, str):
                    return str(l) + str(r)
                return l + r
            if node.op == '-':
                return l - r
            if node.op == '*':
                return l * r
            if node.op == '/':
                return l // r
            if node.op == '%':
                return l % r
            if node.op == '==':
                return l == r
            if node.op == '!=':
                return l != r
            if node.op == '>':
                return l > r
            if node.op == '<':
                return l < r
            if node.op == '>=':
                return l >= r
            if node.op == '<=':
                return l <= r
        if isinstance(node, Assign):
            env[node.name] = self.eval(node.expr, env)
            return env[node.name]
        if isinstance(node, AssignIndex):
            lst = self.eval(node.list_expr, env)
            idx = self.eval(node.index_expr, env)
            val = self.eval(node.value_expr, env)
            lst[idx] = val
            return val
        if isinstance(node, Print):
            output = self.eval(node.expr, env)
            print(output)
            return
        if isinstance(node, If):
            if self.eval(node.cond, env):
                return self.eval(node.then, env)
            elif node.else_:
                return self.eval(node.else_, env)
        if isinstance(node, While):
            while self.eval(node.cond, env):
                self.eval(node.body, env)
            return
        if isinstance(node, For):
            self.eval(node.init, env)
            while self.eval(node.cond, env):
                self.eval(node.body, env)
                self.eval(node.step, env)
            return
        if isinstance(node, Block):
            for stmt in node.stmts:
                result = self.eval(stmt, env)
                # Return handling can be added here if needed.
            return
        if isinstance(node, FuncDef):
            self.functions[node.name] = node
            return
        if isinstance(node, FuncCall):
            func = self.functions.get(node.name)
            if not func:
                raise NameError(f"Undefined function {node.name}")
            local_env = dict(env)
            for param, arg in zip(func.params, node.args):
                local_env[param] = self.eval(arg, env)
            result = self.eval(func.body, local_env)
            if isinstance(result, tuple) and result[0] == 'return':
                return result[1]
            return
        if isinstance(node, Return):
            return ('return', self.eval(node.value, env))
        raise SyntaxError("Unknown node type")