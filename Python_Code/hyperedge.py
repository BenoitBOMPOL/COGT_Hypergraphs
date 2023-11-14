"""
    Class module for hyperedge
"""

class HyperEdge:
    def __init__(self, tails: list[int]):
        self.tails = tails

    def __str__(self) -> str:
        return "(" + ",".join([chr(64 + v) for v in self.tails]) + ")"