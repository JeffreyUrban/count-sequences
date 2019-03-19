import pytest

from random_list import random_list
from iterate_and_count import iterate_and_count
from iterate_and_count_using_sequence_trie import iterate_and_count_using_sequence_trie


def test_output_is_consistent():
    unique_count = 3
    list_length = 6

    input_list = random_list(count=unique_count, length=list_length)
    print("Input list: " + str(input_list))

    sequences1 = iterate_and_count(input_list=input_list, min_sequence_length=2, max_sequence_length=list_length)
    print(sequences1)
    sequences2 = iterate_and_count_using_sequence_trie(input_list=input_list, min_sequence_length=2, max_sequence_length=list_length)
    print(sequences2)
    assert sequences1 == sequences2
