import json
from difflib import SequenceMatcher

from match import Match, find_matches


def get_similarity(string_a, string_b):
    return SequenceMatcher(None, string_a, string_b).ratio()


def check_matches(matches: list[Match], expected_word_list: list[str]):
    correct_matches_count = 0

    num_of_words = len(matches) if (len(matches) <= len(expected_word_list)) else len(expected_word_list)

    for match_id in range(num_of_words):
        match_word = matches[match_id].text

        if match_word in expected_word_list:
            correct_matches_count += 1

    return correct_matches_count / len(expected_word_list)


def check_cells(detected_rows: list[str], expected_rows: list[str]):
    correct_rows_count = 0

    num_of_rows = len(detected_rows) if (len(detected_rows) <= len(expected_rows)) else len(expected_rows)

    for row_id in range(0, num_of_rows):
        stripped_row = detected_rows[row_id].strip()
        correct_rows_count += get_similarity(stripped_row, expected_rows[row_id])

    return correct_rows_count / len(expected_rows)


def check_words(detected_words: list[str], expected_words: list[str]):
    correct_word_count = 0

    stripped_expected_words = [word.strip() for word in expected_words]

    for word in detected_words:
        if word in stripped_expected_words:
            correct_word_count += 1

    return correct_word_count / len(expected_words)


def check_all():
    words2 = ['ABAKAN', 'AMGA', 'AMGUN', 'AMIL', 'AMUR', 'ANABAR', 'ARGUN', 'AVAČA', 'DON', 'GRANIČNAJA', 'IŽMA',
              'IŽORA', 'MDA', 'OSTJOR', 'JANA', 'MOKŠA', '~', 'PES', 'KAT', 'MŠAGA', '„POLA', 'KAVA', 'MZIMTA',
              ' „SIŠKA', 'KEM', 'NARVA', '~', 'SIT', 'KIBA', 'NEVA', 'SJAS', 'KIRVA', 'NIŠČA', 'SOZ', 'KUD', 'OB',
              'SOŽ', 'LENA', 'OKA', 'STARICA', 'LUGA', 'OSKUJA', ' SVIR', 'MALA', 'BEREZINA.', 'OSMA', 'VAGA',
              'VALDAJKA', 'VAŽINKA', 'VELESA', 'VELIKA', 'VIŠERA', 'VIHRA', 'VJATKA', 'VOLGA', 'VOLOŽBA', 'VOP',
              'VORJA', 'VOROŽBA']

    puzzle2 = ['      LENAANAJ', '      IŽMANMGI', '      DSVSITLŽ', '      OEALZVOO', '      NPTAESVR',
               '      UVMLRNOA', '      GUIVEARJ', 'BZPPOVRKZJBROR', 'VOLOŽBADMAAVŽO', 'VSULSVNLUTLABV',
               'ATGAI|IADKAŽAE', 'GJAŠŠLČKKAMICL', 'AOEČKTNIEAJNIE', 'GRANABARMGBKRS', 'ABIKMVJVIHRAAA',
               'ŠONUGMAAGVKJTR', 'MOKŠAJUKSOSASD']

    matches = find_matches(puzzle2, words2)

    json_path = '010_rr.json'
    json_file = open(json_path)
    expected_data = json.load(json_file)
    json_file.close()

    percent_cells = check_cells(puzzle2, expected_data['cell_data'])
    percent_words = check_words(words2, expected_data['words'])
    percent_matches = check_matches(matches, expected_data['words'])
    print('breakpoint')


if __name__ == '__main__':
    check_all()
