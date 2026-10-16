from services.attendance_service import AttendanceService 
from services.student_service import StudentService 

from utils import attendance_utils

import pandas as pd 

class StatisticsService:
    def __init__(
        self,
        attendance_service: AttendanceService
    ):
        self._attendance_service = attendance_service 
        self._attendance_records_df = (attendance_utils.generate_df_from_attendance(
            self._attendance_service.get_all_attendance_records()
        ))
        
    def _get_present_records_count(self) -> int:
        mask = self._attendance_records_df['Attendance Status'] == 'Present' 
        
        return len(
            self._attendance_records_df[mask]
        )
    
    def _get_total_attendance_records(self) -> int:
        return len(self._attendance_records_df)
        
    def _get_absent_records_count(self) -> int:
        return (self._get_total_attendance_records() - 
                self._get_present_records_count()
            )
    
    def _get_attendance_percentage(self) -> int:
        present_count = self._get_present_records_count()
        total_records = self._get_total_attendance_records()
        return (present_count / total_records) * 100 
    
    def get_data_table_form(self) -> None:
        statistics_df = pd.DataFrame(columns=[
            'Attribute',
            'Statistics'
        ])
        
        total_records = self._get_total_attendance_records()
        present_count = self._get_present_records_count()
        absent_count = self._get_absent_records_count()
        attendance_percent = self._get_attendance_percentage()
        
        statistics_df['Attribute'] = [
            'Total records',
            'Present records',
            'Absent records',
            'Attendance percent'
        ]
        
        statistics_df['Statistics'] = [
            total_records,
            present_count,
            absent_count,
            f"{attendance_percent:.2f}%"
        ]
        
        return statistics_df 