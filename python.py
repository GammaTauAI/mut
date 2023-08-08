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

    def convert_to_and(self, node):
        return ast.And()

    def convert_to_or(self, node):
        return ast.Or()

    def convert_to_binop_a(self, node: ast.BinOp):
        return node.left

    def convert_to_binop_b(self, node: ast.BinOp):
        return node.right

    def convert_to_boolop_a(self, node: ast.BoolOp):
        return node.values[0]

    def convert_to_boolop_b(self, node: ast.BoolOp):
        return node.values[1]

    def convert_to_true(self, node):
        return ast.NameConstant(value=True)

    def convert_to_false(self, node):
        return ast.NameConstant(value=False)

    def convert_to_not(self, node):
        return ast.UnaryOp(op=ast.Not(), operand=node)

    def convert_to_gt(self, node):
        return ast.Gt()

    def convert_to_lt(self, node):
        return ast.Lt()

    def convert_to_gte(self, node):
        return ast.GtE()

    def convert_to_lte(self, node):
        return ast.LtE()

    def convert_to_eq(self, node):
        return ast.Eq()

    def convert_to_neq(self, node):
        return ast.NotEq()

    def convert_to_increment(self, node: ast.Constant):
        return ast.Constant(value=node.value + 1)

    def convert_to_decrement(self, node: ast.Constant):
        return ast.Constant(value=node.value - 1)

    def visit_BinOp(self, node: ast.BinOp):
        mutated = self.mutate_binop_expr(node)
        if mutated == node:
            return self.generic_visit(node)
        else:
            return mutated

    def visit_BoolOp(self, node: ast.BoolOp):
        mutated = self.mutate_boolop_expr(node)
        if mutated == node:
            return self.generic_visit(node)
        else:
            return mutated

    def visit_Constant(self, node: ast.Constant):
        if type(node.value) == int:
            return self.mutate_number_literal(node)
        else:  # TODO: mutate bool? i think we shouldn't
            return self.generic_visit(node)

    def visit_Sub(self, node):
        return self.mutate_aor_op(node, "-")

    def visit_Add(self, node):
        return self.mutate_aor_op(node, "+")

    def visit_Mult(self, node):
        return self.mutate_aor_op(node, "*")

    def visit_Div(self, node):
        return self.mutate_aor_op(node, "/")

    def visit_And(self, node):
        return self.mutate_lcr(node, "and")

    def visit_Or(self, node):
        return self.mutate_lcr(node, "or")

    def visit_Gt(self, node):
        return self.mutate_ror(node, ">")

    def visit_Lt(self, node):
        return self.mutate_ror(node, "<")

    def visit_GtE(self, node):
        return self.mutate_ror(node, ">=")

    def visit_LtE(self, node):
        return self.mutate_ror(node, "<=")

    def visit_Eq(self, node):
        return self.mutate_ror(node, "==")

    def visit_NotEq(self, node):
        return self.mutate_ror(node, "!=")


if __name__ == "__main__":
    import os
    CODE = """
def func(a, b):
    bleh = 1337
    if a > b > b and True and True or False:
        return a - b
    elif a < b:
        return b - a
    else: # a == b
        return 0
"""

    tree = ast.parse(CODE)
    print(ast.dump(tree))
    engine = Engine(
        seed=int(os.urandom(4).hex(), 16)
    )
    mutated_set = set()
    for i in range(100):
        mutator = PythonMutator(engine)
        tree = ast.parse(CODE)
        mutated = mutator.visit(tree)
        if engine.mutations == 0:
            continue
        mutated_set.add(astunparse.unparse(mutated))
        engine = engine.new()

    for m in mutated_set:
        print(m)
