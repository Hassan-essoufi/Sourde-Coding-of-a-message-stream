
from huffman_encoder import build_huffman_tree, generate_codes,huff_encoder ,metrics
from huffman_decoder import decode_huffman_with_noise, efficiency, hamming_distance

# Example: 
probabilities = {
    'a': 0.4,
    'b': 0.3,
    'c': 0.15,
    'd': 0.1,
    'e':0.05
}

text = "dbccbbbddddcccddddbbb"

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
print(f"  Efficiency : {eff:.4f}")
print(f"  Redundancy : {red:.4f}")

print(huff_encoder(text,probabilities))

huffman_codes = {char:code for char, code in huffman_codes.items()}

encoded_str = str(huff_encoder(text,probabilities))

decoded_str = decode_huffman_with_noise(encoded_str, huffman_codes,sigma=0.5)
efficiency_of_code = efficiency(text, decoded_str)
hamming_dist =hamming_distance(text, decoded_str)

print(f"Decoded string with noise:{decoded_str}")
print(f"efficiency: {efficiency_of_code} \n Hamming distance: {hamming_dist}")

