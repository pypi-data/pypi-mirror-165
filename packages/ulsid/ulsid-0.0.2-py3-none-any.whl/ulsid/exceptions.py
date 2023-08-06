'''
Exception classes for ulsid

Author: Sekgobela Kevin
Date: August 2022
Language: Python 3
'''


class UlsidError(Exception):
    '''Base class for ulsid exceptions'''
    pass

class StudentNumberError(UlsidError):
    '''Base class for exceptions regarding student numbers'''
    def __init__(self, student_number: int) -> None:
        self.student_number = student_number
        error_msg = self.create_error_message()
        super().__init__(error_msg)

    def create_error_message(self):
        err_msg = "There is problem with student number {student_id}"
        return err_msg.format(student_id=self.student_number)

class InvalidStudentNumber(StudentNumberError):
    '''Student number is invalid'''
    def create_error_message(self):
        err_msg = "Student number {student_id} is invalid"
        return err_msg.format(student_id=self.student_number)

class UnsupportedStudentNumber(StudentNumberError):
    '''Student number is valid but not supported'''
    def create_error_message(self):
        err_msg = "Student number {student_id} is not supported"
        return err_msg.format(student_id=self.student_number)


class StudentNumberOtherError(StudentNumberError):
    def __init__(self, other, student_number:int=None) -> None:
        self.other = other
        super().__init__(student_number)

    def create_message_template(self):
        return "Error with {other} of student number {student_id}"

    def create_error_message(self):
        if self.student_number == None:
            student_number = ""
        else:
            student_number = self.student_number
        
        err_msg = self.create_message_template()
        return err_msg.format(
            other=self.other, 
            student_id=student_number, 
        )
    
class StudentNumberPartError(StudentNumberOtherError):
    '''Exceptions regarding parts of student number'''
    
    def __init__(self, part: str, student_number:int=None) -> None:
        super().__init__(part, student_number)

    def create_message_template(self):
        return "Part {other} of student number {student_id} is invalid"


class YearPartError(StudentNumberPartError):
    '''Exception regarding year part of student number'''
    def create_message_template(self):
        return "Year part {other} of student number {student_id} is invalid"

class PositionPartError(StudentNumberPartError):
    '''Exception regarding position part of student number'''
    def create_message_template(self):
        return "Position part {other} of student number {student_id} " +\
            "is invalid"


class YearError(StudentNumberOtherError):
    '''Errors relating to year of student number'''
    def __init__(self, year: int, student_number:int=None) -> None:
        self.year = year
        super().__init__(year, student_number)

    def create_message_template(self):
        return "Error with year {other} of student number {student_id}"

class InvalidYearError(YearError):
    def create_message_template(self):
        return "Year {other} is invalid for student number"

class UnsupportedYearError(YearError):
    def create_message_template(self):
        return "Year {other} is not supported for student number"


class PositionError(StudentNumberOtherError):
    '''Errors relating to position of student number'''
    def __init__(self, position: int, student_number:int=None) -> None:
        self.position = position
        super().__init__(position, student_number)

    def create_message_template(self):
        return "Error with position {other} of student number {student_id}"

class InvalidPositionError(PositionError):
    def create_message_template(self):
        return "Position {other} is invalid for student number"

class UnsupportedPositionError(PositionError):
    def create_message_template(self):
        return "Position {other} is not supported for student number"


class NavalNotInstalledError(UlsidError):
    pass
