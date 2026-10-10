class Student:
    """Class that defines student as object to be used
    when returning data from repository"""
    
    def __init__(
            self, 
            student_id: str,
            student_name: str,
            student_class: str):
        
        """Set data of the Student model in the constructor"""
        
        self.student_id = student_id 
        self.student_name = student_name 
        self.student_class = student_class 