import json
import os

import pdf2image
import requests
import xmltodict
from bs4 import BeautifulSoup

DPI = 300
OUTPUT_FOLDER = None
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'jpg'
THREAD_COUNT = 2
USERPWD = None
USE_CROPBOX = False
STRICT = False


class Coordinates:
    row_id: int
    col_id: int

    def __init__(self, row_id, col_id) -> None:
        self.row_id = row_id
        self.col_id = col_id


class WordCoordinatePair:
    def __init(self, **kwargs):
        if 'startCoordinate' in kwargs:
            self.startCoordinate = kwargs['startCoordinate']
        if 'endCoordinate' in kwargs:
            self.endCoordinate = kwargs['endCoordinate']

    startCoordinate: int
    endCoordinate: int


class CrosswordCellArrow:
    locationFrom: str
    locationTo: str


class CrosswordCell:
    solution: str
    x: int
    y: int


class Word:
    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'startCoordinates' in kwargs:
            self.start = kwargs['startCoordinates']
        if 'endCoordinates' in kwargs:
            self.end = kwargs['endCoordinates']
        if 'text' in kwargs:
            self.text = kwargs['text']

    id: str

    start: Coordinates
    end: Coordinates

    text: str


class CrosswordBaseData:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'pdfUrl' in kwargs:
            self.pdfUrl = kwargs['pdfUrl']
        if 'crosswordUrl' in kwargs:
            self.crosswordUrl = kwargs['crosswordUrl']

    name: str
    pdfUrl: str
    crosswordUrl: str


class Crossword(CrosswordBaseData):
    def __init__(self, crossword_base_data: CrosswordBaseData):
        super().__init__(name=crossword_base_data.name, pdfUrl=crossword_base_data.pdfUrl,
                         crosswordUrl=crossword_base_data.crosswordUrl)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    words: list[str]  # todo: switch back to Word
    width: int
    height: int

    cell_data: list[str]

def helper_get_word_from_coordinates(x: WordCoordinatePair, y: WordCoordinatePair,
                                     cell_data: dict[int, dict[int, CrosswordCell]]) -> str:
    word: str = ''

    if x.startCoordinate == x.endCoordinate:
        row = cell_data[x.startCoordinate]
        for y_coordinate in range(y.startCoordinate, y.endCoordinate + 1):
            word += row[y_coordinate].solution
    else:
        for x_coordinate in range(x.startCoordinate, x.endCoordinate + 1):
            word += cell_data[x_coordinate][y.startCoordinate].solution

    return word


def helper_parse_xml_coordinates(coordinates: str) -> WordCoordinatePair:
    split_coordinates_list = coordinates.split('-')
    start_coordinate = int(split_coordinates_list[0]) - 1
    end_coordinate = start_coordinate

    if len(split_coordinates_list) == 2:
        end_coordinate = int(split_coordinates_list[1]) - 1

    word_coordinate_pair = WordCoordinatePair()
    word_coordinate_pair.startCoordinate = start_coordinate
    word_coordinate_pair.endCoordinate = end_coordinate

    return word_coordinate_pair


def helper_convert_xml_cell_data_to_special_dict(xml_cell_data: list) -> list[str]:
    special_dict: dict[int, dict[int, str]] = {}

    return_list: list[str] = []

    for cell_dict in xml_cell_data:
        if '@solution' in cell_dict:
            cell: CrosswordCell = CrosswordCell()
            x: int = int(cell_dict['@y'])
            y: int = int(cell_dict['@x'])

            cell.x = x
            cell.y = y

            cell.solution = cell_dict['@solution']

            if x not in special_dict:
                special_dict[x] = {}

            special_dict[x][y] = cell_dict['@solution']
            # special_dict[x][y] = cell

    sorted_by_x_dict = {key: val for key, val in sorted(special_dict.items(), key=lambda ele: ele[0])}

    for key in sorted_by_x_dict:
        y_dict = sorted_by_x_dict[key]
        sorted_by_y_dict = {key: val for key, val in sorted(y_dict.items(), key=lambda ele: ele[0])}

        return_string = ''

        for letter in sorted_by_y_dict.values():
            return_string += letter

        return_list.append(return_string)

    return return_list


def combine_xml_data_and_crossword_base_data_into_crossword(xml_data,
                                                            crossword_base_data: CrosswordBaseData) -> Crossword:
    crossword: Crossword = Crossword(crossword_base_data)

    crossword_puzzle_dict = xml_data['crossword-compiler-applet']['rectangular-puzzle']['word-search']
    grid_data: dict = crossword_puzzle_dict['grid']
    words_data: list = crossword_puzzle_dict['word']

    crossword.cell_data = helper_convert_xml_cell_data_to_special_dict(grid_data['cell'])

    crossword.height = int(grid_data['@height'])
    crossword.width = int(grid_data['@width'])

    words: list[Word] = []
    string_words: list[str] = []

    for word_dict in words_data:
        id = word_dict['@id']
        x = helper_parse_xml_coordinates(word_dict['@x'])
        y = helper_parse_xml_coordinates(word_dict['@y'])
        solution = word_dict['@solution']

        startCoordinates = Coordinates(y.startCoordinate, x.startCoordinate)
        endCoordinates = Coordinates(y.endCoordinate, x.endCoordinate)

        # word_text = helper_get_word_from_coordinates(x, y, cell_contents)

        word = Word(text=solution, id=id, startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        words.append(word)
        string_words.append(solution)

    crossword.words = string_words

    return crossword


def get_xml_dict_from_url(url: str) -> dict[str, str]:
    url_without_http = url.removeprefix('http://')
    url_split = url_without_http.split('/')
    response = requests.get(f'http://{url_split[0]}/puzzles/{url_split[1]}/{url_split[2]}/{url_split[2]}.xml')

    if response.status_code != 200:
        response.raise_for_status()

    return xmltodict.parse(response.content)


def generate_crossword_name_from_url(url: str) -> str:
    url_split = url.split('/')
    return url_split[-1]


def get_crosswords_from_website_page(page_num: int) -> list[CrosswordBaseData]:
    url = f'https://www.enigmatika.rs/ukrstenice/osmosmerke/page/{page_num}/'

    response = requests.get(url)

    if response.status_code != 200:
        response.raise_for_status()

    data = response.text
    soup = BeautifulSoup(data)

    crosswords: list[CrosswordBaseData] = []

    for span in soup.find_all('span', {'class': 'nxowoo-box'}):
        crossword_data = CrosswordBaseData()

        for tag in span.find_all('a'):

            href = tag.get('href')
            if 'crossword.info' in href:
                crossword_data.crosswordUrl = href
                crossword_data.name = generate_crossword_name_from_url(href)
            elif 'pdf' in href:
                crossword_data.pdfUrl = href

        if crossword_data:
            crosswords.append(crossword_data)

    return crosswords


def get_crosswords():
    shared_save_location = './downloaded_data'

    if not os.path.exists(shared_save_location):
        os.mkdir(shared_save_location)

    for i in range(20, 21):
        try:
            crossword_base_data_objects: list[CrosswordBaseData] = get_crosswords_from_website_page(i)
        except:
            print(f'????????Došlo je do greške prilikom preuzimanja stranice {i}')
            continue

        for crossword_base_data in crossword_base_data_objects:

            try:
                crossword_xml_data = get_xml_dict_from_url(crossword_base_data.crosswordUrl)

                crossword = combine_xml_data_and_crossword_base_data_into_crossword(crossword_xml_data,
                                                                                    crossword_base_data)

                if not os.path.exists(f'{shared_save_location}/{crossword.name}'):
                    os.mkdir(f'{shared_save_location}/{crossword.name}')

                pdf_data = requests.get(crossword.pdfUrl).content
                file = open(f'{shared_save_location}/{crossword.name}/{crossword.name}.pdf', 'wb')
                file.write(pdf_data)
                file.close()

                # try:
                #     pil_images = pdf2image.convert_from_path(
                #         f'{shared_save_location}/{crossword.name}/{crossword.name}.pdf', dpi=DPI,
                #         output_folder=f'{shared_save_location}/{crossword.name}',
                #         first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT,
                #         thread_count=THREAD_COUNT, userpw=USERPWD,
                #         use_cropbox=USE_CROPBOX, strict=STRICT)
                #
                #     pil_images[0].save(f'{shared_save_location}/{crossword.name}/{crossword.name}.jpg')
                # except Exception as e:
                #     print(e)

                json_data = crossword.to_json()
                file = open(f'{shared_save_location}/{crossword.name}/{crossword.name}.json', 'w')
                file.write(json_data)
                file.close()

                print(f'Uspešno sačuvana osmosmerka {crossword.name}')

            except:
                try:
                    print(f'!!!!!!!!!Neuspešno sačuvana osmosmerka {crossword_base_data.name}')
                except Exception as e:
                    print(e)
                continue


if __name__ == '__main__':
    get_crosswords()

    print("sve gotovo")
