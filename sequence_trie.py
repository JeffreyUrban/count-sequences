from collections import Counter
import json

# TODO: Index all active nodes within deque (or move to other structure), so updating is faster.

"""
Sequence Trie:

Like a linked list, except each node links to a dictionary (count collection)

Each node stores a count of sequences of strings that reached that node

Maximum depth is specifiable

The tree tracks the present nodes of sequences passing through it

The tree accepts a symbol update and
advances the present node for all of its sequences, and the count for that node
adds a sequence at root, if the symbol matches the root symbol

On request, the tree outputs a list of all sequences of a minimum length or greater, with their counts. 
This is determined by taking the count at each node at depth equal to the minimum length or greater, 
and tracing back to the root.

Does not support:
Deletion of nodes

Consider later:
Adding aging factor for counts, to support sliding window
Handle timestamp offsets somehow to decouple potentially overlapping sequences
Fuzzy matching among sequences that may include different extra intermediate symbols
"""


class Node:
    def __init__(self, trie, symbol, remaining_depth, parent):
        self.trie = trie
        self.symbol = symbol
        self.remaining_depth = remaining_depth
        self.parent = parent
        #
        self.count = 1
        self.children = {}
        self.sequence = []
        if parent and parent.symbol is not None:
            self.sequence = parent.sequence.copy()
        self.sequence.append(symbol)

    def increment(self):
        self.count = self.count + 1
        self.trie.next_active_children_by_level[self.remaining_depth].add(self)

    def update(self, symbol):
        # Add or update child with symbol, if depth not exceeded
        if self.remaining_depth:
            if symbol not in self.children:
                self.children[symbol] = \
                    Node(trie=self.trie, symbol=symbol, remaining_depth=self.remaining_depth - 1, parent=self)
                self.trie.all_child_nodes.add(self.children[symbol])
                self.trie.next_active_children_by_level[self.remaining_depth - 1].add(self.children[symbol])
            else:
                self.children[symbol].increment()

    def structure(self):
        return {'Node': {
            'symbol': self.symbol,
            'count': self.count,
            'remaining_depth': self.remaining_depth,
            'children': [self.children[symbol].structure() for symbol in self.children.keys()]
        }}

    def __str__(self):
        return json.dumps(self.structure(), indent=4)


class Trie:
    def __init__(self, min_length, max_length):
        self.min_length = min_length
        self.max_length = max_length
        #
        self.root = Node(trie=self, symbol=None, remaining_depth=max_length, parent=None)
        # active children are grouped by level for update to flow from leaves to root
        self.present_active_children_by_level = [set() for _ in range(max_length)]
        self.next_active_children_by_level = [set() for _ in range(max_length)]
        self.all_child_nodes = set()

    def update(self, symbol):
        # Advance all active nodes with this symbol
        # Update flows up trie (children before parents)
        self.next_active_children_by_level = [set() for _ in range(self.max_length)]
        for level in self.present_active_children_by_level:
            for node in level:
                node.update(symbol)
        self.root.update(symbol)
        for level in range(self.max_length):
            self.present_active_children_by_level[level] = self.next_active_children_by_level[level]

    @property
    def sequences(self) -> Counter:
        sequences = Counter()
        for node in self.all_child_nodes:
            if node.count > 1 and node.remaining_depth < self.max_length - self.min_length + 1:  # At least min_length
                sequences[str(node.sequence)] = node.count
        return sequences

    def __str__(self):
        trie_string = "Trie: min_length: {}, max_length: {} \n{}"\
            .format(self.min_length, self.max_length, self.root)

        return trie_string


if __name__ == '__main__':
    my_trie = Trie(2, 4)
    my_trie.update('0')
    my_trie.update('0')
    my_trie.update('0')
    my_trie.update('0')
    print(my_trie)
    print(my_trie.sequences)

# Expected Result:
# ['0', '0', '0']: count: 2, remaining_depth: 1
# ['0']: count: 4, remaining_depth: 3
# ['0', '0', '0', '0']: count: 1, remaining_depth: 0
# ['0', '0']: count: 3, remaining_depth: 2
# Counter({"['0', '0']": 3, "['0', '0', '0']": 2})
