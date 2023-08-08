from numpy import random
# Mutation operators
# AOR: Arithmetic Operator Replacement: a + b -> a - b
# LCR: Logical Connector Replacement: a and b -> a or b
# ROR: Relational Operator Replacement: a > b -> a < b
# UOI: Unary Operator Insertion: a -> not a (only in conditionals)
# SBR: Statement Block Replacement: stmt -> 0

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


class Engine:
    def __init__(self, mutation_rate: float = 0.1, seed=1337):
        self.mutation_rate = mutation_rate
        self.rng = random.default_rng(seed)

    def pick(self, iterable):
        return self.rng.choice(iterable)

    def mutate(self, node, conv_fn):
        if self.rng.random() < self.mutation_rate:
            return conv_fn(node)
        else:
            return node


class Mutator(Converter):
    AOR_OPS = ["+", "-", "*", "/"]

    def __init__(self, engine: Engine):
        self.engine = engine

    def mutate_aor(self, node, current: Literal["+", "-", "*", "/"]):
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

        return self.engine.mutate(node, conv_fn)
