import math
def probabilities_freq(string):
    freq = {}
    for ch in string:
        freq[ch] = freq.get(ch, 0) + 1
    alphabet = list(freq.keys())
    probabilities = {ch:freq[ch] / len(string) for ch in alphabet}
    return probabilities

def build_huffman_tree(probabilities):
    nodes = [(char, prob) for char, prob in probabilities.items()]
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

def huff_encoder(text,probabilities):
    tree = build_huffman_tree(probabilities)
    huffman_codes = generate_codes(tree)
    encoded_text = ""
    for char in text :
        encoded_text += huffman_codes[char] 
    return encoded_text

def metrics(probabilities, codes):
    avg_length = sum(probabilities[char] * len(code) for char, code in codes.items())
    
    entropy = -sum(p * math.log2(p) for p in probabilities.values())
    
    efficiency = entropy / avg_length if avg_length > 0 else 0
    
    redundancy = 1 - efficiency

    return avg_length, entropy, efficiency, redundancy

