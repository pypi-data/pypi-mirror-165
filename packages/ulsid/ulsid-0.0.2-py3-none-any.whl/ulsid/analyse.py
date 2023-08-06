'''
Analyses and breaks-down student numbers

Author: Sekgobela Kevin
Date: August 2022
Language: Python 3
'''
import typing
import time

from . import exceptions



UL_START_YEAR = 1959 # Year UL started to operate
MIN_SUPPORTED_YEAR = 1000 # Minimum supported year

# 'Year 2000 bug' or 'Year 2000 problem'
# The year caused year parts of student numbers to change.
Y2K_YEAR = 2000
BEFORE_Y2K_YEAR = Y2K_YEAR - 1

# Year UL started to operate
DEFAULT_START_YEAR = UL_START_YEAR
# End year is based on current year plus 1
DEFAULT_END_YEAR = time.gmtime(time.time()).tm_year + 1

DEFAULT_YEAR_FIRST_POS = 0 # First position likely 0
DEFAULT_YEAR_CAPACITY = 100000 # Max capacity for a each year


#################################################################
# Functions starting here are to be used by main module funtions
#################################################################

def get_capacity_from_kwargs(**kwargs):
    # Gets year capacity from arguments else gets default one
    return kwargs.get("year_capacity", DEFAULT_YEAR_CAPACITY)

def get_first_position_from_kwargs(**kwargs):
    # Gets first position from arguments else gets default one
    return kwargs.get("year_first_position", DEFAULT_YEAR_FIRST_POS)

def caculate_last_postion(
    year_first_position: typing.Union[int, None] = None, 
    year_capacity: typing.Union[int, None] = None):
    # Calculates last position for student numbers
    # year_first_position: first position for the year.
    # year_capacity: maximum student that can be accomodated in a year.
    if year_first_position ==  None:
        year_first_position = DEFAULT_YEAR_FIRST_POS
    if year_capacity == None:
        year_capacity = DEFAULT_YEAR_CAPACITY
    return (year_capacity + year_first_position) - 1

def calculate_year_capacity(year_first_position, year_last_position):
    # Calculates year capacity from year first and last position
    # year_last_position = (year_capacity + year_first_position) - 1
    # -year_capacity = (year_first_position - year_last_position) - 1
    # year_capacity = ((year_first_position - year_last_position) - 1)/-1
    return ((year_first_position - year_last_position) - 1)/-1

def calculate_position_length(
    year_first_position: typing.Union[int, None] = None, 
    year_capacity: typing.Union[int, None] = None):
    # Calculates length(chars) position part of student number.
    last_position = caculate_last_postion(
        year_first_position, year_capacity
    )
    return len(str(last_position))

#################################################################
#                  END for helpers functions
#################################################################


def year_valid(year: int, strict=True):
    # Checks if year is valid or supported
    min_year_satisfied = year >= MIN_SUPPORTED_YEAR
    if not strict:
        return min_year_satisfied
    else:
        return min_year_satisfied and year <= DEFAULT_END_YEAR

def year_part_valid(year_part: str, strict=True):
    # Checks if year part is valid
    if year_part.isdigit():
        if strict and len(year_part) == 2:
            # related to year_to_year_part()
            year_part = "19" + year_part
        return year_valid(int(year_part), strict)
    else:
        return False


def position_valid(position: int, **kwargs):
    # Check if position is valid
    first_position = get_first_position_from_kwargs(**kwargs)
    capacity = get_capacity_from_kwargs(**kwargs)
    last_postion = caculate_last_postion(first_position, capacity)
    return position >= first_position and position <= last_postion
    
def position_part_valid(position_part: str, **kwargs):
    # Checks if position part is valid
    if position_part.isdigit():
        return position_valid(int(position_part), **kwargs)
    else:
        return False
    
def position_part_to_position(position_part: str, **kwargs):
    # Convert position part to position integer
    if position_part_valid(position_part, **kwargs):
        return int(position_part)
    else:
        raise exceptions.PositionPartError(position_part)

def position_to_position_part(position: int, **kwargs):
    # Convert position integer to its position part
    if position_valid(position, **kwargs):
        position_length = calculate_position_length(**kwargs)
        return str(position).zfill(position_length)
    else:
        raise exceptions.InvalidPositionError(position)

def year_part_to_year(year_part: str, strict=True):
    # Convert position integer to its position part
    if year_part_valid(year_part, strict):
        if strict and len(year_part) == 2:
            return int("19"+year_part)
        else:
            return int(year_part)
    else:
        raise exceptions.YearPartError(year_part)

def year_to_year_part(year: int, strict=True):
    # Convert year integer to its year part
    year_str = str(year)
    if year_valid(year, strict):
        if strict and year_str.startswith("19"):
            return year_str[2:]
        return year_str
    else:
        raise exceptions.InvalidYearError(year)
    
        
def extract_position_part(student_number: int, **kwargs):
    # Extracts position part of student number
    student_number: str = str(student_number)
    position_length = calculate_position_length(**kwargs)
    position_part = student_number[position_length*-1:]
    # Position part should have same digits length as position_length
    if position_part_valid(position_part, **kwargs):
        return position_part
    else:
        raise exceptions.PositionPartError(position_part, student_number)

def extract_year_part(student_number: int, strict=True, **kwargs):
    # Extracts year part of student number
    student_number: str = str(student_number)
    position_length = calculate_position_length(**kwargs)
    year_part = student_number[:position_length*-1]
    # Year part should be atleast 2 or 4+ digits
    if year_part_valid(year_part, strict):
        return year_part
    else:
        # Year of student number should contain 2 or 4+ chars.
        # Years with 0, 1 or 3 are considered invalid.
        raise exceptions.YearPartError(year_part, student_number)

def extract_position(student_number: int, **kwargs):
    # Extracts posetion part of student number
    position_part = extract_position_part(student_number, **kwargs)
    try:
        return position_part_to_position(position_part, **kwargs)
    except exceptions.PositionPartError:
        raise exceptions.PositionPartError(position_part, student_number)

def extract_year(student_number: int, strict=True, **kwargs):
    # Extracts year of student number
    year_part = extract_year_part(student_number, **kwargs)
    try:
        return year_part_to_year(year_part, strict)
    except exceptions.YearPartError:
        # Re-raise exception with student number included
        raise exceptions.YearPartError(year_part, student_number)


def split_student_number(student_number: int, strict=True, **kwargs):
    # Splits student number into 2 parts representing year and 
    # application position
    position_part = extract_position_part(student_number, **kwargs)
    year_part = extract_year_part(student_number, strict)
    return year_part, position_part

def student_number_valid(student_number: int, strict=True, **kwargs):
    # Checks if student number is valid
    try:
        # If student number can be split then its valid
        split_student_number(student_number, strict, **kwargs)
    except exceptions.StudentNumberError:
        return False
    else:
        return True


if __name__ == "__main__":
    print(split_student_number(str(8534229216),  strict=False))

