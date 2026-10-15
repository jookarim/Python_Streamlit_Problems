from models.student import Student 
from models.attendance import Attendance 

from services.student_service import StudentService 

import pandas as pd 

def generate_df_from_attendance_data(
    student_service: StudentService,  
    attendance_records: list[Attendance]
) -> pd.DataFrame:
    attendances_df = pd.DataFrame(
        columns=[
            'Student ID',
            'Student Name',
            'Class',
            'Date',
            'Status'
        ]
    )
    
    for record in attendance_records:
        (
            student_name,
            student_class
        ) = student_service.get_name_class_from_id(
            record.student_id
        )

        attendances_df.loc[len(attendances_df)] = [
                        record.student_id,
                        student_name,
                        student_class,
                        record.attendance_date,
                        record.attendance_status
                    ]
    
    return attendances_df 
    
    