from UI.attendance_ui import AttendanceUI 
from UI.student_ui import StudentUI 
from UI.school_ui import SchoolUI
from UI.attendance_explorer_ui import AttendanceExplorerUI 
from UI.statistics_ui import StatisticsUI 
from UI.attendance_charts import AttendanceCharts 

import streamlit as st

from utils import student_utils

class AppUI:
    def __init__(
        self,
        attendance_ui: AttendanceUI,
        student_ui: StudentUI,
        school_ui: SchoolUI,
        attendance_explorer_ui: AttendanceExplorerUI,
        statistics_ui: StatisticsUI,
        attendance_charts: AttendanceCharts
    ):
        self.attendance_ui = attendance_ui 
        self.student_ui = student_ui
        self.school_ui = school_ui 
        self.attendance_explorer_ui = attendance_explorer_ui 
        self.statistics_ui = statistics_ui 
        self.attendance_charts = attendance_charts
          
        st.title('Smart school attendance analytics manager', text_alignment='center')
        
    def display(
        self,
        students_ids: list[str]
    ):
        (tab1,
        tab2,
        tab3,
        tab4,
        tab5,
        tab6,
        tab7,
        tab8,
        tab9,
        tab10,
        tab11,
        tab12,
        tab13) = st.tabs([
            'Register student',
            'Remove student',
            'Search student',
            'View students',
            'Record attendance',
            'Correct attendance',
            'View attendance records',
            'Explore attendance records',
            'View full attendance records',
            'Sort attendance records',
            'Statistics',
            'Charts',
            'Present vs absent'
        ])
        
        with tab1:
            self.student_ui.display_register_student()
        
        with tab2:
            self.school_ui.display_delete_student()
            
        with tab3:
            self.student_ui.display_search_student()
        
        with tab4:
            self.student_ui.view_students()
        
        with tab5:
            self.attendance_ui.display_record_attendance(
                student_utils.get_students_ids(
                    self.student_ui.student_service.get_all_students()
                )
            )

        with tab6:
            self.attendance_ui.display_correct_attendance(
                student_utils.get_students_ids(
                    self.student_ui.student_service.get_all_students()
                )
            )
        
        with tab7:
            self.attendance_ui.view_attendances()
        
        with tab8:
            self.attendance_explorer_ui.display_exploration_buttons()
        
        with tab9:
            self.school_ui.display_full_attendance_records()
        
        with tab10:
            self.attendance_ui.display_sort_attendance()  
        
        with tab11:
            self.statistics_ui.display()
            
        with tab12:
            self.attendance_charts.display_present_vs_absent()
        
        with tab13:
            self.attendance_charts.display_present_vs_absent_percent(
                students_ids
            )