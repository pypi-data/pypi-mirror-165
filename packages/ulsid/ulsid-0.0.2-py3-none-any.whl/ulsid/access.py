'''
Accesses and extract student numbers from their source.

Author: Sekgobela Kevin
Date: August 2022
Language: Python 3
'''
import importlib
import typing
import mimetypes
import os
import re

from . import analyse
from . import generate
from . import exceptions


def _import_navaly():
    # Imports navaly library
    #return importlib.import_module("naval")
    try:
        import naval as _naval
    except ImportError:
        err_msg = "Cant import navaly, please install with " +\
            "'pip install navaly'"
        raise ImportError(err_msg)
    return _naval


def _navaly_importable():
    # Check if navaly can be imported
    try:
        _import_navaly()
    except ImportError:
        return False
    else:
        return True



def _extract_text_bytes(source, content_type):
    # Extract text from bytes of content type
    # This interface should be added to navaly
    naval_lib = _import_navaly()
    return naval_lib.extract_text(
        parse_input=source,
        source_locates_data=False,
        content_type=content_type,
    )

def _extract_text_string(source, content_type):
    # Extract text from string of content type
    # This interface should be added to navaly
    naval_lib = _import_navaly()
    return naval_lib.extract_text(
        parse_input=source,
        source_locates_data=False,
        content_type=content_type,
    )

def _is_plain_text_file(file_path):
    # Returns True if file path points to plain text file
    if not mimetypes.inited:
        mimetypes.init()
    return mimetypes.guess_type(file_path)[0] == "text/plain"

def _is_text_file(file_path):
    # Returns True if file path points to plain text file
    if not mimetypes.inited:
        mimetypes.init()
    return mimetypes.guess_type(file_path)[0].startswith("text/")

def extract_text_path(path, content_type=None):
    # Extacts text from file in path
    if os.path.isfile(path):
        if content_type == "text/plain" or _is_plain_text_file(path):
            with open(path, "r") as fp:
                return fp.read()
        else:
            naval_lib = _import_navaly()
            return naval_lib.extract_text(
                path, content_type=content_type
            )
    else:
        err_msg = "'{}' is not valid file path".format(path)
        raise ValueError(err_msg)

def filter_student_numbers(student_numbers, **kwargs):
    # Filters iterator into allowing only expected student numbers
    def filter_callaback(student_number):
        return generate.student_number_supported(
            student_number, **kwargs
        )
    return filter(filter_callaback, student_numbers)

def extract_student_numbers(text: str, **kwargs):
    # Extracts student numbers from text as specified by optional
    pattern = generate.create_regex_pattern(**kwargs)
    print(pattern)
    matches = re.findall(pattern, text)
    if matches:
        student_numbers = ["".join(match) for match in matches]
        return list(filter_student_numbers(student_numbers, **kwargs))
    else:
        return []

def extract_student_numbers_file(path: str, content_type=None, **kwargs):
    # Extracts student numbers from file in path.
    # This function may attept to use navaly for non plain text files.
    # Navaly can be install with 'pip install navaly'
    file_text = extract_text_path(path, content_type)
    return extract_student_numbers(file_text, **kwargs)


if __name__ == "__main__":
    file_path = "file.pdf"
    numbers = extract_student_numbers_file(file_path, start_year=2021)
    print(numbers)
