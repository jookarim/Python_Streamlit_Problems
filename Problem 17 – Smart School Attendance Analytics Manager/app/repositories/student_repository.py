from models.student import Student 
import pandas as pd 

class StudentRepository:
    def __init__(
        self,       
        csv_path: str
    ) -> None:
        self.csv_path = csv_path 
        self.students_df = pd.read_csv(
            csv_path,
            dtype=str
        )
        
    
    def add_student(
        self,
        student_id: str,
        student_name: str,
        student_class: str
    ) -> None:
        self.students_df.loc[len(self.students_df), [
            'Student ID',
            'Student Name', 
            'Student Class'
        ]] = [
            student_id,
            student_name, 
            student_class
        ]
        
        self.students_df.to_csv(self.csv_path, index=False)
        
    def get_all_students(self) -> list[Student]:
        return [
            Student(
                row['Student ID'],
                row['Student Name'],
                row['Student Class']
            )
            
            for _, row in self.students_df.iterrows()
        ]        
        
    def delete_student(
        self,
        student_id: str
    ) -> None:
        self.students_df = self.students_df[
            self.students_df['Student ID'] != student_id
        ]
        
        self.students_df.to_csv(self.csv_path, index=False)
    
    def get_students_by(
        self,
        student_id: str,
        student_name: str,
        student_class: str
    ) -> list[Student]:
        
        mask = pd.Series(True, index=self.students_df.index)
        
        if student_id:
            mask &= (
                self.students_df['Student ID'] == student_id
            )
        
        if student_name:
            mask &= (
                self.students_df['Student Name'] == student_name
            )
        
        if student_class:
            mask &= (
                self.students_df['Student Class'] == student_class
            )

        return [
            Student(
                row['Student ID'],
                row['Student Name'],
                row['Student Class']
            )
            
            for _, row in self.students_df[mask].iterrows()
        ]

    def check_id_found(
        self,
        student_id: str
    ) -> bool:
        return (self.students_df['Student ID'] == student_id).any()