from repositories.attendance_repository import AttendanceRepository
from validation.attendance_validation import AttendanceValidation 
from models.attendance import Attendance 

from datetime import date 

class AttendanceService:
    def __init__(
        self,
        attendance_repository: AttendanceRepository
    ):
        self.attendance_repository = attendance_repository 
    
    def record_attendance(
        self,
        student_id: str,
        attendance_date: date,
        attendance_status: str
    ):
        AttendanceValidation.validate_attendance_data(
            student_id,
            attendance_date
        )
        
        already_recorded = self.attendance_repository.attendance_already_recorded(
            student_id,
            attendance_date 
        )
        
        AttendanceValidation.validate_attendance_already_recorded(
            student_id,
            already_recorded
        )
        
        self.attendance_repository.add_attendance(
            student_id,
            attendance_date,
            attendance_status
        )
    
    def correct_attendance(
        self,
        student_id: str,
        attendance_date: date,
        new_status: str
    ):
        AttendanceValidation.validate_attendance_data(
            student_id,
            attendance_date 
        )
        
        already_recorded = self.attendance_repository.attendance_already_recorded(
            student_id,
            attendance_date 
        )
                
        AttendanceValidation.validate_attendance_not_recorded(
            student_id,
            already_recorded
        )
        
        self.attendance_repository.correct_attendance(
            student_id,
            attendance_date,
            new_status
        )
        
    def sort_by_date(
        self,
        ascending: bool
    ) -> None:
        AttendanceValidation.validate_found_attendance_records(
            self.get_all_attendance_records()
        )
        
        self.attendance_repository.sort_attendance_by_date(
            ascending
        )
        
    def get_all_attendance_records(self) -> list[Attendance]:
        return self.attendance_repository.get_all_attendance_records()