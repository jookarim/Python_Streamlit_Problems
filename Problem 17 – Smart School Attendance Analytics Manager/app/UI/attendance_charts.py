
from services.statistics_service import StatisticsService

from exceptions import attendance_exceptions 

import matplotlib.pyplot as plt
import streamlit as st


class AttendanceCharts:
    def __init__(
        self,
        statistics_service: StatisticsService,
    ):
        self.statistics_service = statistics_service

    def display_present_vs_absent(self) -> None:
        count_present = self.statistics_service.get_present_records_count()
        count_absent = self.statistics_service.get_absent_records_count()

        fig, ax = plt.subplots(
            nrows=1, ncols=1
        )

        ax.barh(
            y=[
                'Present',
                'Absent'
            ],
            width=[count_present, count_absent]
        )

        ax.set_xlabel('Number of Records')
        ax.set_title('Present vs Absent Attendance')

        st.pyplot(fig)
        plt.close(fig)
    
    def display_present_vs_absent_percent(
        self,
        students_ids: list[str]
    ) -> None:
        fig, ax = plt.subplots(
            nrows=1, 
            ncols=1
        )
        
        student_id = st.selectbox('Student ID: ', students_ids, key='Student ID for chart')
        
        result_button = st.button('Result')
        
        if result_button:
            try:
                (
                    present_percent, 
                    absent_percent
                ) = self.statistics_service.get_present_absent_percent(
                    student_id
                )
                
            except attendance_exceptions.StudentIsNotFoundException as e:
                st.warning(str(e))
            
            else:
                ax.pie([present_percent, 
                        absent_percent], labels=[
                    'Present percent',
                    'Absent percent'
                ],colors=['green', 'red'], autopct='%1.1f%%')
                
                st.pyplot(fig)
                
            finally:
                plt.close()
        