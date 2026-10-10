from datetime import date

from repositories.student_repository import StudentRepository
from repositories.attendance_repository import AttendanceRepository 

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

for student in student_repository.get_all_students():
    print(f"{student.student_id} {student.student_name} {student.student_class}")
