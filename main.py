import math
from functools import reduce

def find_repeated_sequences_and_all_distances(text, min_length, max_length):
    repeated_sequences = {}
    all_distances = []
    for length in range(min_length, max_length + 1):
        sequences = {}
        for i in range(len(text) - length + 1):
            seq = text[i:i + length]
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]
        for seq, positions in sequences.items():
            if len(positions) > 1:
                for j in range(len(positions)):
                    for k in range(j + 1, len(positions)):
                        distance = positions[k] - positions[j]
                        all_distances.append(distance)
        repeated_sequences[length] = {seq: pos for seq, pos in sequences.items() if len(pos) > 1}

    return repeated_sequences, all_distances

def gcd_of_all_distances(distances):
    return reduce(math.gcd, distances)

def find_divisors(n):
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors)

def split_ciphertext_by_key_length(ciphertext, key_length):
    segments = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        segments[i % key_length] += char
    return segments

cipher_text = "PPQCAXQVEKGYBNKMAZUYBNGBALJONITSZMJYIMVRAGVOHTVRAUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOU"
repeats, all_distances = find_repeated_sequences_and_all_distances(cipher_text, 3, 5)
print("Repeated Sequences:", repeats)

gcd = gcd_of_all_distances(all_distances)
print("GCD of all distances:", gcd)

key_lengths = find_divisors(gcd)

for i in key_lengths:
    segments = split_ciphertext_by_key_length(cipher_text, i)
    print(f"Key Length {i}:")
    key_guess = ''
    for index, segment in enumerate(segments):
        print(f"  Segment {index + 1}: {segment}")
