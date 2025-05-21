def find(parent, i):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)
    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

def kruskal(nodes, edges):
    result = []
    i, e = 0, 0
    edges = sorted(edges, key=lambda item: item[2])
    parent, rank = {}, {}
    for node in nodes:
        parent[node] = node
        rank[node] = 0

    while e < len(nodes) - 1 and i < len(edges):
        u, v, w = edges[i]
        i += 1
        x = find(parent, u)
        y = find(parent, v)
        if x != y:
            e += 1
            result.append((u, v, w))
            union(parent, rank, x, y)
    total_cost = sum([w for u, v, w in result])
    return result, total_cost

def prim(nodes, edges):
    import heapq
    adj = {node: [] for node in nodes}
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    visited = set()
    mst = []
    total_cost = 0
    min_heap = [(0, nodes[0], None)]  # (weight, node, parent)

    while min_heap and len(visited) < len(nodes):
        w, u, parent = heapq.heappop(min_heap)
        if u in visited:
            continue
        visited.add(u)
        if parent:
            mst.append((parent, u, w))
            total_cost += w
        for edge_w, v in adj[u]:
            if v not in visited:
                heapq.heappush(min_heap, (edge_w, v, u))

    return mst, total_cost
