import json
import os
import re
from typing import List, Dict, Optional, Union
from urllib.parse import quote_plus

import requests

from settings import PROJECT_ROOT
from utils.api.constants import GRID_PAGE_SIZES
from utils.ui.constants import DOWNLOAD_PATH

FILE_PATH = PROJECT_ROOT + '/parameters/files/'
COMMON_FILES = [os.path.join(FILE_PATH, 'some.pdf')]


def to_sort_query(instance_json: dict, exclude: list = None) -> List[str]:
    """
    Used to get query for sorting entities.

    Pass exclude parameter if you want to exclude some fields from query.

    Example:

    user = Users.manager
    to_sort_query(user.to_json, exclude=user.related_fields()) ->

    [
        'sort=[{"selector": "email", "desc": true}]',
        'sort=[{"selector": "email", "desc": false}]',
        ...
    ]
    """
    should_exclude = exclude or []

    desc = [
        'sort=' + json.dumps([{"selector": field, "desc": True}])
        for field in instance_json if field not in should_exclude
    ]
    asc = [
        'sort=' + json.dumps([{"selector": field, "desc": False}])
        for field in instance_json if field not in should_exclude
    ]
    return desc + asc


def to_pagination_query(page_sizes: Optional[List[int]] = None) -> List[Dict[str, Union[int, bool]]]:
    """
    :param page_sizes: List with numbers of entities to be returned by query API
    :return: query dict

    Example:
         to_pagination_query([5]) -> [{"skip": 0, "take": 5, 'requireTotalCount': True}]
         to_pagination_query([5, 10]) -> [
             {"skip": 0, "take": 5, 'requireTotalCount': True},
             {"skip": 0, "take": 10, 'requireTotalCount': True}
         ]
    """
    safe_page_sizes = page_sizes or GRID_PAGE_SIZES
    return [{"skip": 0, "take": page_size, 'requireTotalCount': True} for page_size in safe_page_sizes]


def get_default_files(exclude: list = None) -> List[str]:
    """
    Used to get all default parameters files as list.

    Optionally set "ignore", then this files will be ignored.

    Example:
    get_default_files() ->  ['parameters/files/some.docx', 'parameters/files/some.json', ...]
    """
    safe_exclude = [*(exclude or []), '.DS_Store', '__init__.py']
    files = list(filter(lambda f: f not in safe_exclude, os.listdir(FILE_PATH)))
    return [FILE_PATH + file for file in files]


def parse_filename_from_url(url: str) -> str:
    """
    :param url: Any file url
    :return: file name

    Example:
        some_url = 'https://some.domain.com/some.pdf?access_token=39e7fbd8-c4f3-456a-a744-dd43862ba8d3'
        parse_filename_from_url(some_url) -> 'some.pdf'
    """
    return re.search(r'(\w+)(\.\w+)+(?!.*(\w+)(\.\w+)+)', url).group()


def encode_to_url(string: str) -> str:
    """
    :param string: Any string
    :return: Url encoded string

    Used to encode string to url string. For example if strin has some
    characters like '/', ',', '.', '"', '[', ']' etc. this method will convert
    it to certain symbols.

    Example:
        encode_to_url('/path/to/some.png') -> '%2Fpath%2Fto%2Fsome.png'
        encode_to_url('/path[]to/some.png') -> '%2Fpath%5B%5Dto%2Fsome.png
        print(encode_to_url('"my string"')) -> '%22my+string%22''

    """
    return quote_plus(string.encode('utf8'))


def download_file(url, path=DOWNLOAD_PATH) -> tuple:
    """
    :param url: any url to download file
    :param path: path where file should be saved. By default all files will be saved
    in "downloads" dir in project root. Make sure to pass path and not file path:

    download_file('https://www.facebook.com/favicon.ico', 'images') # <- will work
    download_file('https://www.facebook.com/favicon.ico', 'images/favicon.ico') # <- will not work

    Used to download file from url to specific directory.

    Example:

    download_file('https://www.facebook.com/favicon.ico', 'images')

    Will create directory "images" in project root and save file favicon.ico into "images" dir.
    """
    response = requests.get(url, verify=False, allow_redirects=True)
    disposition = response.headers.get('content-disposition', None)
    file_name = parse_filename_from_url(url) if not disposition else re.findall("filename=(.+)", disposition)[0]
    file_path = os.path.join(path, file_name)

    if not os.path.exists(path):
        os.mkdir(path)

    with open(file_path, 'wb') as file:
        file.write(response.content)

    return file_path, file_name
