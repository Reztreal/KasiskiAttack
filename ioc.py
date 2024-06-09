from collections import Counter, defaultdict

def index_of_coincidence(text):
    cleaned_text = ''.join(filter(str.isalpha, text)).upper()
    frequency = Counter(cleaned_text)
    N = len(cleaned_text)
    ic = sum(f * (f - 1) for f in frequency.values()) / (N * (N - 1)) if N > 1 else 0
    return ic

def divide_into_cosets(text, length):
    cosets = [''] * length
    for i in range(len(text)):
        cosets[i % length] += text[i]
    return cosets

def keyword_length_estimation(text, max_length=10, english_ic=0.068):
    cleaned_text = ''.join(filter(str.isalpha, text)).upper()
    best_length = 1
    smallest_diff = float('inf')
    results = []

    for length in range(1, max_length + 1):
        cosets = divide_into_cosets(cleaned_text, length)
        ics = [index_of_coincidence(coset) for coset in cosets]
        average_ic = sum(ics) / len(ics)
        diff = abs(average_ic - english_ic)
        results.append((length, ics, average_ic, diff))

        if diff < smallest_diff:
            smallest_diff = diff
            best_length = length

    return best_length, results

# Example usage
text = "WQXYMREOBPVWHTHQYEQVEDEXRBGSIZSILGRTAJFZOAMAVVXGRFQGKCPIOZIJBCBLUWYRWSTUGVQPSUDIUWOESFMTBTANCYZTKTYBVFDKDERSIBJECAQDWPDERIEKGPRAQFBGTHQKVVGRAXAVTHARQEELUECGVVBJEBXIJAKNGESWTKBEDXPBQOUDWVTXESMRUWWRPAWKMTITKHFWTDAURRVFESFESTKSHFLZAEONEXZBWTIARWWTTHQYEQVEDEXRBGSOREDMTICM"
best_length, results = keyword_length_estimation(text, max_length=10)

print(f"Best keyword length: {best_length}")
print("Detailed results:")
for length, ics, average_ic, diff in results:
    print(f"Length: {length}, ICs: {ics}, Average IC: {average_ic}, Difference from English IC: {diff}")
