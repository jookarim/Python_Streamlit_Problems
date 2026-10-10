import pandas as pd 
from datetime import date

class AttendanceRepository:
    def __init__(self, csv_path: str):
        self.attendance_data = pd.read_csv(
            csv_path,
            dtype={
                'Student ID': 'string'
            },
            
            parse_dates=['Attendance date']
        )
        
        self.csv_path = csv_path 
        
    def record_attendance(  
                            self,
                            student_id: str,
                            attendance_date: date,
                            attendance_status: str):
        self.attendance_data.loc[len(self.attendance_data), [
            'Student ID', 'Attendance date', 'Attendance status'
        ]] = [
            student_id, pd.Timestamp(attendance_date), attendance_status
        ]
        
        self.attendance_data.to_csv(self.csv_path, index=False)
        
    def correct_attendance(
                            self,
                            student_id : str,
                            attendance_date : date,
                            new_status: str):
        mask = (
            (self.attendance_data['Student ID'] == student_id) &
            (self.attendance_data['Attendance date'] == pd.Timestamp(attendance_date))
        )

        self.attendance_data.loc[mask, 'Attendance status'] = new_status
        
        self.attendance_data.to_csv(self.csv_path, index=False)
    
        