from repositories.attendance_repository import AttendanceRepository
from models.attendance import Attendance 
from validation.attendance_validator import AttendanceValidator

class AttendanceExplorer:
    def __init__(self, attendance_repository: AttendanceRepository) -> None:
        self.attendance_repository = attendance_repository 
    
    def get_first_record(self) -> Attendance:
        count_attendance_records = len(self.attendance_repository.get_all_records())
        AttendanceValidator.validate_record_count(count_attendance_records)
        return self.attendance_repository.get_all_records()[0]
    
    def get_last_record(self) -> Attendance:
        count_attendance_records = len(self.attendance_repository.get_all_records())
        AttendanceValidator.validate_record_count(count_attendance_records)        
        return self.attendance_repository.get_all_records()[-1]

    def get_last_5(self) -> Attendance:
        count_attendance_records = len(self.attendance_repository.get_all_records())
        AttendanceValidator.validate_record_count(count_attendance_records)
        
        if count_attendance_records < 5:
            return self.attendance_repository.get_all_records()[-count_attendance_records: ]
        
        return self.attendance_repository.get_all_records()[-5: ] 
    