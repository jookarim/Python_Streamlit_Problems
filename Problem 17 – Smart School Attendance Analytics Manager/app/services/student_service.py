from models.student import Student 
from repositories.student_repository import StudentRepository 
from validation.student_validation import StudentValidation 

class StudentService:
    def __init__(
        self,
        student_repository: StudentRepository
    ):
        self.student_repository = student_repository 
    
    def register_student(
        self,
        student_id: str,
        student_name: str,
        student_class: str
    ) -> None:
        
        StudentValidation.validate_student_data(
            student_id,
            student_name, 
            student_class
        )
        
        found_id = self.student_repository.check_id_found(
            student_id
        )
        
        StudentValidation.validate_duplicate_id(
            found_id
        )
        
        self.student_repository.add_student(
            student_id,
            student_name, 
            student_class     
        )
    
    def search_student(
        self,
        student_id: str, 
        student_name: str,
        student_class: str
    ) -> list[Student] | None:
        
        search_result = self.student_repository.get_students_by(
            student_id, 
            student_name, 
            student_class
        )
        
        StudentValidation.validate_search_result(
            search_result
        )
        
        return search_result
    
    def get_all_students(self) -> list[Student]:
        return self.student_repository.get_all_students()
    
    def get_name_class_from_id(
                                self,
                                student_id: str
                            ) -> tuple[str, str]:
        
        return self.student_repository.get_name_class_from_id(
            student_id
        )