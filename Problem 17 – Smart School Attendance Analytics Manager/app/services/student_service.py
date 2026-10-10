
from repositories.student_repository import StudentRepository
from validation.student_validator import StudentValidator
from models.student import Student


class StudentService:
    def __init__(
        self,
        student_repository: StudentRepository
    ) -> None:

        self.student_repository = student_repository

    def add_student(
        self,
        student_id: str,
        student_name: str,
        student_class: str
    ) -> None:

        StudentValidator.validate_student(
            student_id,
            student_name,
            student_class
        )

        self.student_repository.add_student(
            student_id,
            student_name,
            student_class  
        )

    def delete_student(
        self,
        student_id: str
    ) -> None:

        StudentValidator.validate_id(student_id)
        self.student_repository.remove_student(student_id)

    def search_student(
        self,
        student_id: str,
        student_name: str,
        student_class: str
    ) -> list[Student]:

        return self.student_repository.search_student_by(
            student_id,
            student_name,
            student_class
        )

    def get_all_students(self) -> list[Student]:
        return self.student_repository.get_all_students()
