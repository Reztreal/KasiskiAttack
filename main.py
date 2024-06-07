import math
from functools import reduce
from collections import Counter

english_freq = {
    'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127,
    'F': 0.022, 'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002,
    'K': 0.008, 'L': 0.040, 'M': 0.024, 'N': 0.067, 'O': 0.075,
    'P': 0.019, 'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091,
    'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001, 'Y': 0.020,
    'Z': 0.001
}

def calculate_letter_frequency(segment):
    frequency = {chr(i): 0 for i in range(ord('A'), ord('Z') + 1)}
    for letter in segment:
        if letter in frequency:
            frequency[letter] += 1
    total = len(segment)
    for letter in frequency:
        frequency[letter] /= total
    return frequency

def chi_squared_statistic(observed, expected):
    return sum(((observed[char] - expected[char]) ** 2) / expected[char] for char in observed)

def find_best_shift(segment):
    best_shift = 0
    lowest_chi_squared = float('inf')
    for shift in range(26):
        shifted_segment = ''.join(chr((ord(char) - ord('A') - shift) % 26 + ord('A')) for char in segment)
        frequency = calculate_letter_frequency(shifted_segment)
        chi_squared = chi_squared_statistic(frequency, english_freq)
        if chi_squared < lowest_chi_squared:
            lowest_chi_squared = chi_squared
            best_shift = shift
    return best_shift

def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

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

def index_of_coincidence(text):
    frequency = Counter(text)
    N = len(text)
    return sum(f * (f - 1) for f in frequency.values()) / (N * (N - 1))

def find_best_keyword_length(ciphertext, max_length):
    average_ioc = []
    for length in range(1, max_length + 1):
        segments = split_ciphertext_by_key_length(ciphertext, length)
        ioc_values = [index_of_coincidence(segment) for segment in segments]
        average_ioc.append((length, sum(ioc_values) / len(ioc_values)))
    return max(average_ioc, key=lambda x: x[1])[0]

def decrypt_vigenere(ciphertext):
    ciphertext = ''.join(filter(str.isalpha, ciphertext))  # Remove non-alphabetic characters
    repeats, all_distances = find_repeated_sequences_and_all_distances(ciphertext, 3, 5)
    gcd = gcd_of_all_distances(all_distances)
    key_lengths = find_divisors(gcd)
    best_length = find_best_keyword_length(ciphertext, 20)

    segments = split_ciphertext_by_key_length(ciphertext, best_length)
    key_guess = ''.join(chr(find_best_shift(segment) + ord('A')) for segment in segments)

    decrypted_text = vigenere_decrypt(ciphertext, key_guess)
    return key_guess, decrypted_text


ciphertext = "FIIFLVZOZSVPDCAZVFSLEMRULBQISCXVQTSNDMFTIDGIZILZDMFFLVZYMHCGDIGSLDSHEZSIWMMXPNANTIIRJSFMWBXIDPSEWHAIXYWQMEXVVVDMRUKXASPFOQTUPJLNTQWTJYQOLFOFEOVVWWTURXDIGPTLLMFTINJYFOLKZUFXMVKCZISVAHDQQVEVDMRTWIRMWYJIGPRFOCFUWKZYFUQVGZZUKYLNTMXKZYSDEMWMMXPXSJUZKNAXQQZVJSAZICWNERSILBTUWJHLUFIZFNTQGYMLOTARQJMFLJLISXMUWUZPAVXUUDMVKNTMXUGLGZFPLBQFVZHFQTITSNQEXVSGRDSDLBQBVVKYZOIFXNTQWLFZAXPFOCZSHRJEZQWJDCWQEUJYMYRFOUDQJIGFUORFLUYAYJWMTMPCVCEFYITNTUWYSFXAAUZIGEIZSGEQRKOCFTFIGIYNIWGLQFSJOYQBXYWXGEXSWBUZHKZYPASI"

ciphertext2 = "DAZFISFSPAVQLSNPXYSZWXALCDAFGQUISMTPHZGAMKTTFTCCFXKFCRGGLPFETZMMMZOZDEADWVZWMWKVGQSOHQSVHPWFKLSLEASEPWHMJEGKPURVSXJXVBWVPOSDETEQTXOBZIKWCXLWNUOVJMJCLLOEOFAZENVMJILOWZEKAZEJAQDILSWWESGUGKTZGQZVRMNWTQSEOTKTKPBSTAMQVERMJEGLJQRTLGFJYGSPTZPGTACMOECBXSESCIYGUFPKVILLTWDKSZODFWFWEAAPQTFS"

key, plaintext = decrypt_vigenere(ciphertext)
key2, plaintext2 = decrypt_vigenere(ciphertext2)
print(f"Recovered Key: {key}")
print(f"Decrypted Text: {plaintext}")

print(f"Recovered Key: {key2}")
print(f"Decrypted Text: {plaintext2}")
