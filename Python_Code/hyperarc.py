"""
    Class module for HyperArcs
"""

class HyperArc:
    def __init__(self, tails: list[int], head : int):
        self.tails = tails
        self.head = head

    def __str__(self) -> str:
        return "(" + ",".join([chr(64 + v) for v in self.tails]) + f") -> {chr(64 + self.head)}"
    
    def reorient(self, new_head : int):
        assert new_head in self.tails
        self.tails.append(self.head)
        self.tails.remove(new_head)
        self.head = new_head
        