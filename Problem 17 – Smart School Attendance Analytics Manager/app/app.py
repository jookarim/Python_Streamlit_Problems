from repositories.student_repository import StudentRepository 
from repositories.attendance_repository import AttendanceRepository

from services.student_service import StudentService 
from services.attendance_service import AttendanceService 
from services.school_service import SchoolService 

from UI.student_ui import StudentUI 
from UI.attendance_ui import AttendanceUI 
from UI.app_ui import AppUI 
from UI.school_ui import SchoolUI 

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
    student_service 
)

app_ui = AppUI(
    attendance_ui=attendance_ui,
    student_ui=student_ui,
    school_ui=school_ui
)

app_ui.display()