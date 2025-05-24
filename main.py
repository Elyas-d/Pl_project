from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

def run(code):
    tokens = tokenize(code)
    tree = Parser(tokens).parse()
    Interpreter().eval(tree)

program = """
ይዘው ዝ = [1, 2, 3, 4];
አትም(ዝ[0]);
አትም(ዝ[2] + ዝ[3]);
"""

run(program)