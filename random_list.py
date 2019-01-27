import random


def random_list(count, length) -> []:
    the_list = []
    for _ in range(length):
        the_list.append(str(random.choice(range(count))))
    return the_list
