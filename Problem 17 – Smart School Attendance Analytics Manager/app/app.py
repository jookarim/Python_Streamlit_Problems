from repositories.student_repository import StudentRepository 
from services.student_service import StudentService 
from UI.student_ui import StudentUI 

import pandas as pd 
import streamlit as st 

student_repository = StudentRepository(
    'app/data/students.csv'
)

student_service = StudentService(
    student_repository     
)

student_ui = StudentUI(
    student_service
)

student_ui.display()