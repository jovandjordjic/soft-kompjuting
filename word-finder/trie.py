from __future__ import annotations


class MatchResult:
    isComplete: bool
    hasMore: bool

    def __str__(self) -> str:
        return f'isComplete: {self.isComplete}, hasMore: {self.hasMore}'


class TrieNode:
    isTerminal: bool = False
    children: dict[str, TrieNode] = {}

    def __init__(self) -> None:
        self.isTerminal = False
        self.children = {}


def add_to_trie(word: str, node: TrieNode):
    if len(word) == 0:
        node.isTerminal = True
        return

    prefix: str = word[0]

    if len(word) > 1 and (prefix == 'D' or prefix == 'N' or prefix == 'L'):
        if word[1] == 'j' or word[1] == 'ž':
            prefix += word[1]

    child: TrieNode = get_or_add(prefix, node)

    add_to_trie(word[1:], child)


def get_or_add(prefix: str, node: TrieNode):
    new_node: TrieNode = node.children.get(prefix)
    if new_node is None:
        new_node = TrieNode()
        node.children[prefix] = new_node

    return new_node


def find_prefix_in_trie(word: str, node: TrieNode):
    if len(word) == 0:
        match_result: MatchResult = MatchResult()
        match_result.isComplete = node.isTerminal
        match_result.hasMore = len(node.children) > 0

        return match_result

    prefix = word[0]

    if len(word) > 1 and (prefix == 'D' or prefix == 'N' or prefix == 'L'):
        if word[1] == 'j' or word[1] == 'ž':
            prefix += word[1]

    child: TrieNode = node.children.get(prefix)
    if child is None:
        return None

    return find_prefix_in_trie(word[1:], child)
