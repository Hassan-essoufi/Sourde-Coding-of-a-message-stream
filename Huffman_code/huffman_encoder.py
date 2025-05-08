import math
def build_huffman_tree(probabilities):
    # Create a list of tuples (character, probability)
    nodes = [(char, prob) for char, prob in probabilities.items()]

    # Build the Huffman tree
    while len(nodes) > 1:
        # Sort the nodes by probability
        nodes.sort(key=lambda x: x[1])
        
        # Take the two nodes with the smallest probabilities
        left = nodes.pop(0)
        right = nodes.pop(0)
        
        # Create a merged node (no character, just a combined probability)
        merged_node = (None, left[1] + right[1], left, right)
        
        # Add the merged node back to the list
        nodes.append(merged_node)

    # The last remaining node is the root of the Huffman tree
    return nodes[0]

def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    # If the node is a leaf (a character), add the code
    if node[0] is not None:
        codebook[node[0]] = prefix
    else:
        # If not a leaf, explore the left and right children
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



# Example: 
probabilities = {
    'a': 0.4,
    'b': 0.3,
    'c': 0.2,
    'd': 0.1
}

# Build the Huffman tree
huffman_tree = build_huffman_tree(probabilities)
print(huffman_tree)
# Generate the Huffman codes
huffman_codes = generate_codes(huffman_tree)

# Display the Huffman codes
for char, code in huffman_codes.items():
    print(f"{char}: {code}")

#huffman code metrics
avg, H, eff, red = metrics(probabilities, huffman_codes)
print("\nMetrics:")
print(f"  Average Codeword Length: {avg}")
print(f"  Entropy: {H}")
print(f"  Efficiency : {eff}")
print(f"  Redundancy : {red}")