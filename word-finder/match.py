from trie import TrieNode, add_to_trie, find_prefix_in_trie


class Position:
    col_id: int
    row_id: int

    def __init__(self, row, col) -> None:
        self.col_id = col
        self.row_id = row


class Match:
    text: str
    start: Position
    end: Position

    def __init__(self, text: str, start: Position, end: Position) -> None:
        self.text = text
        self.start = start
        self.end = end


def find_matches(rows: list[str], words: list[str]) -> list[Match]:
    directions = [
        Position(-1, 1),
        Position(0, 1),
        Position(1, 1),
        Position(1, 0),
        Position(1, -1),
        Position(0, -1),
        Position(-1, -1),
        Position(-1, 0),
    ]

    trie = TrieNode()
    for word in words:
        add_to_trie(word, trie)

    matches: list[Match] = []

    for start_row_id in range(0, len(rows)):
        row = rows[start_row_id]

        for start_col_id in range(0, len(row)):
            for direction in directions:
                row_id = start_row_id
                col_id = start_col_id
                seen = ''

                while 0 <= row_id < len(rows) and 0 <= col_id < len(rows[row_id]):
                    seen += rows[row_id][col_id]
                    result = find_prefix_in_trie(seen, trie)

                    if result is None:
                        break

                    if result.isComplete:
                        matches.append(Match(seen, Position(start_row_id, start_col_id), Position(row_id, col_id)))

                    if not result.hasMore:
                        break

                    row_id += direction.row_id
                    col_id += direction.col_id

    return matches


if __name__ == '__main__':
    puzzle = [
        '      SODABRAB',
        '      BMJANMAR',
        '      EŠRJČSNU',
        '      LELIČOGA',
        '      GDLLŽAOL',
        '      IAUANLLA',
        '      JLAMANAP',
        'KAJIBMAGOOTBGE',
        'ARGENTINASUIEN',
        'ZHAITIAASKBRNK',
        'IENMBKGBJRIAEI',
        'MEOGOTUEATVNSP',
        'BELIZEVLRAILAA',
        'AJIPOITESJAGRR',
        'BMALTAJAANAMOG',
        'VABURABIDNURUB',
        'EIRSKARIAJISUR'
    ]
    words = [
        'ALŽIR', 'ANGOLA', 'ARGENTINA', 'ARUBA', 'BANGLADEŠ', 'BARBADOS', 'BELGIJA', 'BELIZE', 'BENIN', 'BURUNDI',
        'BUTAN',
        'ČAD'
    ]

    matches = find_matches(puzzle, words)
    print('matching done :)')
