from repositories.student_repository import StudentRepository 
from repositories.attendance_repository import AttendanceRepository
from validation.student_validation import StudentValidation 

class SchoolService:
    def __init__(
        self,
        student_repository: StudentRepository,
        attendance_repository: AttendanceRepository
    ) -> None:
        self.student_repository = student_repository 
        self.attendance_repository = attendance_repository 
    
    def delete_student(
        self,
        student_id: str,
    ) -> None:
        StudentValidation.validate_id(
            student_id
        )
        
        found_id = self.student_repository.check_id_found(
            student_id
        )
        
        StudentValidation.validate_not_found_id(found_id)
        
        self.student_repository.delete_student(
            student_id
        )
        
        self.attendance_repository.delete_attendance_history(
            student_id
        )
        
        