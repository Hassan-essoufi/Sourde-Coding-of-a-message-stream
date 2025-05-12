import math
import numpy as np

def binary_fix(i, n):
    return bin(i)[2:].zfill(n)

def build_tunstall_tree(alphabet, probs, n):
    leaves = []
    tree = []

    for sym, p in zip(alphabet, probs):
        node = {"seq": sym, "prob": p, "children": []}
        leaves.append(node)
        tree.append(node)

    N = len(alphabet)
    k = (2 ** n - N) // (N - 1) if N != 1 else 1

    for _ in range(k):
        leaf_to_expand = max(leaves, key=lambda x: x["prob"])
        leaves.remove(leaf_to_expand)
        for sym, p in zip(alphabet, probs):
            new_seq = leaf_to_expand["seq"] + sym
            new_prob = leaf_to_expand["prob"] * p
            child = {"seq": new_seq, "prob": new_prob, "children": []}
            leaf_to_expand["children"].append(child)
            leaves.append(child)

    return tree, leaves 

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

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))

def decode_binary(encoded, leaves):
    decoded = ""
    i = 0
    code_to_seq = {node["code"]: node["seq"] for node in leaves}
    seq_freq = {node["seq"]: node["prob"] for node in leaves}  
    n = len(next(iter(code_to_seq.keys()))) 

    while i < len(encoded):
        found = False
        current_code = encoded[i:i+n]

        if current_code in code_to_seq:
            decoded += code_to_seq[current_code]
            i += n
            found = True
        else:
            possible_matches = []
            for code in code_to_seq:
                if len(code) == len(current_code) and hamming_distance(code, current_code) <= 2:
                    possible_matches.append((code_to_seq[code], seq_freq[code_to_seq[code]]))
            if possible_matches:
                best_seq = max(possible_matches, key=lambda x: x[1])[0]
                decoded += best_seq
            else:
                decoded += "?" 
                i += n  


    return decoded

def add_gaussian_noise(encoded, sigma=0.5):
    signal = np.array([1 if bit == '1' else -1 for bit in encoded])
    noise = np.random.normal(0, sigma, len(signal))
    noisy_signal = signal + noise
    noisy_bits = ['1' if s > 0 else '0' for s in noisy_signal]

    return ''.join(noisy_bits)

n = int(input("Enter number of bits: "))
string = input("Enter the string to be encoded: ")

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

# Add noise
noisy_encoded = add_gaussian_noise(encoded, sigma=0.5)
print("Encoded string (noisy):", noisy_encoded)

# Decoding
decoded = decode_binary(noisy_encoded, leaves)
print("Decoded string:", decoded)

def compute_entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)

def compute_avg_length(leaves):
    total = 0
    for node in leaves:
        total += len(node["seq"]) * node["prob"]
    return total

def compute_accuracy(original, decoded):
    min_len = min(len(original), len(decoded))
    correct = sum(1 for i in range(min_len) if original[i] == decoded[i])
    return correct / len(original)

# Efficiency calculations
entropy = compute_entropy(probs)
avg_length = compute_avg_length(leaves)
efficiency = entropy / avg_length
print(f"\nEntropy H(X): {entropy:.4f}")
print(f"Average sequence length: {avg_length:.4f}")
print(f"Efficiency (H(X)/L): {efficiency:.4f}")
print(f"Redundancy (R) : {1 - efficiency:.4f}")

# Decoding accuracy rate
accuracy = compute_accuracy(string, decoded)
print(f"Decoding accuracy: {accuracy*100:.2f}%")
