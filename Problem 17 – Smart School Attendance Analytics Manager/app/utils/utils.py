from models.student import Student 
import pandas as pd 

def generate_df_from_students(
    students_data: list[Student]
) -> pd.DataFrame:
    
    df = pd.DataFrame(columns=[
        'Student ID',
        'Student Name',
        'Class'
    ])
    
    for student in students_data:
        df.loc[len(df), [
            'Student ID',
            'Student Name',
            'Class'
        ]] = [
            student.student_id,
            student.student_name,
            student.student_class
        ]
    
    return df 
