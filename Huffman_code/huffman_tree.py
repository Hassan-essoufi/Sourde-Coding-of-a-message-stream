import heapq
import matplotlib.pyplot as plt

def build_huffman_tree(probabilities):
    # Create a heap from the probabilities
    heap = [[prob] for prob in probabilities]
    heapq.heapify(heap)

    # Build the Huffman tree by combining the smallest nodes
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        node = [left[0] + right[0], left, right]
        heapq.heappush(heap, node)

    return heap[0] if heap else None

def draw_tree(tree):
    fig, ax = plt.subplots(figsize=(10, 6))
    positions = {}
    y_offset = [0]

    def assign_positions(node, depth=0):
        if isinstance(node, list) and len(node) == 1:
            x = y_offset[0]
            y_offset[0] += 3
        else:
            # Sort the children: smaller one goes down (y increases), larger one goes up (y decreases)
            child1, child2 = sorted([node[1], node[2]], key=lambda x: x[0])
            assign_positions(child2, depth + 1)  # larger (higher)
            assign_positions(child1, depth + 1)  # smaller (lower)
            x = (positions[id(child1)][0] + positions[id(child2)][0]) / 2
            node[1], node[2] = child2, child1  # Save visual order
        y = -depth  # depth determines vertical position
        positions[id(node)] = (x, y)

    def draw_edges(node):
        if isinstance(node, list) and len(node) == 3:
            for i, child in enumerate([node[1], node[2]]):
                x0, y0 = positions[id(node)]
                x1, y1 = positions[id(child)]
                ax.plot([x0, x1], [y0, y1], 'k-', lw=1.5)
                dx = (x1 - x0) * 0.3
                dy = (y1 - y0) * 0.3
                ax.text(x0 + dx, y0 + dy, str(i), color='red', fontsize=10)
            draw_edges(node[1])
            draw_edges(node[2])

    def draw_nodes(node):
        x, y = positions[id(node)]
        prob_label = f"{node[0]:.2f}"
        ax.add_patch(plt.Rectangle((x - 0.3, y - 0.25), 0.6, 0.5, fc='lightblue', ec='black', zorder=2))
        ax.text(x, y + 0.35, prob_label, ha='center', va='bottom', fontsize=9, fontweight='bold', zorder=3)
        if isinstance(node, list) and len(node) == 3:
            draw_nodes(node[1])
            draw_nodes(node[2])

    assign_positions(tree)
    draw_edges(tree)
    draw_nodes(tree)

    ax.set_xlim(-1, y_offset[0])
    ax.set_ylim(min(y for x, y in positions.values()) - 1, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.show()

# Example
probabilities = [0.4, 0.3, 0.2, 0.1]
tree = build_huffman_tree(probabilities)
draw_tree(tree)
