import math
import pickle
from os.path import exists

import graded_roots
import tau_extrema_sequence

def generate_data(p_max, q_max):
    for p in range(2, p_max+1):
        for q in range(3, q_max+1):
            if math.gcd(p,q) == 1:
                for r in range(2, 2*p*q+2):
                    if math.gcd(p,r) == 1 and math.gcd(q,r) == 1:
                        if set([p,q,r]) == set([2,3,5]):
                            break
                        save_path = f"maximal_monotone_subroot_data/{p}, {q}, {r}.pickle"
                        if not exists(save_path):
                            with open(save_path, "wb") as f: 
                                pickle.dump(graded_roots.maximal_monotone_subroot(tau_extrema_sequence.extrema_sequence(p,q,r)), f)

def read_data(p,q,r):
    with open(f"maximal_monotone_subroot_data/{p}, {q}, {r}.pickle", "rb") as f:
        subroot = pickle.load(f)
        pop_keys = []
        min_stem = 1000000
        for key in subroot:
            if subroot[key] == key:
                pop_keys.append(key)
                if key < min_stem:
                    min_stem = key

        for key in pop_keys:
            subroot.pop(key)
        
        subroot[min_stem] = min_stem
                
        return subroot

if __name__ == "__main__":
    generate_data(20,30)
    # print(read_data(5,19,183))