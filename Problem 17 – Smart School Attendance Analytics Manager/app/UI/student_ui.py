import streamlit as st 
from services.student_service import StudentService 
from exceptions import student_exceptions 
from utils import utils

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
    
    def display_delete_student(self):
        student_id = st.text_input('Student ID: ')
        delete_student_button = st.button('Delete student')
        
        if delete_student_button:
            try:
                self.student_service.remove_student(student_id)
            
            except student_exceptions.InvalidStudentIDException as e:
                st.error(e)
                
            except student_exceptions.StudentNotFoundException as e:
                st.warning(str(e))

            else:
                st.success('Student deleted successfully')
                
    def display_search_student(self):
        with st.form(key="Search student"):
            student_id = st.text_input("Student ID: ")
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
                st.dataframe(utils.generate_df_from_students(
                    search_result   
                ))
                
                st.success('Search result appeared successfully')
    
    def view_students(self):
        students_data = self.student_service.get_all_students()
        st.dataframe(utils.generate_df_from_students(
            students_data     
        ), hide_index=True)
        
    def display(self):
        tab1,tab2,tab3,tab4 = st.tabs([
            'Register student',
            'Remove student',
            'Search student',
            'View students'
        ])
        
        with tab1:
            self.display_register_student()
            
        with tab2:
            self.display_delete_student()
            
        with tab3:
            self.display_search_student()
        
        with tab4:
            self.view_students()