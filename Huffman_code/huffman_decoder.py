import random

def decode_huffman_with_noise(encoded_str, huffman_codes, noise_prob=0.05):
    reverse_huffman_codes = {code: char for char, code in huffman_codes.items()}
    decoded_str = ''
    current_code = ''
    

    def add_noise(bit):
        return '1' if bit == '0' and random.random() < noise_prob else '0' if bit == '1' and random.random() < noise_prob else bit
    

    for bit in encoded_str:
        bit_with_noise = add_noise(bit)  
        current_code += bit_with_noise  
        
        if current_code in reverse_huffman_codes:
            decoded_str += reverse_huffman_codes[current_code]  
            current_code = ''  
        elif current_code:
            closest_code = min(reverse_huffman_codes.keys(), key=lambda code: hamming_distance(current_code, code))
            decoded_str += reverse_huffman_codes[closest_code]
            current_code = '' 

    return decoded_str

def hamming_distance(str1, str2):
    return sum(el1 != el2 for el1, el2 in zip(str1, str2))

def efficiency(original, decoded):
    correct = sum(o == d for o, d in zip(original, decoded))
    return (correct / len(original))*100