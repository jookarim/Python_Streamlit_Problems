from repositories.student_repository import StudentRepository 
from repositories.attendance_repository import AttendanceRepository

from services.student_service import StudentService 
from services.attendance_service import AttendanceService 

from UI.student_ui import StudentUI 
from UI.attendance_ui import AttendanceUI 
from UI.app_ui import AppUI 

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

student_ui = StudentUI(
    student_service
)

attendance_ui = AttendanceUI(
    attendance_service
)

app_ui = AppUI(
    attendance_ui=attendance_ui,
    student_ui=student_ui
)

app_ui.display()