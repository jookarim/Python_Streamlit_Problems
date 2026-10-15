from repositories.attendance_repository import AttendanceRepository 
from models.attendance import Attendance 
from validation.attendance_validation import AttendanceValidation 

class AttendanceExplorer:
    def __init__(
        self,
        attendance_repository: AttendanceRepository
    ):
        self.attendance_repository = attendance_repository 
    
    def get_first_record(self) -> Attendance | None:
        AttendanceValidation.validate_found_attendance_records(
            self.attendance_repository.get_all_attendance_records()
        )
        
        return self.attendance_repository.get_all_attendance_records()[0]
    
    def get_last_record(self) -> Attendance | None:
        AttendanceValidation.validate_found_attendance_records(
            self.attendance_repository.get_all_attendance_records()
        )
        
        return self.attendance_repository.get_all_attendance_records()[-1]
    
    def get_recent_records(self) -> list[Attendance] | None:
        AttendanceValidation.validate_found_attendance_records(
            self.attendance_repository.get_all_attendance_records()
        )
         
        all_records = self.attendance_repository.get_all_attendance_records() 
        
        if len(all_records) >= 5:
            return self.attendance_repository.get_all_attendance_records()[-5: ]
        
        return self.attendance_repository.get_all_attendance_records()[-len(all_records): ]
    