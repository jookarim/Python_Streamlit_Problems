from services.statistics_service import StatisticsService 
from services.student_service import StudentService 

import streamlit as st 

class StatisticsUI:
    def __init__(
        self,
        statistics_service: StatisticsService,
        student_service: StudentService
    ) -> None:
        self.statistics_service = statistics_service 
        self.student_service = student_service 
        
    def display(self):
        statistics_table = self.statistics_service.get_data_table_form()
        class_attendance_table = self.statistics_service.get_attendance_by_class(
            self.student_service
        )
        
        st.dataframe(statistics_table, hide_index=True)
        st.dataframe(class_attendance_table, hide_index=True)