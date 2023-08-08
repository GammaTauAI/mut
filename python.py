import ast
from engine import Mutator, Engine
import astunparse


class PythonMutator(ast.NodeTransformer, Mutator):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)

    def convert_to_div(self, node):
        return ast.Div()

    def convert_to_mult(self, node):
        return ast.Mult()

    def convert_to_add(self, node):
        return ast.Add()

    def convert_to_sub(self, node):
        return ast.Sub()

    def visit_Sub(self, node):
        return self.mutate_aor(node, "-")

    def visit_Add(self, node):
        return self.mutate_aor(node, "+")

    def visit_Mult(self, node):
        return self.mutate_aor(node, "*")

    def visit_Div(self, node):
        return self.mutate_aor(node, "/")


if __name__ == "__main__":
    import os
    CODE = """
def func(a, b):
    bleh = 1337
    if a > b:
        return a - b
    elif a < b:
        return b - a
    else: # a == b
        return 0
"""

    tree = ast.parse(CODE)
    engine = Engine(0.9, int(os.urandom(4).hex(), 16))
    mutator = PythonMutator(engine)
    tree = mutator.visit(tree)
    print(astunparse.unparse(tree))
