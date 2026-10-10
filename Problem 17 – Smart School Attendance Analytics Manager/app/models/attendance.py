class Attendance:
    def __init__(self,
                student_id: str, 
                attendance_date: str, 
                status: str) -> None:
        
        self.student_id = student_id 
        self.attendance_date = attendance_date 
        self.status = status 
        