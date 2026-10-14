import streamlit as st 
from services.student_service import StudentService 
from exceptions import student_exceptions 
from utils import student_utils

class StudentUI:
    def __init__(
        self,
        student_service: StudentService
    ):
        self.student_service = student_service
        
    def display_register_student(self):
        with st.form(key="Register student"): 
            student_id = st.text_input("Student ID: ")
            student_name = st.text_input("Student name: ")
            student_class = st.text_input("Class: ")
            add_student_button = st.form_submit_button("Register student")

        if add_student_button:
            try:
                self.student_service.register_student(
                    student_id,
                    student_name,
                    student_class
                )
                
            except student_exceptions.InvalidStudentDataException as e:
                st.error(str(e))
            except student_exceptions.DuplicateStudentException as e:
                st.warning(str(e))
            
            else:
                st.success('Student registered successfully')
                
    def display_search_student(self):
        with st.form(key="Search student"):
            student_id = st.selectbox("Student ID: ",
                                    student_utils.get_students_ids(self.student_service.get_all_students()))
            student_name = st.text_input("Student Name: ")
            student_class = st.text_input("Class: ")
            search_student = st.form_submit_button("Search student")

        if search_student:
            search_result = None 
            
            try:
                search_result = self.student_service.search_student(
                    student_id,
                    student_name,
                    student_class
                )
            
            except student_exceptions.EmptySearchResultException as e:
                st.warning('No result for these search data')
            
            else:
                st.dataframe(student_utils.generate_df_from_students(
                    search_result   
                ), hide_index=True)
                
                st.success('Search result appeared successfully')
    
    def view_students(self):
        students_data = self.student_service.get_all_students()
        
        if len(students_data):
            st.dataframe(student_utils.generate_df_from_students(
                students_data     
            ), hide_index=True)
        else:
            st.warning('There are no students yet')