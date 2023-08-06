'''
Generates student numbers

Author: Sekgobela Kevin
Date: August 2022
Language: Python 3
'''
from . import exceptions
from . import analyse

import typing
import random
import time


#########################################################
# Functions here are meant for assisting main functions.
# They help in getting values from keywords arguments.
# Also with calculating some values from the argumnets.
# Some help in raising exceptions for reuse.
#########################################################

def get_start_year_from_kwargs(**kwargs):
    # Gets start year from arguments else gets default one
    return kwargs.get("start_year", analyse.DEFAULT_START_YEAR)

def get_end_year_from_kwargs(**kwargs):
    # Gets start year from arguments else gets default one
    return kwargs.get("end_year", analyse.DEFAULT_END_YEAR)

def calculate_start_position(year_first_position:int):
    # Calculates start position based on year_first_position
    return year_first_position

def calculate_end_position(start_pos:int, year_capacity:int):
    # Calculates end position from start position and capacity
    return analyse.caculate_last_postion(start_pos, year_capacity)

def get_start_pos_from_kwargs(**kwargs):
    # Gets start year from arguments else calculates it.
    first_position = analyse.get_first_position_from_kwargs(**kwargs)
    return kwargs.get("start_pos", first_position)

def get_end_pos_from_kwargs(**kwargs):
    # Gets start year from arguments else calculates it.
    end_pos = kwargs.get("end_pos", None)
    if end_pos != None:
        return end_pos
    else:
        # Calculates end position from year first pos and capacity.
        # Realise that year first position was used than start_pos
        first_position = analyse.get_first_position_from_kwargs(**kwargs)
        year_capacity = analyse.get_capacity_from_kwargs(**kwargs)
        return calculate_end_position(first_position, year_capacity)

def year_range_exception(start_year:int=None, end_year:int=None, 
    strict=True):
    # Returns exception if any or None
    # if start_year > end_year:
    #     err_msg = "Start year {} cant be greater than end year {}"
    #     return ValueError(err_msg.format(start_year, end_year))
    
    # if strict:
    #     if start_year < analyse.DEFAULT_START_YEAR:
    #         err_msg = "Start year {} cant be less than default " +\
    #             "end year {} when strict is enabled."
    #         return ValueError(err_msg.format(end_year, 
    #             analyse.DEFAULT_START_YEAR))
    #     if end_year > analyse.DEFAULT_END_YEAR:
    #         err_msg = "End year {} cant be greater than default " +\
    #             "end year {} when strict is enabled."
    #         return ValueError(err_msg.format(end_year, 
    #             analyse.DEFAULT_END_YEAR))

    # Its still possible for start and end year to be invalid
    if not analyse.year_valid(start_year, strict):
        return exceptions.UnsupportedYearError(start_year)
    if not analyse.year_valid(start_year, strict):
        return exceptions.UnsupportedYearError(end_year)


def year_position_exception(start_pos:int=None, end_pos:int=None, **kwargs):
    # Returns exception if any or None
    # Gets year capacity from arguments else gets default one
    # year_capacity = analyse.get_capacity_from_kwargs(**kwargs)
    # # Gets first position from arguments else gets default one
    # first_position = analyse.get_first_position_from_kwargs(**kwargs)
    # # Calculates max position based on start pos and capacity
    # max_end_pos = analyse.caculate_last_postion(start_pos, year_capacity)
    
    # if start_pos > end_pos:
    #     err_msg = "Start position {} cant be less than end position {}"
    #     error_msg = err_msg.format(start_pos, end_pos)

    # if start_pos < first_position:
    #     err_msg = "Start position {} cant be less than first position {}"
    #     error_msg = err_msg.format(start_pos, first_position)
    #     raise ValueError(error_msg)

    # if end_pos > max_end_pos:
    #     err_msg = "End position {} cant be greater than last position {}"
    #     err_msg = err_msg.format(end_pos, max_end_pos)
    #     raise ValueError(err_msg)

    # Its still possible for start and end position to be invalid
    if not analyse.position_valid(start_pos, **kwargs):
        return exceptions.UnsupportedPositionError(start_pos)
    if not analyse.position_valid(end_pos, **kwargs):
        return exceptions.UnsupportedPositionError(end_pos)

def raise_exception(exception:Exception):
    # Raises exception if exception is not None
    if exception != None:
        raise exception
    else:
        # This is done for linters to avoid 'Code not reachable'
        # or -> NoReturn
        return None

##############################################################
#               End for helpers functions
##############################################################

def guess_position(start_pos:int=None, end_pos:int=None, **kwargs):
    # Guesses position to be used with student number

    # Updates start_pos if not provided on argumnets
    if start_pos == None:
        start_pos = analyse.get_first_position_from_kwargs(**kwargs)
    
    # Updates end_pos if not provided on argumnets
    if end_pos == None:
        end_pos = get_end_pos_from_kwargs(**kwargs)

    # Raises exception if any
    exception = year_position_exception(start_pos, end_pos, **kwargs)
    raise_exception(exception)

    # Uses start pos and end pos to guess position
    return random.randint(start_pos, end_pos)

def guess_position_part(start_pos:int=None, end_pos:int=None, **kwargs):
    # Guesses position part to be used with student number
    position = guess_position(start_pos, end_pos, **kwargs)
    return analyse.position_to_position_part(position, **kwargs)


def guess_year(start_year:int=None, end_year:int=None, strict=True):
    # Guesses year to be used with student number
    if start_year == None:
        start_year = get_start_year_from_kwargs()
    if end_year == None:
        end_year = get_end_year_from_kwargs()

    # Raises exception if any regarding argumets
    exception = year_range_exception(start_year, end_year, strict)
    raise_exception(exception)

    return random.randint(start_year, end_year)

def guess_year_part(start_year:int=None, end_year:int=None, strict=True):
    # Guesses year part to be used with student number
    year = guess_year(start_year, end_year, strict)
    return analyse.year_to_year_part(year, strict)


def guess_student_number(
    start_year:int=None, 
    end_year:int=None, 
    start_pos:int=None, 
    end_pos:int=None, 
    strict=True,
    **kwargs):
    # Guesses student number limited by provided arguments
    year_part = guess_year_part(start_year, end_year, strict)
    position_part = guess_position_part(start_pos, end_pos, **kwargs)
    return year_part + position_part


def common_leading_substring(__str:str, __str2:str):
    # Returns substring which both strings starts with.
    startswith = ""
    for i in range(len(__str)):
        try:
            if __str[i] == __str2[i]:
                startswith += __str[i]
            else:
                break
        except IndexError:
            break
    return startswith


def extract_remaing_substring(__str:str, leading_substring:str):
    if __str.startswith(leading_substring):
        return __str[len(leading_substring):]
    else:
        err_msg = "string '{}' needs to start with '{}'"
        err_msg = err_msg.format(__str, leading_substring)
        raise ValueError(err_msg)

def occurance_range_regex(start:int, end:int=None, regex_char=r"\d"):
    # Returns regex for certain occurances of character
    pattern = ""
    if end == None or start == end:
        if start != 0:
            pattern = regex_char + "{" + str(start) + "}"
    else:
        pattern = regex_char + "{" + str(start) + "," +\
            str(end) + "}"
    return pattern


def range_regex(start:int, end:int, regex_digit=r"\d"):
    start = str(start)
    end = str(end)

    # Extracts leading parts of string
    if len(start) == len(end):
        leading_string = common_leading_substring(start, end)
    else:
        # Ingnore leading string integers have differnt digits length
        leading_string = ""

    # Extracts remaing parts of start and end strings
    start_remainig_string = extract_remaing_substring(start, leading_string)
    end_remainig_string = extract_remaing_substring(end, leading_string)

    remaining_pattern = "" # pattern for remaining digits
    leading_digits_pattern = leading_string # matched as it is

    if start_remainig_string or end_remainig_string:
        if len(start_remainig_string) == len(end_remainig_string):
            # Handles regex for remaining characters
            remaining_string_length = len(start_remainig_string)
            # Creates pattern for first digit
            remaining_pattern = "[" + start_remainig_string[0] + "-" +\
                end_remainig_string[0] + "]"
            # Creates pattern for other remaining digits
            # Its better to ignore if no other digits left
            if remaining_string_length-1 != 0:
                # -1 is for digit already added to remaining_pattern
                remaining_pattern += occurance_range_regex(
                    remaining_string_length-1, regex_char=regex_digit
                    )
        else:
            remaining_pattern = "[1-9]"
            if start_remainig_string:
                if int(start_remainig_string) == 0:
                    # Zero is allowed for at begining of integer
                    # This is because that integer is allowed to be 0
                    remaining_pattern = occurance_range_regex(
                        len(start_remainig_string), 
                        len(end_remainig_string),
                        regex_digit
                    )
                else:
                    # -1 is for character already added to remaining_pattern
                    # Zero is not allowed at begining of integer
                    remaining_pattern += occurance_range_regex(
                        len(start_remainig_string)-1, 
                        len(end_remainig_string)-1,
                        regex_digit
                    )
            else:
                # -1 is for character already added to remaining_pattern
                # Zero is not allowed at begining of integer
                # Matches exatly digits of length and they should start
                # with zero.
                remaining_pattern += occurance_range_regex(
                    len(end_remainig_string)-1, regex_char=regex_digit
                )
    else:
        # Remaining parts are empty
        pass

    # leading_string should be matched extly as it is.
    return leading_digits_pattern + remaining_pattern

    
def create_position_parts_regex(   
    start_pos:int=None, 
    end_pos:int=None, 
    **kwargs):
    # Creates regex pattern position part of student number.
    # The pattern is enough to filter a lot of other digits in 
    # regex string without guarantee that matched regex string is 
    # valid position part as specified by argumets.
    # In most cases it will perform as expected but issue may be with
    # leading zeros.
    if start_pos == None:
        start_pos = get_start_pos_from_kwargs(**kwargs)
    if end_pos == None:
        end_pos = get_end_pos_from_kwargs(**kwargs)

    # Raises exception if any regarding provided argumnets
    exception = year_position_exception(start_pos, end_pos, **kwargs)
    raise_exception(exception)

    # calculates maximum position length
    year_capacity = analyse.get_capacity_from_kwargs(**kwargs)
    year_first_position = analyse.get_first_position_from_kwargs(**kwargs)
    max_position_length = analyse.calculate_position_length(
        year_first_position, year_capacity
    )

    # Calculates minum and maximul leading zeros for position part
    min_leading_zeros = max_position_length - len(str(end_pos))
    max_leading_zeros = max_position_length - len(str(start_pos))

    # Creates pattern for matching leading zeros
    # Matched leading zeros wont always mean position part is valid.
    leading_zeros_pattern = occurance_range_regex(min_leading_zeros, 
        max_leading_zeros, "0")
    # Creates pattern for matching position integer
    position_pattern = range_regex(start_pos, end_pos)

    # Combines the to patterns to create pattern for position part.
    return leading_zeros_pattern + position_pattern

def create_year_part_regex(   
    start_year:int=None, 
    end_year:int=None, 
    strict=True):
    if start_year == None:
        start_year = get_start_year_from_kwargs()
    if end_year == None:
        end_year = get_end_year_from_kwargs()

    # Raises exception if any regarding argumets
    exception = year_range_exception(start_year, end_year, strict)
    raise_exception(exception)

    # Creates start parts for years to use on patterns
    start_year_part = analyse.year_to_year_part(start_year, strict)
    end_year_part = analyse.year_to_year_part(end_year, strict)

    return range_regex(int(start_year_part), int(end_year_part))

def create_regex_pattern(    
    start_year:int=None, 
    end_year:int=None, 
    start_pos:int=None, 
    end_pos:int=None, 
    strict=True,
    **kwargs):
    # Creates regex pattern for student numbers
    years_part_pattern = create_year_part_regex(start_year, end_year, 
        strict)
    positions_pattern = create_position_parts_regex(
        start_pos, end_pos, **kwargs
    )
    return years_part_pattern + positions_pattern


def student_number_supported(    
    student_number:int,
    start_year:int=None, 
    end_year:int=None, 
    start_pos:int=None,
    end_pos:int=None, 
    strict=True,
    **kwargs):
    # Validates student number against range of years and positions.
    # This function is similar to analyse.student_number_valid().
    # But it can handle generate module specific arguments like
    # 'start_year' and 'start_pos'.
    # analyse.student_number_valid() does not support such arguments.

    # Sets optional argumets values if not provided
    if start_pos == None:
        start_pos = get_start_pos_from_kwargs(**kwargs)
    if end_pos == None:
        end_pos = get_end_pos_from_kwargs(**kwargs)

    # Sets optional argumnets values if not provided
    if start_year == None:
        start_year = get_start_year_from_kwargs()
    if end_year == None:
        end_year = get_end_year_from_kwargs()

    # Raises exception if any regarding argumets
    exception = year_range_exception(start_year, end_year, strict)
    raise_exception(exception)

    # Invalid student number is already not allowed.
    if analyse.student_number_valid(student_number, strict, **kwargs):
        # Extracts year and position of student number
        year = analyse.extract_year(student_number, strict, **kwargs)
        position = analyse.extract_position(student_number, **kwargs)
        # Checks year and position of studedent numbers
        year_allowed = year >= start_year and year <= end_year
        postion_allowed = position >= start_pos and position <= end_pos
        # Both year and position need to be allowed
        return year_allowed and postion_allowed
    else:
        return False

def create_student_number(
    year:int, 
    position:int, 
    start_year:int=None, 
    end_year:int=None, 
    start_pos:int=None,
    end_pos:int=None, 
    strict=True,
    **kwargs):
    # Creates student number from year and position
    year_part = analyse.year_to_year_part(year, strict)
    position_part = analyse.position_to_position_part(position, **kwargs)
    student_number = int(year_part  + position_part)
    # Checks if student number is supported if not raises exception.
    is_supported = student_number_supported(
        student_number, 
        start_year=start_year, 
        end_year=end_year, 
        start_pos=start_pos, 
        end_pos=end_pos, 
        strict=strict, 
        **kwargs
    )
    if is_supported:
        return student_number
    else:
        # Student number is valid but not supported
        raise exceptions.UnsupportedStudentNumber(student_number)





def next_student_number(    
    student_number:int,
    start_year:int=None, 
    end_year:int=None, 
    start_pos:int=None,
    end_pos:int=None, 
    strict=True,
    same_year=False,
    **kwargs):
    # Returns next student number after provided one.
    # Captures kewyords arguments into dict for reuse.
    other_kwargs = {
            "start_year": start_year, 
            "end_year": end_year, 
            "start_pos": start_pos,
            "end_pos": end_pos, 
            "strict": strict
        }
    # Extarcts year and position of student number
    position = analyse.extract_position(student_number, **kwargs)
    year = analyse.extract_year(student_number, strict, **kwargs)

    # Creates new student number by incrementing position
    try:
        _student_number = create_student_number(
            year, position+1, **other_kwargs, **kwargs
        )
    except exceptions.StudentNumberError:
        if same_year:
            # Next student number only be of same year
            # Year is never incremented when end_pos is reached.
            return
    else:
        return _student_number
        

    # Creates new student number by incrementing year
    # Position is reset to start position.
    try :
        start_pos = get_start_pos_from_kwargs(**other_kwargs)
        _student_number = create_student_number(
            year+1, start_pos, **other_kwargs,**kwargs
        )
    except exceptions.StudentNumberError:
        pass
    else:
        return _student_number
    
    # Next student number cannot be created.
    # Likely this is the last student number supported.

        

def create_student_numbers(
    start_year:int=None, 
    end_year:int=None, 
    start_pos:int=None,
    end_pos:int=None, 
    strict=True,
    **kwargs):
    # Creates studnet numbers based on provided arguments

    # Sets optional argumets values if not provided
    if start_pos == None:
        start_pos = get_start_pos_from_kwargs(**kwargs)
    if end_pos == None:
        end_pos = get_end_pos_from_kwargs(**kwargs)

    # Sets optional argumnets values if not provided
    if start_year == None:
        start_year = get_start_year_from_kwargs()
    if end_year == None:
        end_year = get_end_year_from_kwargs()

    # Raises exception if any regarding argumets
    exception = year_range_exception(start_year, end_year, strict)
    raise_exception(exception)

    # Prepares years and positions for student numbers
    years = range(start_year, end_year+1)
    positions = range(start_pos, end_pos+1)

    # Loops and yield student numbers
    for year in years:
        for position in positions:
            yield create_student_number(year, position, **kwargs)


if __name__ == "__main__":
    student_number = 202399998
    print(list(create_student_numbers(start_year=2020, year_capacity=10)))
    