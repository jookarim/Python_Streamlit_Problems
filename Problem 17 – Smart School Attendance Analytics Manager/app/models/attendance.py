from datetime import date 

class Attendance:
    def __init__(
        self,
        student_id: str,
        attendance_date: date,
        attendance_status: str
    ):
        self.student_id = student_id 
        self.attendance_date = attendance_date 
        self.attendance_status = attendance_status       