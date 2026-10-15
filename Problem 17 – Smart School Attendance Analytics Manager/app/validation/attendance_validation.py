from exceptions import attendance_exceptions
from models.attendance import Attendance 

from datetime import date


class AttendanceValidation:
    @staticmethod
    def validate_attendance_data(
        student_id: str,
        attendance_date: date
    ) -> None:
        if not (student_id and attendance_date <= date.today()):
            raise attendance_exceptions.InvalidAttendanceDataException(
                "Invalid attendance data"
            )

    @staticmethod
    def validate_attendance_already_recorded(
        student_id: str,
        already_recorded: bool
    ) -> None:
        if already_recorded:
            raise attendance_exceptions.AttendanceAlreadyRecordedException(
                f"Attendance already recorded for student: {student_id}"
            )

    @staticmethod
    def validate_attendance_not_recorded(
        student_id: str,
        already_recorded: bool
    ) -> None:
        if not already_recorded:
            raise attendance_exceptions.AttendanceNotRecordedException(
                f"Attendance not recorded for this student: {student_id}"
            )
            
    @staticmethod 
    def validate_found_attendance_records(
        attendance_records: list[Attendance]
    ):
        if not len(attendance_records):
            raise attendance_exceptions.NoAttendanceRecordsException(
                "There are no attendance records"
            )