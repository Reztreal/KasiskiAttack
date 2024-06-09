import string
from collections import Counter

# Frequency of letters in English text
english_frequencies = {
    'A': 0.082, 'B': 0.014, 'C': 0.028, 'D': 0.038, 'E': 0.131, 'F': 0.029, 'G': 0.020,
    'H': 0.053, 'I': 0.064, 'J': 0.001, 'K': 0.004, 'L': 0.034, 'M': 0.025, 'N': 0.071,
    'O': 0.080, 'P': 0.020, 'Q': 0.001, 'R': 0.068, 'S': 0.061, 'T': 0.105, 'U': 0.025,
    'V': 0.009, 'W': 0.015, 'X': 0.002, 'Y': 0.020, 'Z': 0.001
}


# Calculate the chi-squared value for a given shift
def calculate_chi_squared(text, shift):
    shifted_text = ''.join(chr((ord(c) - shift - 65) % 26 + 65) for c in text)
    observed_frequencies = Counter(shifted_text)
    total = sum(observed_frequencies.values())

    # Calculate the chi-squared value for each letter
    # chi-squared = sum((observed - expected)^2 / expected)
    # observed is the frequency of the letter in the text
    # expected is the frequency of the letter in English text
    # sum is over all letters in the alphabet
    # chi-squared value closer to 0 indicates a better match
    chi_squared = 0.0
    for letter in string.ascii_uppercase:
        observed = observed_frequencies[letter] / total if total > 0 else 0
        expected = english_frequencies[letter]
        chi_squared += (observed - expected) ** 2 / expected

    return chi_squared


def divide_into_cosets(text, length):
    cosets = [''] * length
    for i in range(len(text)):
        cosets[i % length] += text[i]
    return cosets


def recover_keyword(text, length):
    cleaned_text = ''.join(filter(str.isalpha, text)).upper()
    cosets = divide_into_cosets(cleaned_text, length)

    keyword = ''
    coset_info = []

    # Iterate over the cosets and find the best shift for each coset
    # Calculate the chi-squared value for each shift
    # Choose the shift with the smallest chi-squared value
    # Convert the shift to the corresponding letter and append to the keyword
    # Store the detailed information for each coset
    for coset_index, coset in enumerate(cosets):
        min_chi_squared = float('inf')
        best_shift = 0
        chi_squared_values = []

        # Iterate over the possible shifts
        # Calculate the chi-squared value for each shift
        # Keep track of the shift with the smallest chi-squared value
        for shift in range(26):
            chi_squared = calculate_chi_squared(coset, shift)
            chi_squared_values.append((shift, chi_squared))
            if chi_squared < min_chi_squared:
                min_chi_squared = chi_squared
                best_shift = shift

        keyword_letter = chr(best_shift + 65)
        keyword += keyword_letter
        coset_info.append((coset_index + 1, keyword_letter, best_shift, chi_squared_values))

    return keyword, coset_info


def display_coset_info(coset_info):
    for coset_index, keyword_letter, best_shift, chi_squared_values in coset_info:
        print(f"Coset {coset_index}:")
        print(f"  Recovered letter: {keyword_letter}")
        print(f"  Best shift: {best_shift}")
        print(f"  Chi-squared values for each shift:")
        for shift, chi_squared in chi_squared_values:
            print(f"    Shift {shift} ({chr(shift + 65)}): {chi_squared:.4f}")


text = "WQXYMREOBPVWHTHQYEQVEDEXRBGSIZSILGRTAJFZOAMAVVXGRFQGKCPIOZIJBCBLUWYRWSTUGVQPSUDIUWOESFMTBTANCYZTKTYBVFDKDERSIBJECAQDWPDERIEKGPRAQFBGTHQKVVGRAXAVTHARQEELUECGVVBJEBXIJAKNGESWTKBEDXPBQOUDWVTXESMRUWWRPAWKMTITKHFWTDAURRVFESFESTKSHFLZAEONEXZBWTIARWWTTHQYEQVEDEXRBGSOREDMTICM"
length = 7
keyword, coset_info = recover_keyword(text, length)

print(f"Recovered keyword: {keyword}")
print("Detailed coset information:")
display_coset_info(coset_info)
