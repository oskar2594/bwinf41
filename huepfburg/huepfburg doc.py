# Findet Pfade, über die die Spieler sich treffen können
def find_paths(edges):
    pos1 = {1}
    pos2 = {2}
    pos1_last = set()
    pos2_last = set()
    pairs = {(1, 2)}
    pairs_last = set()
    origins = {(1, 2): (-1, -1)}
    while (not pos1 & pos2) and (pairs != pairs_last):
        pairs_last, pos1_last, pos2_last = pairs, pos1, pos2
        pos1 = {w for (v, w) in edges if v in pos1}
        pos2 = {w for (v, w) in edges if v in pos2}
        pairs = pairs | {(a, b) for a in pos1 for b in pos2}
        origins = {
            (v1, v2): (w1, w2)
            for (w1, v1) in edges
            for (w2, v2) in edges
            if w1 in pos1_last and w2 in pos2_last
        } | origins
    if pos1 & pos2:
        path = [(a := (pos1 & pos2).pop(), a)]
        while path[-1] != (1, 2):
            path.append(origins[path[-1]])
        return path[::-1]
    return None


# Graph aus Datei einlesen
edges = set()
with open(input("Pfad: ")) as f:
    while line := f.readline():
        edges.add(tuple(map(int, line.split())))

# verbindende Pfade finden
path = find_paths(edges)
if path:
    print("Treffen möglich")
    print("Pfad 1:")
    print("->".join(" {} ".format(x[0]) for x in path))
    print("Pfad 2:")
    print("->".join(" {} ".format(x[1]) for x in path))
else:
    print("Treffen nicht möglich")
