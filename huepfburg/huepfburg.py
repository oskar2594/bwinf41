from operator import truediv
import numpy as np

with open(input("Path: ")) as f:
    n_nodes, n_edges = map(int, f.readline().split(" "))
    graph = np.zeros((n_nodes, n_nodes), dtype=bool)
    for _ in range(n_edges):
        startnode, endnode = map(int, f.readline().split(" "))
        graph[startnode - 1, endnode - 1] = True

combinations_visited = np.zeros((n_nodes, n_nodes), dtype=bool)
origin = np.ndarray((n_nodes, n_nodes, 2), dtype=int)
origin[:, :, :] = -1
origin[0, 1] = -2
identity = np.identity(n_nodes, dtype=bool)
pos1 = np.zeros((n_nodes,), dtype=bool)
pos2 = np.zeros((n_nodes,), dtype=bool)
pos1[0] = True
pos2[1] = True
while (
    not (combinations_visited * identity).any()
    and pos1.any()
    and pos2.any()
):
    combinations = pos1.reshape(-1, 1) & pos2.reshape(1, -1)
    pos1 = (combinations & ~combinations_visited).any(axis=1) | (
        pos1 & ~combinations.any(axis=1)
    )
    pos2 = (combinations & ~combinations_visited).any(axis=0) | (
        pos2 & ~combinations.any(axis=0)
    )
    combinations_visited |= combinations
    pos1_old, pos2_old = pos1, pos2
    pos1 = pos1 @ graph
    pos2 = pos2 @ graph
    for i in range(n_nodes):
        for k in range(n_nodes):
            if pos1[i] and pos2[k]:
                if origin[i, k, 0] == -1:
                    for m in range(n_nodes):
                        if pos1_old[m] and graph[m, i]:
                            origin[i, k, 0] = m
                            break
                if origin[i, k, 1] == -1:
                    for m in range(n_nodes):
                        if pos2_old[m] and graph[m, k]:
                            origin[i, k, 1] = m
                            break
print("done")
if (combinations_visited.diagonal()).any():
    meet = np.where(combinations_visited.diagonal())[0][0]
    route1, route2 = [meet + 1], [meet + 1]
    o1, o2 = origin[meet, meet]
    while o1 > -1:
        route1.append(o1 + 1)
        route2.append(o2 + 1)
        o1, o2 = origin[o1, o2]
    print("Weg 1: ")
    print(" ".join(str(x) for x in reversed(route1)))
    print("Weg 2: ")
    print(" ".join(str(x) for x in reversed(route2)))
else:
    print("Kein Weg")