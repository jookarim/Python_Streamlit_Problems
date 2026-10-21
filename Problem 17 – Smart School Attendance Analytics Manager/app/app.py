from repositories.student_repository import StudentRepository 
from repositories.attendance_repository import AttendanceRepository

from services.student_service import StudentService 
from services.attendance_service import AttendanceService 
from services.school_service import SchoolService 
from services.attendance_explorer_service import AttendanceExplorer 
from services.statistics_service import StatisticsService 

from UI.student_ui import StudentUI 
from UI.attendance_ui import AttendanceUI 
from UI.app_ui import AppUI 
from UI.school_ui import SchoolUI 
from UI.attendance_explorer_ui import AttendanceExplorerUI 
from UI.statistics_ui import StatisticsUI 
from UI.attendance_charts import AttendanceCharts 

student_repository = StudentRepository(
    'app/data/students.csv'
)

attendance_repository = AttendanceRepository(
    'app/data/attendance.csv'
)

student_service = StudentService(
    student_repository     
)

attendance_service = AttendanceService(
    attendance_repository
)

school_service = SchoolService(
    student_repository,
    attendance_repository
)

student_ui = StudentUI(
    student_service
)

attendance_ui = AttendanceUI(
    attendance_service
)

school_ui = SchoolUI(
    school_service,
    student_service,
    attendance_service
)

attendance_explorer_service = AttendanceExplorer(
    attendance_repository
)

attendance_explorer_ui = AttendanceExplorerUI(
    attendance_explorer_service
)

statistics_service = StatisticsService(
    attendance_service 
)

statistics_ui = StatisticsUI(
    statistics_service,
    student_service 
)

attendance_charts = AttendanceCharts(
    statistics_service
)

app_ui = AppUI(
    attendance_ui=attendance_ui,
    student_ui=student_ui,
    school_ui=school_ui,
    attendance_explorer_ui=attendance_explorer_ui,
    statistics_ui=statistics_ui,
    attendance_charts=attendance_charts
)

app_ui.display(
    student_service.get_all_students_ids()
)