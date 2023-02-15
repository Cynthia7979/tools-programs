from itertools import chain, combinations

E = []  # Empty set

def powerset(iterable: iter):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    S = list(iterable)
    subsets_with_repeats = list(chain.from_iterable(combinations(S, r) for r in range(len(S)+1)))
    powerset_no_repeat = []
    for subset in subsets_with_repeats:
        if subset not in powerset_no_repeat:
            powerset_no_repeat.append(list(subset))
        if len(powerset_no_repeat) == 2 ** len(S):  # We've collected all the elements
            break
    return powerset_no_repeat
    

def main(S):
    p1 = powerset(S)
    p2 = powerset(p1)
    print(p2)
    print(S in p2)
    print(p2.index(S))
    print(str(p2[:6]).replace('[', '\\{').replace(']', '\\}').replace('\\{\\}', '\\emptyset'))

if __name__ == "__main__":
    main([E, [E], [[E]]])
