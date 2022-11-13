from itertools import product

# nächste Mögliche Positionen im Graph
def next_pos(graph, pos):
    return set().union(*(graph[p] for p in pos))


def nextState(graph, pos1, pos2, pairs, origin: dict):
    pos1_n = next_pos(graph, pos1)
    pos2_n = next_pos(graph, pos2)
    pairs_n = set(product(pos1_n, pos2_n))
    origin_n = origin | {
        (p1, p2): (
            next(w for w in pos1 if p1 in graph[pos1]),
            next(w for w in pos2 if p2 in graph[pos2]),
        )
        for p1, p2 in pairs_n
    }
    return pos1_n, pos2_n, pairs | pairs_n, origin_n

def start_path(origin, p1, p2):
    path = [p1, p2]
    while path[-1] != (0,1):
        path.append(origin[path[-1]])
    return path[::-1]

def find_path(graph, pos1, pos2, pairs, origin):
    intersection = pos1 & pos2
    if intersection:
        return start_path(origin, a := intersection.pop(), a)
    else:
        pos1_n, pos2_n, pairs_n, origin_n = nextState(graph, pos1, pos2, pairs, origin)
        if pairs_n == pairs:
            return None
        return find_path(graph, pos1_n, pos2_n, pairs_n, origin_n)

with open(input("Pfad: ")) as f:
    n_nodes, n_edges = map(int, f.readline().split(" "))
    graph = [set() for i in range(n_nodes)]
    for i in range(n_edges):
        startnode, endnode = map(int, f.readline().split(" "))
        # - 1 weil python-indizes bei 0 anfangen, aber knoten in eingabe bei 1
        graph[startnode - 1].add(endnode - 1)

path = find_path(graph, {0}, {1}, {(0, 1)}, {})
if path:
    print("Treffen möglich!")
    print("Weg 1:")
    print(" ".join("{:4}".format(x[0] + 1) for x in path))
    print("Weg 2:")
    print(" ".join("{:4}".format(x[1] + 1) for x in path))
else:
    print("Treffen nicht möglich!")
