from services.attendance_service import AttendanceService 
from services.student_service import StudentService 

from exceptions import attendance_exceptions 

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
        
    def get_present_records_count(self) -> int:
        mask = self._attendance_records_df['Attendance Status'] == 'Present' 
        
        return len(
            self._attendance_records_df[mask]
        )
    
    def _get_total_attendance_records(self) -> int:
        return len(self._attendance_records_df)
        
    def get_absent_records_count(self) -> int:
        return (self._get_total_attendance_records() - 
                self.get_present_records_count()
            )
    
    def _get_attendance_percentage(self) -> int:
        present_count = self.get_present_records_count()
        total_records = self._get_total_attendance_records()
        return (present_count / total_records) * 100 
    
    def get_data_table_form(self) -> pd.DataFrame:
        statistics_df = pd.DataFrame(columns=[
            'Attribute',
            'Statistics'
        ])
        
        total_records = self._get_total_attendance_records()
        present_count = self.get_present_records_count()
        absent_count = self.get_absent_records_count()
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

    def get_attendance_by_class(
        self,
        student_service: StudentService 
    ) -> pd.DataFrame:
        class_to_attendance = {
            
        }
        
        class_to_attendance_df = pd.DataFrame(
            columns=['Class', 'Present', 'Total']
        )
        
        for _, row in self._attendance_records_df.iterrows():
            student_id = row['Student ID']
            student_class = student_service.get_name_class_from_id(
                student_id
            )[1]
            
            if student_class not in class_to_attendance:
                class_to_attendance[student_class] = [0,0]
            
            class_to_attendance[student_class][0] += 1
            
            if row['Attendance Status'] == 'Present': 
                class_to_attendance[student_class][1] += 1 
                
        for student_class, (total, present) in class_to_attendance.items():
            class_to_attendance_df.loc[len(class_to_attendance_df)] = [
                student_class,
                present,
                total 
            ]
        
        return class_to_attendance_df.copy()
    
    def get_present_absent_percent(
        self,
        student_id: str
    ) -> tuple[int, int]:
        count_records_student = self._attendance_records_df[
            self._attendance_records_df['Student ID'] == student_id 
        ].size 
        
        count_present_records = self._attendance_records_df[
            (self._attendance_records_df['Student ID'] == student_id) & 
            (self._attendance_records_df['Attendance Status'] == 'Present')
        ].size
        
        if count_records_student == 0:
            raise attendance_exceptions.StudentIsNotFoundException(
                "Student does not have attendance records"
            )
            
        percent_present = (count_present_records / count_records_student) * 100 
        percent_absent = 100 - percent_present 
        
        return (percent_present, percent_absent)
    
        