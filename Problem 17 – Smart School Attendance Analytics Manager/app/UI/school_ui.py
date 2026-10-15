from services.school_service import SchoolService
from services.student_service import StudentService 
from services.attendance_service import AttendanceService 

from exceptions import student_exceptions 
from utils import student_utils 
from utils import school_utils 

import streamlit as st 

class SchoolUI:
    def __init__(
        self,
        school_service: SchoolService,
        student_service: StudentService,
        attendance_service: AttendanceService
    ) -> None:
        self.school_service = school_service
        self.student_service = student_service 
        self.attendance_service = attendance_service 
                
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
        
    def display_full_attendance_records(self):
        attendances_df = school_utils.generate_df_from_attendance_data(
                            self.student_service,
                            self.attendance_service.get_all_attendance_records()
                        )
        
        if not len(attendances_df):
            st.warning('No attendance records yet')
            
        else:
            st.dataframe(
                attendances_df,
                hide_index=True
            )