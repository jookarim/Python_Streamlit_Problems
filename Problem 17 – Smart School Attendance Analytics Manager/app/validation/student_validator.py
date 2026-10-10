from exceptions import students_exceptions 

class StudentValidator:
    @staticmethod 
    def validate_id(student_id: str) -> None:
        if not student_id:
            raise students_exceptions.InvalidStudentIDException("Invalid student id")
    
    @staticmethod 
    def validate_name(student_name: str) -> None:
        if not student_name:
            raise students_exceptions.InvalidStudentNameException("Invalid student name")
    
    @staticmethod 
    def validate_class(class_name: str) -> None:
        if not class_name:
            raise students_exceptions.InvalidClassException("Invalid student class")
    
    @staticmethod 
    def validate_student(
        student_id: str,
        student_name: str,
        class_name: str
    ) -> None:
        StudentValidator.validate_id(student_id)
        StudentValidator.validate_name(student_name)
        StudentValidator.validate_class(class_name)