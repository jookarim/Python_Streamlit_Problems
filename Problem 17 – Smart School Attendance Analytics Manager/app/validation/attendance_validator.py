from exceptions import attendance_exceptions 

class AttendanceValidator:
    @staticmethod
    def validate_record_count(count_records: int) -> None:
        if count_records <= 0:
            raise attendance_exceptions.NoRecordException("Record count is invalid")