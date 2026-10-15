from services.attendance_explorer_service import AttendanceExplorer 
from exceptions import attendance_exceptions
from utils import attendance_utils 

import streamlit as st 

class AttendanceExplorerUI:
    def __init__(
        self,
        attendance_explorer: AttendanceExplorer
    ):
        self.attendance_explorer = attendance_explorer 
    
    def display_first_attendance(self):
        first_record_button = st.button('First attendance record')
        
        if first_record_button:
            try:
                first_record = self.attendance_explorer.get_first_record()
            except attendance_exceptions.NoAttendanceRecordsException as e:
                st.warning(str(e))
            else:
                first_record_df = attendance_utils.generate_df_from_attendance(
                    [first_record]
                )
                
                st.dataframe(
                    first_record_df, 
                    hide_index=True
                )
                
    def display_last_attendance(self):
        last_record_button = st.button('Last attendance record')
                
        if last_record_button:
            try:
                last_record = self.attendance_explorer.get_last_record()
            except attendance_exceptions.NoAttendanceRecordsException as e:
                st.warning(str(e))
            else:
                last_record_df = attendance_utils.generate_df_from_attendance(
                    [last_record]
                )

                st.dataframe(
                    last_record_df, 
                    hide_index=True
                )
                
    def display_recent_attendance_records(self):
        recent_attendance_records = st.button('Recent attendance records')
        
        if recent_attendance_records:
            try:
                recent_records = self.attendance_explorer.get_recent_records()
            except attendance_exceptions.NoAttendanceRecordsException as e:
                st.warning(str(e))
            else:
                recent_records_df = attendance_utils.generate_df_from_attendance(
                    recent_records
                )
                
                st.dataframe(
                    recent_records_df, 
                    hide_index=True
                )
    
    def display_exploration_buttons(self):
        self.display_first_attendance()
        self.display_last_attendance()
        self.display_recent_attendance_records()