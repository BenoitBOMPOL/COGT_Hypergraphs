"""
    Class module for hypergraph (UNDIRECTED)
"""

from hyperarc import HyperArc
from misc import get_all_subsets, build_minimal_inclusionwise

class HyperGraph:
    def __init__(self, vertices : list[int], hyperarcs = list[HyperArc]) -> None:
        self.vertices = vertices
        self.hyperarcs = hyperarcs
        self.k = min([self.out_degree(subset) for subset in get_all_subsets(self.vertices)])

    
    def get_k(self):
        return min([self.out_degree(subset) for subset in get_all_subsets(self.vertices)])

    def update_k(self):
        self.k = min([self.out_degree(subset) for subset in get_all_subsets(self.vertices)])


    def in_degree(self, subset : list[int]) -> int:
        in_deg : int = 0
        for hyperarc in self.hyperarcs:
            head, tails = hyperarc.head, hyperarc.tails
            if (head in subset) and (len([tail for tail in tails if tail not in subset]) > 0):
                in_deg += 1
        return in_deg

    def out_degree(self, subset : list[int]) -> int:
        out_deg : int = 0
        for hyperarc in self.hyperarcs:
            head, tails = hyperarc.head, hyperarc.tails
            if (head not in subset) and (len([tail for tail in tails if tail in subset]) > 0):
                out_deg += 1
        return out_deg
    
    def in_tight(self, v : int) -> list[list[int]]:
        in_tight_sets : list[list[int]] = []
        for subset in get_all_subsets(self.vertices):
            if (v not in subset) and (self.in_degree(subset) == self.k):
                in_tight_sets.append(subset)
        in_tight_sets.append(self.vertices)
        return in_tight_sets
    
    def out_tight(self, v : int) -> list[list[int]]:
        out_tight_sets : list[list[int]] = []
        for subset in get_all_subsets(self.vertices):
            if (v not in subset) and (self.out_degree(subset) == self.k):
                out_tight_sets.append(subset)
        out_tight_sets.append(self.vertices)
        return out_tight_sets

    def minimal_in_tight(self, v : int) -> list[list[int]]:
        return build_minimal_inclusionwise(self.in_tight(v))

    def minimal_out_tight(self, v : int) -> list[list[int]]:
        return build_minimal_inclusionwise(self.out_tight(v))
    
    def in_dangerous(self, v: int) -> list[list[int]]:
        in_dang_sets : list[list[int]] = []
        for subset in get_all_subsets(self.vertices):
            if (v not in subset) and (self.in_degree(subset) == self.k + 1):
                in_dang_sets.append(subset)
        return in_dang_sets
    
    def out_dangerous(self, v: int) -> list[list[int]]:
        out_dang_sets : list[list[int]] = []
        for subset in get_all_subsets(self.vertices):
            if (v not in subset) and (self.out_degree(subset) == self.k + 1):
                out_dang_sets.append(subset)
        return out_dang_sets

    def risky(self, v : int) -> list[list[int]]:
        potential_risky_sets : list[list[int]] = []
        for r_m in self.in_tight(v):
            for subset in get_all_subsets(r_m):
                if subset in self.out_tight(v):
                    potential_risky_sets.append(r_m)
                    break
        for r_p in self.out_tight(v):
            for subset in get_all_subsets(r_p):
                if subset in self.in_tight(v):
                    potential_risky_sets.append(r_p)
                    break
        risky_sets = build_minimal_inclusionwise(potential_risky_sets)
        return risky_sets

    def is_a_safe_source(self, v : int, s : int, min_in_tight : list[int]) -> bool:
        assert (s in min_in_tight) and (min_in_tight in self.minimal_in_tight(v))

        for x in [xx for xx in self.out_tight(v) if s in xx]:
            if not(set(min_in_tight).issubset(x)):
                # NOTE : DINODANGER
                return False

        oud = self.out_dangerous(v)
        for x in [xx for xx in oud if (s in xx) and len([u for u in min_in_tight if u not in xx]) > 0]:
            cond = False
            for y in [o for o in self.out_tight(v) if s not in o]:
                if set(y).issubset(set(x)) and y != x:
                    cond = True
            
            if not cond:
                return False
        return True
    
    def is_a_safe_sink(self, v : int, t : int, min_out_tight : list[int]) -> bool:
        assert t in min_out_tight
        assert min_out_tight in self.minimal_out_tight(v)

        for x in [xx for xx in self.in_tight(v) if t in xx]:
            if not(set(min_out_tight).issubset(x)):
                return False
        
        out = self.in_dangerous(v)
        for x in [xx for xx in out if (t in xx) and len([w for w in min_out_tight if w not in xx]) > 0]:
            cond = False
            for y in [i for i in self.in_tight(v) if t not in i]:
                if set(y).issubset(set(x)) and y != x:
                    cond = True
            
            if not cond:
                return False
        return True

    def find_hyperarcs(self, s: int, d: int) -> list[HyperArc]:
        matching_hyperarcs = [h for h in self.hyperarcs if s in h.tails and d == h.head]
        return matching_hyperarcs
    
    def better_find_hyperpath(self, p_prim : list[tuple[int, int]], hpath : list[HyperArc] = []) -> list[HyperArc]:
        if len(p_prim) == 0:
            return hpath
        
        u, v = p_prim[-1]
        matching_hyperarcs = self.find_hyperarcs(u, v)

        if len(matching_hyperarcs) == 0:
            # Normalement, ne devrait pas arriver
            return []
        
        subprim = p_prim[:-1] # p_prim = subprim + [(u, v)]
        
        for m_h in matching_hyperarcs:
            result = self.better_find_hyperpath(subprim, hpath + [m_h])  # Rappel récursif

            if result:
                return result  # Renvoie le chemin trouvé
        
        return []


    def find_hyperpath(self, p_prim: list[tuple[int, int]]) -> list[HyperArc]:
        hyperpath = []
        for i in range(len(p_prim)):
            current_tail = p_prim[i][0]
            current_head = p_prim[i][1]

            # Find the hyperarc with the current_tail and current_head
            matching_hyperarcs = self.find_hyperarcs(current_tail, current_head)

            if not matching_hyperarcs:
                # If no matching hyperarc found, the sequence is broken
                return []

            hyperpath.append(matching_hyperarcs[0])  # Append the found hyperarc to the path

            if i < len(p_prim) - 1:
                # Check if the head of P[i] is among the tails of P[i+1]
                next_head = p_prim[i + 1][1]
                if next_head not in matching_hyperarcs[0].tails:
                    # If the condition is not met, the sequence is broken
                    return []
        
        return hyperpath
    
    def alg2(self, r_set : list[int], r : int):
        assert r_set in self.risky(r)
        assert r_set in self.in_tight(r)

        s : list[int] = [ss for ss in self.minimal_in_tight(r) if set(ss).issubset(set(r_set))][0]
        safe_source = [v for v in s if self.is_a_safe_source(r, v, s)][0]
        z : set[int] = set([safe_source])
        f : list[set[int], list[tuple[int, int]]] = [z, []]
        v_prim : list[int] = r_set

        potential_hyperarcs : list[HyperArc] = [h for h in self.hyperarcs if h.head in [w for w in v_prim if w not in z] and len(list(z.intersection(set(h.tails)))) > 0]
        while len(potential_hyperarcs) > 0:
            h = potential_hyperarcs[0]
            x, v = h.tails, h.head
            u = list(z.intersection(set(x)))[0]
            z.add(v)
            f[1].append((u, v))

            pot_q_plus_v = [t for t in self.out_tight(r) if v in t]
            q_plus_v = build_minimal_inclusionwise(pot_q_plus_v)[0]

            if set(q_plus_v).issubset(set(v_prim)) and (set(q_plus_v) != set(v_prim)):
                v_prim = list(q_plus_v)
            potential_hyperarcs = [h for h in self.hyperarcs if h.head in [w for w in v_prim if w not in z] and len(list(z.intersection(set(h.tails)))) > 0]

        t = v_prim
        safe_sink = [v for v in t if self.is_a_safe_sink(r, v, t)][0]

        def find_path(current, end):
            for (u, v) in f[1]:
                if u == current:
                    if v == end:
                        return [(u, v)]
                    new_path = find_path(v, end)
                    if new_path:
                        return [(u, v)] + new_path
            return None
    
        p_prim = find_path(safe_source, safe_sink)

        hyperpath = self.better_find_hyperpath(p_prim)[::-1]

        return s, t, safe_source, safe_sink, hyperpath


    def alg3(self, r_set : list[int], r : int):
        assert r_set in self.risky(r)
        assert r_set in self.out_tight(r)

        t : list[int] = [tt for tt in self.minimal_out_tight(r) if set(tt).issubset(set(r_set))][0]
        safe_sink : int = [v for v in t if self.is_a_safe_sink(r, v, t)][0]
        z : set[int] = set([safe_sink])
        f : list[set[int], list[tuple[int, int]]] = [z, []]
        v_prim : list[int] = r_set

        potential_hyperarcs : list[HyperArc] = [h for h in self.hyperarcs if (h.head in z) and len([w for w in set(h.tails).intersection(set(v_prim)) if w not in z]) > 0]
        while len(potential_hyperarcs) > 0:
            h = potential_hyperarcs[0]
            x, v = h.tails, h.head
            while len([w for w in set(x).intersection(set(v_prim)) if w not in z]) > 0:
                u = [w for w in set(x).intersection(set(v_prim)) if w not in z][0]
                z.add(u)
                f[1].append((u, v))
            
                pot_q_minus_u = [t for t in self.in_tight(r) if u in t]
                q_minus_u = build_minimal_inclusionwise(pot_q_minus_u)[0]
                if set(q_minus_u).issubset(set(v_prim)) and (set(q_minus_u) != set(v_prim)):
                    v_prim = list(q_minus_u)
            potential_hyperarcs = [h for h in self.hyperarcs if (h.head in z) and len([w for w in set(h.tails).intersection(set(v_prim)) if w not in z]) > 0]
        
        s = v_prim
        safe_source = [v for v in s if self.is_a_safe_source(r, v, s)][0]

        # Finding the path
        def find_path(current, end):
            for (u, v) in f[1]:
                if u == current:
                    if v == end:
                        return [(u, v)]
                    new_path = find_path(v, end)
                    if new_path:
                        return [(u, v)] + new_path
            return None
        
        p_prim = find_path(safe_source, safe_sink)
        hyperpath = self.find_hyperpath(p_prim)
        return s, t, safe_source, safe_sink, hyperpath
            

    def stopping_criteria(self, r : int) -> bool:
        assert r in self.vertices
        prev_k = self.k
        self.update_k()
        if prev_k == self.k:
            return False
        return True