from exceptions import student_exceptions
from models.student import Student

class StudentValidation:
    @staticmethod 
    def validate_student_data(
        student_id: str,
        student_name: str,
        student_class: str
    ) -> None:
        if (
            not student_id 
            or not student_name 
            or not student_class
        ):
            raise student_exceptions.InvalidStudentDataException(
                "Invalid student data"
            )
    
    @staticmethod
    def validate_id(
        student_id: str
    ):
        if not student_id:
            raise student_exceptions.InvalidStudentIDException(
                "Invalid student id"
            )

    @staticmethod            
    def validate_duplicate_id(
        found_id: bool
    ) -> None:
        if found_id:
            raise student_exceptions.DuplicateStudentException(
                "Student already found"
            )
    
    @staticmethod
    def validate_not_found_id(
        found_id: bool
    ) -> None:
        if not found_id:
            raise student_exceptions.StudentNotFoundException(
                "Student not found"
            )
            
    @staticmethod
    def validate_search_result(
        search_result: list[Student]
    ) -> None:
        if not search_result:
            raise student_exceptions.EmptySearchResultException(
                "Search result is empty"
            )