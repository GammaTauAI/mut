from numpy import random

# Mutation operators
# AOR: Arithmetic Operator Replacement: a + b -> a - b
# LCR: Logical Connector Replacement: a and b -> a or b
# ROR: Relational Operator Replacement: a > b -> a < b
# UOI: Unary Operator Insertion: b -> not b, i -> i + 1
# SBR: Statement Block Replacement: stmt -> 0 TODO

from typing import Literal, Callable, Any

Node = Any  # TODO: fix later


class Converter:
    def __init__(self):
        pass

    def convert_to_div(self, node):
        raise NotImplementedError

    def convert_to_mult(self, node):
        raise NotImplementedError

    def convert_to_add(self, node):
        raise NotImplementedError

    def convert_to_sub(self, node):
        raise NotImplementedError

    def convert_to_binop_a(self, node):
        raise NotImplementedError

    def convert_to_binop_b(self, node):
        raise NotImplementedError

    def convert_to_boolop_a(self, node):
        raise NotImplementedError

    def convert_to_boolop_b(self, node):
        raise NotImplementedError

    def convert_to_and(self, node):
        raise NotImplementedError

    def convert_to_or(self, node):
        raise NotImplementedError

    def convert_to_true(self, node):
        raise NotImplementedError

    def convert_to_false(self, node):
        raise NotImplementedError

    def convert_to_gt(self, node):
        raise NotImplementedError

    def convert_to_lt(self, node):
        raise NotImplementedError

    def convert_to_gte(self, node):
        raise NotImplementedError

    def convert_to_lte(self, node):
        raise NotImplementedError

    def convert_to_eq(self, node):
        raise NotImplementedError

    def convert_to_neq(self, node):
        raise NotImplementedError

    def convert_to_not(self, node):
        raise NotImplementedError

    def convert_to_increment(self, node):
        raise NotImplementedError

    def convert_to_decrement(self, node):
        raise NotImplementedError


class EngineConfig:
    def __init__(
            self,
            aor_op_rate=0.2,
            lcr_op_rate=0.2,
            ror_op_rate=0.2,
            binop_expr_rate=0.1,
            boolop_expr_rate=0.1,
            num_lit_rate=0.1,
            max_mutations=1,
    ):
        self.aor_op_rate = aor_op_rate
        self.lcr_op_rate = lcr_op_rate
        self.ror_op_rate = ror_op_rate
        self.binop_expr_rate = binop_expr_rate
        self.boolop_expr_rate = boolop_expr_rate
        self.num_lit_rate = num_lit_rate
        self.max_mutations = max_mutations


class Engine:
    def __init__(
            self,
            config: EngineConfig = EngineConfig(),
            seed=1337
    ):
        self.config = config
        self.rng = random.default_rng(seed)
        self.mutate_calls = 0
        self.already_mutated = []
        self.mutations = 0

    def new(self):
        engine = Engine(config=self.config, seed=self.rng.integers(0, 2 ** 32))
        engine.already_mutated = self.already_mutated
        return engine

    def pick(self, iterable):
        return self.rng.choice(iterable)

    def mutate_node(self, node, conv_fn, rate):
        self.mutate_calls += 1
        if self.mutations < self.config.max_mutations \
                and self.mutate_calls not in self.already_mutated \
                and self.rng.random() < rate:
            self.mutations += 1
            self.already_mutated.append(self.mutate_calls)
            return conv_fn(node)
        else:
            return node


class Mutator(Converter):
    AOR_OPS = ["+", "-", "*", "/"]
    BIN_OPS = ["a", "b"]
    BOOL_OPS = ["a", "b", "true", "false", "not"]
    LCR_OPS = ["and", "or"]
    ROR_OPS = [">", "<", ">=", "<=", "==", "!="]
    NUM_LIT_OP = ["++", "--"]

    def __init__(self, engine: Engine):
        self.engine = engine

    def mutate_aor_op(self, node, current: Literal["+", "-", "*", "/"]):
        possible = [op for op in self.AOR_OPS if op != current]
        picked = self.engine.pick(possible)

        conv_fn = None
        if picked == "+":
            conv_fn = self.convert_to_add
        elif picked == "-":
            conv_fn = self.convert_to_sub
        elif picked == "*":
            conv_fn = self.convert_to_mult
        elif picked == "/":
            conv_fn = self.convert_to_div
        else:
            raise Exception("Unknown operator")

        return self.engine.mutate_node(node, conv_fn, self.engine.config.aor_op_rate)

    def mutate_binop_expr(self, node):
        picked = self.engine.pick(self.BIN_OPS)

        conv_fn = None
        if picked == "a":
            conv_fn = self.convert_to_binop_a
        elif picked == "b":
            conv_fn = self.convert_to_binop_b
        else:
            raise Exception("Unknown operator")

        return self.engine.mutate_node(node, conv_fn, self.engine.config.binop_expr_rate)

    def mutate_lcr(self, node, current: Literal["and", "or"]):
        possible = [op for op in self.LCR_OPS if op != current]
        picked = self.engine.pick(possible)

        conv_fn = None
        if picked == "and":
            conv_fn = self.convert_to_and
        elif picked == "or":
            conv_fn = self.convert_to_or
        else:
            raise Exception("Unknown operator")

        return self.engine.mutate_node(node, conv_fn, self.engine.config.lcr_op_rate)

    def mutate_boolop_expr(self, node):
        picked = self.engine.pick(self.BOOL_OPS)

        conv_fn = None
        if picked == "a":
            conv_fn = self.convert_to_boolop_a
        elif picked == "b":
            conv_fn = self.convert_to_boolop_b
        elif picked == "true":
            conv_fn = self.convert_to_true
        elif picked == "false":
            conv_fn = self.convert_to_false
        elif picked == "not":
            conv_fn = self.convert_to_not
        else:
            raise Exception("Unknown operator")

        return self.engine.mutate_node(node, conv_fn, self.engine.config.boolop_expr_rate)

    def mutate_ror(self, node, current: Literal[">", "<", ">=", "<=", "==", "!="]):
        possible = [op for op in self.ROR_OPS if op != current]
        picked = self.engine.pick(possible)

        conv_fn = None
        if picked == ">":
            conv_fn = self.convert_to_gt
        elif picked == "<":
            conv_fn = self.convert_to_lt
        elif picked == ">=":
            conv_fn = self.convert_to_gte
        elif picked == "<=":
            conv_fn = self.convert_to_lte
        elif picked == "==":
            conv_fn = self.convert_to_eq
        elif picked == "!=":
            conv_fn = self.convert_to_neq
        else:
            raise Exception("Unknown operator")

        return self.engine.mutate_node(node, conv_fn, self.engine.config.ror_op_rate)

    def mutate_number_literal(self, node):
        picked = self.engine.pick(self.NUM_LIT_OP)

        conv_fn = None
        if picked == "++":
            conv_fn = self.convert_to_increment
        elif picked == "--":
            conv_fn = self.convert_to_decrement

        return self.engine.mutate_node(node, conv_fn, self.engine.config.num_lit_rate)
