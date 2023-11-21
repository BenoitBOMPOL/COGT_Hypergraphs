#!/usr/bin/env python3
"""
    Code based on 
        Directed hypergraph connectivity augmentation 
        by hyperarc reorientations
"""

from hypergraph import HyperGraph
from hyperarc import HyperArc

def main_algorithm(H : HyperGraph, r : int):
    assert r in H.vertices                  # Step 1 : Choose a vertex in H
    if (H.stopping_criteria(r)):
        return False
    risky_set = H.risky(r)[0]               # Step 4 : Take a set in R
    print(f"R = {risky_set}")
    
    if risky_set in H.in_tight(r):          # Step 5, 6 : Finding and reorienting P
        s, t, safe_source, safe_sink, hyperpath = H.alg2(risky_set, r)
        print("+++ Algo 2 +++")
        print(f"\tsafe_source : {chr(safe_source + 64)}")
        print(f"\tsafe_sink : {chr(safe_sink + 64)}\n")
        
        l = len(hyperpath)
        for i in range(l - 1, 0, -1):
            head_to_reorient = hyperpath[i - 1].head
            for h in H.hyperarcs:
                if h == hyperpath[i]:
                    print(f"\tReorient {h} towards {chr(64 + head_to_reorient)}")
                    h.reorient(head_to_reorient)
                    print(f"\t\t After reorientation, H is {H.get_k()}-hyperarc-connected.")

        for h in H.hyperarcs:
            if h == hyperpath[0]:
                print(f"\tReorient {h} towards {chr(64 + safe_source)}")
                h.reorient(safe_source)
                print(f"\t\t After reorientation, H is {H.get_k()}-hyperarc-connected.")
    elif risky_set in H.out_tight(r):
        s, t, safe_source, safe_sink, hyperpath = H.alg3(risky_set, r)
        print("+++ Algo 3 +++")
        print(f"\tsafe_source : {chr(safe_source + 64)}")
        print(f"\tsafe_sink : {chr(safe_sink + 64)}\n")
        for h in H.hyperarcs:
            if h == hyperpath[0]:
                print(f"\tReorient {h} towards {chr(64 + safe_source)}")
                h.reorient(safe_source)
                print(f"\t\t After reorientation, H is {H.get_k()}-hyperarc-connected.")
        l = len(hyperpath)
        for i in range(1, l):
            head_to_reorient = hyperpath[i - 1].head
            for h in H.hyperarcs:
                if h == hyperpath[i]:
                    print(f"\tReorient {h} towards {chr(64 + head_to_reorient)}")
                    h.reorient(head_to_reorient)
                    print(f"\t\t After reorientation, H is {H.get_k()}-hyperarc-connected.")
    print()
    return True


if __name__ == "__main__":
    VERTICES = list(range(1, 7))
    TAILS_SET : list[list[int]] = [[1], [2], [3], [4], [5], [6], [1], [1, 3], [3], [3], [5], [5], [1, 2], [1, 2, 3], [3, 4], [3, 4, 5], [5, 6], [6, 1]]
    HEADS_SET : list[int] = [2, 3, 4, 5, 6, 1, 6, 2, 2, 4, 4, 6, 3, 4, 5, 6, 1, 2]
    
    HYPERARCS = [HyperArc(tails, head) for (tails, head) in zip(TAILS_SET, HEADS_SET)]
    
    H = HyperGraph(VERTICES, HYPERARCS)
    print("+++ Hyperarcs +++")
    for h in H.hyperarcs:
        print(h)
    print("--- Hyperarcs ---")
    print(f"H is {H.k}-hyperarc-connected.")

    r = 1
    to_continue = True
    while to_continue:
        to_continue = main_algorithm(H, r)
    H.update_k()

    print(f"H is {H.k}-hyperarc-connected.")

