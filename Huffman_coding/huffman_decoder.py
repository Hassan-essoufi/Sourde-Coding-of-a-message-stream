import random
import numpy as np

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def add_gaussian_noise(encoded, sigma=0.5):
    signal = np.array([1 if bit == '1' else -1 for bit in encoded])
    noise = np.random.normal(0, sigma, len(signal))
    noisy_signal = signal + noise
    noisy_bits = ['1' if s > 0 else '0' for s in noisy_signal]
    return ''.join(noisy_bits)

def decode_huffman_with_noise(encoded_str, huffman_codes, sigma=0.5):
    reverse_huffman_codes = {code: char for char, code in huffman_codes.items()}
    noisy_encoded_str = add_gaussian_noise(encoded_str, sigma)
    
    decoded_str = ''
    current_code = ''
    
    for bit in noisy_encoded_str:
        current_code += bit
        if current_code in reverse_huffman_codes:
            decoded_str += reverse_huffman_codes[current_code]
            current_code = ''
        elif len(current_code) > max(len(code) for code in reverse_huffman_codes):
            closest_code = min(
                reverse_huffman_codes.keys(),
                key=lambda code: hamming_distance(current_code, code)
            )
            decoded_str += reverse_huffman_codes[closest_code]
            current_code = ''
    
    return decoded_str

def efficiency(original, decoded):
    correct = sum(el1 == el2 for el1, el2 in zip(original, decoded))
    return f"({(correct / len(original))*100}%"