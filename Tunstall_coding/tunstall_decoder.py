import numpy as np
def add_gaussian_noise(encoded, sigma=0.5):
    signal = np.array([1 if bit == '1' else -1 for bit in encoded])
    noise = np.random.normal(0, sigma, len(signal))
    noisy_signal = signal + noise
    noisy_bits = ['1' if s > 0 else '0' for s in noisy_signal]

    return ''.join(noisy_bits)

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
def compute_accuracy(original, decoded):
    min_len = min(len(original), len(decoded))
    correct = sum(1 for i in range(min_len) if original[i] == decoded[i])
    return correct / len(original)
def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))




