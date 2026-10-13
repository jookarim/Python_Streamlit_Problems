from models.attendance import Attendance 

import pandas as pd 

def generate_df_from_attendance(
    attendance_data: list[Attendance]
) -> pd.DataFrame:
     
    attendance_df = pd.DataFrame(columns=[
        'Student ID',
        'Attendance Date',
        'Attendance Status'
    ])
    
    for attendance in attendance_data:
        attendance_df.loc[len(attendance_df), [
            'Student ID',
            'Attendance Date',
            'Attendance Status'
        ]] = [attendance.student_id,
            attendance.attendance_date,
            attendance.attendance_status]
        
    
    return attendance_df 
