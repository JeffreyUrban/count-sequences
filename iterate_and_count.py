# Naive approach as point of truth and performance benchmark.
# Single dictionary: Iterate through items. Count sequences of all lengths ending at that item.

from collections import Counter


def iterate_and_count(input_list, min_sequence_length, max_sequence_length) -> Counter:
    sequences = Counter()

    for i in range(len(input_list)):
        min_index = max(0, i + 1 - max_sequence_length)
        max_index = min(i + 1 - min_sequence_length, i)
        for j in range(min_index, max_index + 1):
            # Count sequences of each length ending at item j
            sequence = input_list[j:i+1]
            sequences.update([str(sequence)])

    for sequence in sequences.most_common():
        if sequence[1] < 2:
            # Keep only repeated sequences
            del sequences[sequence[0]]

    return sequences
