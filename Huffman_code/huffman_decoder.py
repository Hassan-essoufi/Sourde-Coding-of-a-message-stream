import random

def decode_huffman_with_noise(encoded_str, huffman_codes, noise_prob=0.05):
    # Invert the Huffman codes to get a reverse mapping (code -> character)
    reverse_huffman_codes = {code: char for char, code in huffman_codes.items()}

    # Initialize variables
    decoded_str = ''
    current_code = ''
    
    # Simulate Gaussian noise by flipping bits with a certain probability (noise_prob)
    def add_noise(bit):
        return '1' if bit == '0' and random.random() < noise_prob else '0' if bit == '1' and random.random() < noise_prob else bit
    
    # Go through the encoded string and match codes to characters
    for bit in encoded_str:
        bit_with_noise = add_noise(bit)  # Add noise to the bit
        current_code += bit_with_noise  # Append the noisy bit
        
        # Try to decode if the current code matches a Huffman code
        if current_code in reverse_huffman_codes:
            decoded_str += reverse_huffman_codes[current_code]  # Add the decoded character
            current_code = ''  # Reset the current code to start looking for the next code

        # If no match, try to find the closest code (using Hamming distance)
        elif current_code:
            # Find the closest match by comparing with all Huffman codes using Hamming distance
            closest_code = min(reverse_huffman_codes.keys(), key=lambda code: hamming_distance(current_code, code))
            decoded_str += reverse_huffman_codes[closest_code]
            current_code = ''  # Reset the current code

    return decoded_str

def hamming_distance(str1, str2):
    # Calculate the Hamming distance between two strings of equal length
    return sum(el1 != el2 for el1, el2 in zip(str1, str2))

# Example Huffman codes (assumed from previous encoding)
huffman_codes = {
    'a': '0',
    'b': '10',
    'c': '11',
    'd': '011'
}

# Example encoded string with noise added (e.g., '0111010110' with some bit errors)
encoded_str = '0111011110'  # This is a noisy version of 'dcb'

# Decode the encoded string with noise
decoded_str = decode_huffman_with_noise(encoded_str, huffman_codes, noise_prob=0.1)

# Display the decoded string
print("Decoded string with noise:", decoded_str)
