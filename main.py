from collections import defaultdict
def find_repeated_substrings(text):
    # Dictionary to store the repeated substrings and their distances
    substrings_dict = {}

    def is_part_of_larger_substring(sub, substrings_dict):
        for key in substrings_dict.keys():
            if sub in key:
                return True
        return False

    for length in range(10, 2, -1):
        current_length_substrings = defaultdict(list)

        for i in range(len(text) - length + 1):
            substring = text[i:i + length]
            current_length_substrings[substring].append(i)

        for substring, positions in current_length_substrings.items():
            if len(positions) > 1:
                if not is_part_of_larger_substring(substring, substrings_dict):
                    distances = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
                    substrings_dict[substring] = distances

    return substrings_dict


def calculate_factors(distances):
    factor_counts = defaultdict(int)

    def find_factors(n):
        factors = set()
        for i in range(2, n):
            if n % i == 0:
                factors.add(i)
                factors.add(n // i)
        return factors

    for dist_list in distances.values():
        for dist in dist_list:
            factors = find_factors(dist)
            for factor in factors:
                factor_counts[factor] += 1

    return dict(factor_counts)


def sort_and_find_largest(factor_counts):
    # Sort the factor counts in descending order by value
    sorted_factor_counts = dict(sorted(factor_counts.items(), key=lambda item: item[1], reverse=True))
    # Find the largest value
    largest_factor = next(iter(sorted_factor_counts.items()))

    return sorted_factor_counts, largest_factor

text = "WQXYMREOBPVWHTHQYEQVEDEXRBGSIZSILGRTAJFZOAMAVVXGRFQGKCPIOZIJBCBLUWYRWSTUGVQPSUDIUWOESFMTBTANCYZTKTYBVFDKDERSIBJECAQDWPDERIEKGPRAQFBGTHQKVVGRAXAVTHARQEELUECGVVBJEBXIJAKNGESWTKBEDXPBQOUDWVTXESMRUWWRPAWKMTITKHFWTDAURRVFESFESTKSHFLZAEONEXZBWTIARWWTTHQYEQVEDEXRBGSOREDMTICM"
substrings = find_repeated_substrings(text)
factor_counts = calculate_factors(substrings)
sorted_factor_counts, largest_factor = sort_and_find_largest(factor_counts)

largest_factor_value = largest_factor[0]

print("Sorted factor counts:", sorted_factor_counts)
print("Largest factor:", largest_factor)
print("Most likely key length:", largest_factor_value)
