from services.attendance_service import AttendanceService 
from utils import attendance_utils 
from exceptions import attendance_exceptions 

import streamlit as st 

class AttendanceUI:
    def __init__(
        self,
        attendance_service: AttendanceService
    ):
        self.attendance_service = attendance_service 
        
    def display_record_attendance(
        self, 
        students_ids: list[str]
    ):
        with st.form(key="Record attendance"):
            student_id = st.selectbox('Student: ', students_ids)
            attendance_date = st.date_input('Attendance date: ')
            attendance_status = st.selectbox('Attendance status: ', [
                'Present',
                'Absent'
            ])
            
            record_attendance_button = st.form_submit_button('Record attendance')
        
        if record_attendance_button:
            try:
                self.attendance_service.record_attendance(
                    student_id,
                    attendance_date,
                    attendance_status
                )
            
            except attendance_exceptions.InvalidAttendanceDataException as e:
                st.error(str(e))            
            except attendance_exceptions.AttendanceAlreadyRecordedException as e:
                st.warning(str(e))
            else:
                st.success('Attendance corrected successfully')
                            
    def display_correct_attendance(
        self,
        students_ids: list[str]
    ):
        with st.form(key="Correct attendance"):
            student_id = st.selectbox('Student ID: ', students_ids)
            attendance_date = st.date_input("Attendance Date: ")
            new_status = st.selectbox("New status: ", [
                'Present',
                'Absent'
            ])
            
            correct_attendance_button = st.form_submit_button('Correct attendance')
        
        if correct_attendance_button:
            try:
                self.attendance_service.correct_attendance(
                    student_id,
                    attendance_date,
                    new_status 
                )
            except attendance_exceptions.InvalidAttendanceDataException as e:
                st.error(str(e))
            except attendance_exceptions.AttendanceNotRecordedException as e:
                st.warning(str(e))
            else:
                st.success('Attendance corrected successfully')
                
    def view_attendances(self):
        attendances_records = self.attendance_service.get_all_attendance_records()
        
        if len(attendances_records):
            st.dataframe(attendance_utils.generate_df_from_attendance(
                attendances_records
            ), hide_index=True)
        
        else:
            st.warning('No attendance records yet')