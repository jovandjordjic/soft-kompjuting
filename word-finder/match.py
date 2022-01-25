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


def find_matches(rows: list[list[str]], words: list[str]) -> list[Match]:
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


def split(word):
    return [char for char in word]


if __name__ == '__main__':
    puzzle = [['D', 'O', 'M', 'B', 'A', 'S', 'D', 'P', 'R', 'A', 'V', 'D', 'A'],
              ['R', 'A', 'T', 'U', 'L', 'O', 'P', 'A', 'R', 'E', 'E', 'R', 'Z'],
              ['O', 'S', 'K', 'A', 'R', 'L', 'E', 'T', 'R', 'I', 'V', 'A', 'N'],
              ['K', 'O', 'M', 'U', 'N', 'I', 'Z', 'A', 'M', 'I', 'L', 'K', 'A'],
              ['N', 'A', 'Č', 'N', 'E', 'S', 'N', 'K', 'N', 'O', 'S', 'O', 'S'],
              ['O', 'A', 'Š', 'N', 'M', 'T', 'V', 'A', 'R', 'J', 'N', 'N', 'G'],
              ['K', 'Č', 'K', 'O', 'E', 'A', 'N', 'P', 'A', 'T', 'R', 'C', 'Z'],
              ['A', 'A', 'N', 'I', 'R', 'A', 'J', 'R', 'J', 'M', 'O', 'E', 'A'],
              ['U', 'T', 'R', 'T', 'T', 'T', 'A', 'I', 'A', 'A', 'T', 'P', 'S'],
              ['T', 'E', 'E', 'A', 'S', 'S', 'T', 'C', 'C', 'K', 'K', 'T', 'T'],
              ['R', 'P', 'L', 'K', 'O', 'S', 'A', 'I', 'I', 'A', 'I', 'A', 'A'],
              ['A', 'P', 'R', 'L', 'I', 'N', 'B', 'M', 'L', 'S', 'V', 'J', 'R'],
              ['V', 'A', 'E', 'E', 'A', 'R', 'I', 'I', 'A', 'A', 'I', 'E', 'A'],
              ['A', 'R', 'T', 'R', 'V', 'G', 'K', 'K', 'G', 'B', 'G', 'M', 'L'],
              ['R', 'A', 'V', 'I', 'Z', 'O', 'P', 'V', 'A', 'A', 'A', 'A', 'C'],
              ['A', 'J', 'P', 'K', 'K', 'L', 'D', 'R', 'N', 'A', 'G', 'R', 'I'],
              ['D', 'L', 'A', 'P', 'R', 'I', 'A', 'N', 'O', 'R', 'A', 'K', 'N'],
              ['I', 'I', 'K', 'R', 'R', 'P', 'N', 'O', 'E', 'T', 'A', 'A', 'K'],
              ['N', 'J', 'A', 'A', 'A', 'E', 'A', 'T', 'A', 'K', 'D', 'M', 'A'],
              ['D', 'A', 'R', 'K', 'S', 'L', 'K', 'N', 'V', 'E', 'N', 'A', 'T'],
              ['I', 'T', 'D', 'T', 'R', 'I', 'D', 'O', 'P', 'L', 'A', 'T', 'A'],
              ['J', 'K', 'O', 'I', 'S', 'O', 'S', 'B', 'R', 'E', 'M', 'U', 'B'],
              ['K', 'R', 'Š', 'K', 'R', 'I', 'Z', 'M', 'A', 'J', 'O', 'R', 'E'],
              ['A', 'S', 'T', 'A', 'L', 'A', 'K', 'A', 'T', 'O', 'K', 'A', 'D']
              ]

    words = [
        'ANATAL',
        'ANDORA',
        'ARABIJA',
        'ARVINA',
        'ASTAL',
        'ATEISTI',
        'BATAK',
        'BONTON',
        'CINKAT',
        'DAKOTA',
        'DANAK',
        'DEBATA',
        'DIRAR',
        'DOMBAS',
        'DOPLATA',
        'DORUČAK',
        'DRAKON',
        'ELEKTRA',
        'EPILOG',
        'GALICA',
        'GIVIKT',
        'IKAKVO',
        'INDIJKA',
        'JARINA',
        'JELEK',
        'KALIKO',
        'KAPARA',
        'KAPRIC',
        'KARDOŠ',
        'KARONA',
        'KASABA',
        'KATION',
        'KENDO',
        'KLERIK',
        'KLIMA',
        'KNOSOS',
        'KOKILA',
        'KOMANDA',
        'KOMUNIZAM',
        'KONCERT',
        'KONKORD',
        'KRIKET',
        'KRIZMA',
        'KRPAN',
        'KVART',
        'LAGANO',
        'LAKAT',
        'LEPILO',
        'LEVACIJA',
        'LISOVKA',
        'LOPARE',
        'MACAN',
        'MAJICA',
        'MAJOR',
        'MAKRAME',
        'MASTIKA',
        'MATURA',
        'MILKA',
        'MISICA',
        'MONCA',
        'MURINA',
        'NADIRA',
        'NAKIT',
        'NESTOR',
        'NIKITA',
        'NOKAUT',
        'OSKAR',
        'PAKARD',
        'PARAJLIJA',
        'PATAK',
        'PETAČA',
        'PETRA',
        'PLATA',
        'PLATAN',
        'POLUTAR',
        'POTRK',
        'POZIVAR',
        'PRAKTIKA',
        'PRAVDA',
        'PREKOR',
        'PREVOD',
        'PRILOG',
        'PROLAZ',
        'RAJAC',
        'RAMEJA',
        'RAONIK',
        'RATAN',
        'REGAN',
        'SAKLA',
        'SARAJ',
        'SENČA',
        'SIKTER',
        'SISAK',
        'SKARLET',
        'SKRAD',
        'SKVER',
        'SLAMA',
        'SOLER',
        'SOLISTA',
        'SRKTAJ',
        'STALAK',
        'STISAK',
        'STORA',
        'STREMEN',
        'TANEV',
        'TERGAL',
        'TRAVARA',
        'TRIDO',
        'TRIVAN',
        'TROŠAK',
        'VARADIN',
        'VERAN',
        'VIKTOR',
        'VRANAC',
        'VRBICA',
        'ZASTARA',
        'ZORKA'
    ]

    words2 = ['BODLjIKA', 'BOKELj', 'BOLjKA', 'BULjUBAŠA', 'BUTELjA', 'ČAKLjA', 'ČEŠLjAONICA', 'ČKALjA', 'DALjINA',
              'DIVLjAK', 'KRALjICA', 'KRPLjAČE', 'LjERKA', 'LjETON', 'LjILjAK', 'LjILjANA', 'LjOKAČ', 'LjUBELj',
              'LjUBINjE', 'LjUBIŠA', 'LjUBLjANČANIN', 'LjUBLjANČANKA', 'LjUBLjENICA', 'LjUTINA', 'LjUBOMORNOST',
              'MELjAK', 'LjULjAŠKA', 'NAVILjAK', 'LjUPČAC', 'ODOLjEN', 'LjUSKICA', 'PAHULjA', 'LjUSPA', 'PIŠTOLj',
              'LjUŠTURA', 'PIŠTALjKA', 'STELjINA', 'ŠKALjAK', 'RALjE', 'SATLjIK', 'SELjANKA', 'SEVILjA', 'SNOPLjE',
              'SRLjANjE', 'ŠTIPALjKA', 'TULjAN', 'ULjANIK', 'UPALjAČ', 'VALjEVO', 'ŽABLjAK']

    puzzle2 = [
        ['Lj', 'U', 'Lj', 'A', 'Š', 'K', 'A', 'N', 'A', 'Lj', 'I', 'Lj'],
        ['Lj', 'U', 'Š', 'T', 'U', 'R', 'A', 'Lj', 'E', 'Lj', 'O', 'U'],
        ['U', 'U', 'B', 'T', 'Š', 'A', 'N', 'U', 'Lj', 'K', 'Ž', 'S'],
        ['B', 'O', 'D', 'Lj', 'I', 'K', 'A', 'P', 'A', 'O', 'A', 'P'],
        ['O', 'U', 'K', 'O', 'A', 'P', 'A', 'Č', 'Lj', 'V', 'B', 'A'],
        ['M', 'N', 'Lj', 'D', 'Lj', 'N', 'A', 'Lj', 'P', 'I', 'Lj', 'H'],
        ['O', 'A', 'G', 'U', 'I', 'A', 'Č', 'Lj', 'A', 'Lj', 'A', 'U'],
        ['R', 'Lj', 'R', 'Lj', 'B', 'V', 'N', 'A', 'K', 'K', 'K', 'Lj'],
        ['N', 'U', 'E', 'A', 'U', 'A', 'Lj', 'K', 'N', 'A', 'Č', 'A'],
        ['O', 'T', 'D', 'T', 'N', 'P', 'Š', 'A', 'A', 'I', 'S', 'N'],
        ['S', 'I', 'E', 'I', 'O', 'Lj', 'Č', 'A', 'K', 'Č', 'N', 'I'],
        ['T', 'N', 'Lj', 'N', 'O', 'N', 'I', 'A', 'A', 'Lj', 'O', 'K'],
        ['S', 'A', 'O', 'T', 'A', 'E', 'K', 'Lj', 'C', 'U', 'P', 'R'],
        ['D', 'K', 'Š', 'Lj', 'Nj', 'R', 'A', 'O', 'A', 'S', 'Lj', 'P'],
        ['Lj', 'I', 'B', 'I', 'E', 'P', 'M', 'K', 'V', 'K', 'E', 'Lj'],
        ['P', 'U', 'B', 'Lj', 'U', 'B', 'Lj', 'E', 'N', 'I', 'C', 'A'],
        ['Lj', 'U', 'B', 'I', 'Š', 'A', 'S', 'Lj', 'Lj', 'C', 'Lj', 'Č'],
        ['Lj', 'T', 'Lj', 'E', 'T', 'R', 'E', 'O', 'E', 'A', 'E', 'E'],
        ['S', 'K', 'R', 'A', 'Lj', 'E', 'V', 'O', 'V', 'K', 'K', 'D'],
        ['E', 'I', 'V', 'A', 'N', 'E', 'I', 'D', 'S', 'R', 'O', 'O'],
        ['Lj', 'H', 'Nj', 'Č', 'Lj', 'K', 'Lj', 'O', 'A', 'A', 'T', 'B'],
        ['A', 'E', 'Č', 'A', 'K', 'Lj', 'A', 'Lj', 'T', 'Lj', 'R', 'R'],
        ['N', 'A', 'V', 'I', 'Lj', 'A', 'K', 'E', 'Lj', 'I', 'Lj', 'Lj'],
        ['K', 'Č', 'E', 'Š', 'Lj', 'A', 'O', 'N', 'I', 'C', 'A', 'I'],
        ['A', 'Lj', 'E', 'T', 'U', 'B', 'O', 'Lj', 'K', 'A', 'N', 'N'],
    ]

matches = find_matches(puzzle2, words2)

text_matches = []
for match in matches:
    text_matches.append(match.text)

text_matches.sort()

print('matching done :)')
