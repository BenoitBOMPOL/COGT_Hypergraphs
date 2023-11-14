#!/usr/bin/env python3
"""
    Misc functions used pretty much everywhere
"""
from itertools import combinations

def get_all_subsets(elements : list[int]) -> list[list[int]]:
    co_elements : list[int] = sorted(elements)
    all_subsets : list[list[int]] = []
    for i in range(1, len(co_elements)):
        subsets = [list(el) for el in combinations(co_elements, i)]
        all_subsets.extend(subsets)
    return all_subsets

def build_minimal_inclusionwise(elements: list[list[int]]) -> list[list[int]]:
    add_to_m : list[bool] = [True for _ in elements]
    for ix, x, iy, y in [(iix, xx, iiy, yy) for iix, xx in enumerate(elements) for iiy, yy in enumerate(elements) if iiy > iix]:
        if set(x).issubset(set(y)) and add_to_m[iy]:
            add_to_m[iy] = False
        if set(y).issubset(set(x)) and add_to_m[ix]:
            add_to_m[ix] = False
    return[e for (b, e) in zip(add_to_m, elements) if b]

# TODO : Building every partitions of V
def get_subsets(elements : list[int], full_set_allowed : bool) -> list[list[int]]:
    upperbound = len(elements) + int(full_set_allowed)
    return [list(p) for p in combinations(elements, upperbound)]

if __name__ == "__main__":
    ELEMENTS = list(range(1, 7))
    for pos_subsets in get_subsets(ELEMENTS, True):
        print(pos_subsets)
    
    for neg_subsets in get_subsets(ELEMENTS, False):
        print(neg_subsets)