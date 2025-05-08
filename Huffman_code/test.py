
from huffman_encoder import build_huffman_tree, generate_codes, metrics
from huffman_decoder import decode_huffman_with_noise
from huffman_tree import draw_tree,huffman_tree_b
# Example: 
probabilities = {
    'a': 0.4,
    'b': 0.3,
    'c': 0.2,
    'd': 0.1
}

tree = build_huffman_tree(probabilities)
print(tree)
huffman_codes = generate_codes(tree)

for char, code in huffman_codes.items():
    print(f"{char}: {code}")

#huffman code metrics
avg, H, eff, red = metrics(probabilities, huffman_codes)
print("\nMetrics:")
print(f"  Average Codeword Length: {avg}")
print(f"  Entropy: {H}")
print(f"  Efficiency : {eff}")
print(f"  Redundancy : {red}")

probabilities_only = [value for value in probabilities.values()]
tree = huffman_tree_b(probabilities_only)
draw_tree(tree)


huffman_codes = {char:code for char, code in huffman_codes.items()

}

# Example encoded string with noise added (e.g., '0111010110' with some bit errors)
encoded_str = '0111011110'  # This is a noisy version of 'dcb'

# Decode the encoded string with noise
decoded_str = decode_huffman_with_noise(encoded_str, huffman_codes, noise_prob=0.1)

# Display the decoded string
print("Decoded string with noise:", decoded_str)
