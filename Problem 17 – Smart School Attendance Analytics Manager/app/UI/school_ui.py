from services.school_service import SchoolService
from services.student_service import StudentService 

from exceptions import student_exceptions 
from utils import student_utils 

import streamlit as st 

class SchoolUI:
    def __init__(
        self,
        school_service: SchoolService,
        student_service: StudentService 
    ) -> None:
        self.school_service = school_service
        self.student_service = student_service 
        
    def display_delete_student(
        self
    ):
        
        student_id = st.selectbox('Student ID: ', 
                                student_utils.get_students_ids(self.student_service.get_all_students()))
        delete_student_button = st.button('Delete student')
        
        if delete_student_button:
            try:
                self.school_service.delete_student(student_id)
            
            except student_exceptions.InvalidStudentIDException as e:
                st.error(e)
                
            except student_exceptions.StudentNotFoundException as e:
                st.warning(str(e))

            else: 
                st.success('Student deleted successfully') 
        

