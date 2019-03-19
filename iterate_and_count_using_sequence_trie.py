# Alternative approach for performance comparison using trie structure specific to this application.

from collections import Counter
import sequence_trie


def iterate_and_count_using_sequence_trie(input_list, min_sequence_length, max_sequence_length) -> Counter:
    my_trie = sequence_trie.Trie(min_sequence_length, max_sequence_length)

    for i in range(len(input_list)):
        my_trie.update(input_list[i])

    return my_trie.sequences
