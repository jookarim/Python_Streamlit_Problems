
from models.student import Student
import pandas as pd


class StudentRepository:
    def __init__(self, csv_path: str) -> None:
        """read the csv file of students"""
        self.csv_path = csv_path
        self.students = pd.read_csv(csv_path)

    def add_student(
        self,
        student_id: str,
        student_name: str,
        student_class: str
    ) -> None:
        """Add student at the end of the students df"""
        
        self.students.loc[len(self.students)] = [
            student_id,
            student_name,
            student_class
        ]

        self.students.to_csv(self.csv_path, index=False)

    def remove_student(self, student_id: str) -> None:
        """Remove student by id"""
        
        student_index = self.students[
            self.students['Student ID'] == student_id
        ].index

        self.students.drop(student_index, inplace=True)

        self.students.to_csv(self.csv_path, index=False)

    def get_all_students(self) -> list[Student]:
        """Get all students as shape of list of Student"""
        
        #Use loop for conversion from pandas df to list[Student]
        return [
            Student(
                row['Student ID'],
                row['Student Name'],
                row['Class']
            )
            for _, row in self.students.iterrows()
        ]

    def search_student_by(
        self,
        student_id: str,
        student_name: str,
        student_class: str
    ) -> list[Student]:
        """Search student by categories"""

        #Use masking to get specific df from available search categories
                
        mask = pd.Series(True, index=self.students.index)

        if student_id:
            mask &= self.students['Student ID'] == student_id

        if student_name:
            mask &= self.students['Student Name'] == student_name

        if student_class:
            mask &= self.students['Class'] == student_class

        search_result = self.students[mask]

        #Use loop for conversion from pandas df to list[Student]
        return [
            Student(
                row['Student ID'],
                row['Student Name'],
                row['Class']
            )
            for _, row in search_result.iterrows()
        ]
