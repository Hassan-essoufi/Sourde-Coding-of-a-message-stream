def binary_fix(i, n):
    return bin(i)[2:].zfill(n)

def build_tunstall_tree(alphabet, probs, n):
    leaves = []
    tree = []

    for sym, p in zip(alphabet, probs):
        node = {"seq": sym, "prob": p, "children": []}
        leaves.append(node)
        tree.append(node)

    # Calculate the number of extensions to make
    N = len(alphabet)
    k = (2 ** n - N) // (N - 1) if N != 1 else 1

    for _ in range(k):
        # Find the leaf with the highest probability
        leaf_to_expand = max(leaves, key=lambda x: x["prob"])
        leaves.remove(leaf_to_expand)

        # Generate its children
        for sym, p in zip(alphabet, probs):
            new_seq = leaf_to_expand["seq"] + sym
            new_prob = leaf_to_expand["prob"] * p
            child = {"seq": new_seq, "prob": new_prob, "children": []}
            leaf_to_expand["children"].append(child)
            leaves.append(child)

    return tree, leaves  # complete tree, leaves (final dictionary)

def assign_codes(leaves, n):
    for i, node in enumerate(leaves):
        node["code"] = binary_fix(i, n)

def encode_string(string, leaves):
    encoded = ""
    i = 0
    while i < len(string):
        matched = False
        for node in sorted(leaves, key=lambda x: -len(x["seq"])):
            if string.startswith(node["seq"], i):
                encoded += node["code"]
                i += len(node["seq"])
                matched = True
                break
        if not matched:
            print("No matching code found for:", string[i:])
            break
    return encoded

def print_dictionary(leaves):
    print("\nAlphabet\tCode")
    print("-------------------------")
    for node in leaves:
        print(f"{node['seq']}\t\t{node['code']}")
def compute_entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)

def compute_avg_length(leaves):
    total = 0
    for node in leaves:
        total += len(node["seq"]) * node["prob"]
    return total
