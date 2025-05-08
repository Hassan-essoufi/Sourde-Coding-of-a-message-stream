import math
def build_huffman_tree(probabilities):
    nodes = [(char, prob) for char, prob in probabilities.items()]

    # Build the Huffman tree
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x[1])
        left = nodes.pop(0)
        right = nodes.pop(0)
        
        merged_node = (None, left[1] + right[1], left, right)
        
        nodes.append(merged_node)

    return nodes[0]

def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node[0] is not None:
        codebook[node[0]] = prefix
        
    else:
        generate_codes(node[2], prefix + "0", codebook)
        generate_codes(node[3], prefix + "1", codebook)

    return codebook

def metrics(probabilities, codes):
    # Average codeword length:
    avg_length = sum(probabilities[char] * len(code) for char, code in codes.items())
    
    # Entropy:
    entropy = -sum(p * math.log2(p) for p in probabilities.values())
    
    # Efficiency: 
    efficiency = entropy / avg_length if avg_length > 0 else 0
    
    # Redundancy:
    redundancy = 1 - efficiency

    return avg_length, entropy, efficiency, redundancy

