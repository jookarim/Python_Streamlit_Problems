from repositories.student_repository import StudentRepository

student_repository = StudentRepository(
    r"D:\Dev\Python_Streamlit_Problems\Problem 17 – Smart School Attendance Analytics Manager\app\data\students.csv"
)

student_repository.add_student(
    '1001',
    'Hello',
    'C1'
)

for student in student_repository.get_all_students():
    print(f"{student.student_id} {student.student_name} {student.student_class}")
