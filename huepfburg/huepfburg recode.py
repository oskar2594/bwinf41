with open(input("Pfad: ")) as f:
    n_nodes, n_edges = map(int, f.readline().split(" "))
    graph = [set() for i in range(n_nodes)]
    for i in range(n_edges):
        startnode, endnode = map(int, f.readline().split(" "))
        # - 1 weil python-indizes bei 0 anfangen, aber knoten in eingabe bei 1
        graph[startnode - 1].add(endnode - 1)

nodes_1 = {0}
nodes_2 = {1}

pair_origins = {(0, 1) : (-1, -1)}
run = True
while run:
    old_nodes_1 = set(nodes_1)
    old_nodes_2 = set(nodes_2)
    nodes_1 = set()
    nodes_2 = set()
    single_origins_1 = {}
    single_origins_2 = {}
    for old_node in old_nodes_1:
        for new_node in graph[old_node]:
            single_origins_1[new_node] = old_node
            nodes_1.add(new_node)

    for old_node in old_nodes_2:
        for new_node in graph[old_node]:
            single_origins_2[new_node] = old_node
            nodes_2.add(new_node)

    new_pair = False
    for node_1 in nodes_1:
        for node_2 in nodes_2:
            if (node_1, node_2) not in pair_origins:
                new_pair = True
                pair_origins[(node_1, node_2)] = (single_origins_1[node_1], single_origins_2[node_2])
            if node_1 == node_2:
                print("Treffen möglich!")
                path1 = [node_1]
                path2 = [node_2]
                while pair_origins[(path1[-1], path2[-1])] != (-1, -1):
                    origin = pair_origins[(path1[-1], path2[-1])]
                    path1.append(origin[0])
                    path2.append(origin[1])
                print("Weg 1:")
                print(" ".join("{:4}".format(x + 1) for x in reversed(path1)))
                print("Weg 2:")
                print(" ".join("{:4}".format(x + 1) for x in reversed(path2)))
                run = False
    if not new_pair:
        print("Treffen nicht möglich!")
        run = False
