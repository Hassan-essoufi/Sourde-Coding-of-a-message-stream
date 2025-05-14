import heapq
import matplotlib.pyplot as plt
import networkx as nx

def create_node(symbol, prob, left=None, right=None):
    return {
        "symbol": symbol,
        "prob": prob,
        "left": left,
        "right": right
    }

def huffman_tree(probs):
    heap = [(prob, create_node(sym, prob)) for sym, prob in probs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        prob1, node1 = heapq.heappop(heap)
        prob2, node2 = heapq.heappop(heap)
        merged_node = create_node(None, prob1 + prob2, left=node1, right=node2)
        heapq.heappush(heap, (prob1 + prob2, merged_node))

    return heap[0][1]  # Return the node only

def build_graph(node, graph, parent=None, label=""):
    if node is None:
        return
    name = f"{node['symbol']}:{node['prob']:.2f}" if node['symbol'] else f"{node['prob']:.2f}"
    graph.add_node(name)
    if parent:
        graph.add_edge(parent, name, label=label)
    build_graph(node['left'], graph, name, "0")
    build_graph(node['right'], graph, name, "1")

def draw_huffman_tree(root):
    G = nx.DiGraph()
    root_name = f"{root['symbol']}:{root['prob']:.2f}" if root['symbol'] else f"{root['prob']:.2f}"
    build_graph(root, G)
    pos = hierarchy_pos(G, root_name)
    edge_labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title("Huffman Tree (Sans POO)")
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

# Exemple
probs = {
    'a': 0.45,
    'b': 0.13,
    'c': 0.12,
    'd': 0.16,
    'e': 0.09,
    'f': 0.05
}

tree_root = huffman_tree(probs)
draw_huffman_tree(tree_root)
