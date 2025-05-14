import matplotlib.pyplot as plt
import networkx as nx
import heapq

def create_node(sequence, prob):
    return {
        "sequence": sequence,
        "prob": prob,
        "children": []
    }

def build_tunstall_tree(symbol_probs, max_leaves):
    root = create_node("", 1.0)
    heap = [(-root["prob"], root)]  # max-heap by negative prob
    leaves = []

    while len(heap) + len(leaves) < max_leaves:
        _, node = heapq.heappop(heap)
        for sym, p in symbol_probs.items():
            child = create_node(node["sequence"] + sym, node["prob"] * p)
            node["children"].append(child)
            heapq.heappush(heap, (-child["prob"], child))  # Max-heap with -prob
        if not node["children"]:
            leaves.append(node)

    # Remaining nodes in heap are leaves
    for _, leaf in heap:
        leaves.append(leaf)

    return root, leaves

def build_graph(node, graph, parent_name=None):
    name = f"{node['sequence']}\n({node['prob']:.3f})"
    graph.add_node(name)
    if parent_name:
        graph.add_edge(parent_name, name)
    for child in node["children"]:
        build_graph(child, graph, name)

def draw_tunstall_tree(root):
    G = nx.DiGraph()
    build_graph(root, G)
    pos = hierarchy_pos(G, list(G.nodes)[0])
    plt.figure(figsize=(14, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightyellow", font_size=10, font_weight="bold")
    plt.title("Arbre de Tunstall (Sans POO)")
    plt.show()

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root))
    if parent:
        neighbors = [n for n in neighbors if n != parent]
    if len(neighbors) != 0:
        dx = width / len(neighbors)
        nextx = xcenter - width / 2 - dx / 2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                pos=pos, parent=root)
    return pos

# Exemple : probabilités des symboles
probs = {
    'a': 0.45,
    'b': 0.13,
    'c': 0.12,
    'd': 0.16,
    'e': 0.09,
    'f': 0.05
}

racine, feuilles = build_tunstall_tree(probs, max_leaves=16)
draw_tunstall_tree(racine)
