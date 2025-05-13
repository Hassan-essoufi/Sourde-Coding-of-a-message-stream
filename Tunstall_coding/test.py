from tustall_encoder import build_tunstall_tree, assign_codes, print_dictionary, encode_string, compute_entropy, compute_avg_length
from tunstall_decoder import decode_binary, add_gaussian_noise, compute_accuracy
#example
n = 3
string = "aaabbbbbbbdddddddccccccccccccaaaddddddddabbbcc"

# Calculate probabilities
freq = {}
for ch in string:
    freq[ch] = freq.get(ch, 0) + 1

alphabet = list(freq.keys())
probs = [freq[ch] / len(string) for ch in alphabet]

# Build the tree
tree, leaves = build_tunstall_tree(alphabet, probs, n)
assign_codes(leaves, n)

# Display the dictionary
print_dictionary(leaves)

encoded = encode_string(string, leaves)
print("\nEncoded string (clean):", encoded)

# tunstall code metrics
entropy = compute_entropy(probs)
avg_length = compute_avg_length(leaves)
efficiency = entropy / avg_length
print(f"\nEntropy H(X): {entropy:.4f}")
print(f"Average sequence length: {avg_length:.4f}")
print(f"Efficiency (H(X)/L): {efficiency:.4f}")
print(f"Redundancy (R) : {1 - efficiency:.4f}")

# Add noise
noisy_encoded = add_gaussian_noise(encoded, sigma=0.5)
print("Encoded string (noisy):", noisy_encoded)

# Decoding
decoded = decode_binary(noisy_encoded, leaves)
print("Decoded string:", decoded)

# Decoding accuracy rate
accuracy = compute_accuracy(string, decoded)
print(f"Decoding accuracy: {accuracy*100:.2f}%")
