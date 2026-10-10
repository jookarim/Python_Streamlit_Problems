from datetime import date

from repositories.student_repository import StudentRepository
from repositories.attendance_repository import AttendanceRepository 

from services.attendance_explorer import AttendanceExplorer 

import exceptions.products_exceptions as products_exceptions

student_repository = StudentRepository(
    r"data\students.csv"
)

student_repository.add_student(
    '1001',
    'Hello',
    'C1'
)

attendance_repo = AttendanceRepository(r"data\attendance.csv")
attendance_repo.record_attendance(
    '1001',
    date(2026, 5, 10),
    'Present'
)

attendance_explorer = AttendanceExplorer(attendance_repo)

try:
    print(attendance_explorer.get_first_record())
except products_exceptions.NoProductsException as e:
    print(str(e))
else:
    print("Got the first product")
    
for student in student_repository.get_all_students():
    print(f"{student.student_id} {student.student_name} {student.student_class}")
