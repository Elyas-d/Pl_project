from ast_nodes import *

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