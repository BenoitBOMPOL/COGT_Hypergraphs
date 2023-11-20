import itertools

V = {"A", "B", "C", "D", "E", "F"}
E0 = [({"A"}, "B"),
     ({"A"}, "F"),

     ({"B"}, "C"),
     
     ({"C"}, "D"),
     ({"C"}, "D"),
     ({"C"}, "B"),
     
     ({"D"}, "E"),
     
     ({"E"}, "F"),
     ({"E"}, "F"),
     ({"E"}, "D"),
     
     ({"F"}, "A"),
     
     ({"A", "B"}, "C"), # cyan
     ({"A", "C"}, "B"), # grey
     ({"C", "D"}, "E"), # blue
     ({"E", "F"}, "A"), # yellow
     ({"A", "B", "C"}, "D"), # red
     ({"C", "D", "E"}, "F"), # green
     ({"F", "A"}, "B"), # magenta
     ]

E1 = [({"A"}, "B"),
     ({"A"}, "F"),

     ({"B"}, "C"),
     
     ({"C"}, "D"),
     ({"C"}, "D"),
     ({"C"}, "B"),
     
     ({"D"}, "E"),
     
     ({"E"}, "F"),
     ({"E"}, "F"),
     ({"E"}, "D"),
     
     ({"F"}, "A"),
     
     ({"A", "B"}, "C"), # cyan
     ({"A", "B"}, "C"), # grey # modified
     ({"C", "D"}, "E"), # blue
     ({"E", "F"}, "A"), # yellow
     ({"A", "B", "C"}, "D"), # red
     ({"C", "D", "E"}, "F"), # green
     ({"F", "A"}, "B"), # magenta
     ]

E2 = [({"A"}, "B"),
     ({"A"}, "F"),

     ({"B"}, "C"),
     
     ({"C"}, "D"),
     ({"C"}, "D"),
     ({"C"}, "B"),
     
     ({"D"}, "E"),
     
     ({"E"}, "F"),
     ({"E"}, "F"),
      ({"D"}, "E"), # modified
     
     ({"F"}, "A"),
     
     ({"A", "B"}, "C"), # cyan
     ({"A", "B"}, "C"), # grey # modified
     ({"C", "D"}, "E"), # blue
     ({"E", "F"}, "A"), # yellow
     ({"A", "B", "C"}, "D"), # red
     ({"C", "D", "E"}, "F"), # green
     ({"F", "A"}, "B"), # magenta
     ]

E = E1
Tp = [["A", "B", "C", "D", "E", "F"]]
Tm = [["A", "B", "C", "D", "E", "F"]]
Dp = []
Dm = []
Mp = []
Mm = []
M = []
R = []  

def deg_out(X):
    count = 0
    for tail, head in E:
        done = False
        for x in X:
            if done:
                continue
            if x in tail and head not in X and not done: 
                count += 1
                done = True
    return count
            
def deg_in(X):
    count = 0
    for tail, head in E:
        if head in X:
            done = False
            for x in head:
                if done: 
                    continue
                if x not in X and not done:
                    count += 1
                    done = True
    return count

def min_inclusion_wise(S):
    res = []
    for set in S:
        min_incl = True
        for set2 in S:
            if set2 != set:
                is_included = True
                for x in set2:
                    if x not in set:
                        is_included = False
                if is_included:
                    min_incl = False
        if min_incl:
            res.append(set)
    return res

r = "A" 

# compute Tp, Tm and Dp, Dm
for k in range(len(V)):
    for subset in list(itertools.combinations(V,k)):
        if r in subset:
            continue
        subset = [x for x in subset]
        if deg_out(subset) == 2:
            Tp.append(subset)
        if deg_in(subset) == 2:
            Tm.append(subset)
        if deg_out(subset) == 3:
            Dp.append(subset)
        if deg_in(subset) == 3:
            Dm.append(subset)

# compute Mp    
Mp = min_inclusion_wise(Tp)

# compute Mm    
Mm = min_inclusion_wise(Tm)

# compute M
Mu = []
for m in Mp:
    Mu.append(m)
for m in Mm:
    if m not in Mu:
        Mu.append(m)
M = min_inclusion_wise(Mu)

# compute R
for r in Tm:
    valide = False
    for s in Tp:
        contains = True
        for x in s:
            if x not in r:
                contains = False
        if contains:
            valide = True
    if valide and r not in R:
        R.append(r)
for r in Tp:
    valide = False
    for s in Tm:
        contains = True
        for x in s:
            if x not in r:
                contains = False
        if contains:
            valide = True
    if valide and r not in R:
        R.append(r)

print(f"T+ : {Tp}")
print(f"T- : {Tm}")
print(f"D+ : {Dp}")
print(f"D- : {Dm}")
print(f"M+ : {Mp}")
print(f"M- : {Mm}")
print(f"M : {M}")
print(f"R : {R}")


 #for i in rdm.choices([i for i in range(self.N)], k=self.K):
hyper_conn_3 = True
for k in range(len(V)):
    for subset in list(itertools.combinations(V,k)):
        if len(subset) in [0, len(V)]:
            continue
        if deg_out(subset) < 3:
            hyper_conn_3 = False
print(f"hyper arc conn : {hyper_conn_3} ")
