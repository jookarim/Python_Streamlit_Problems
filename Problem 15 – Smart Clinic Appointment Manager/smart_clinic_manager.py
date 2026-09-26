import streamlit as st
from datetime import date
import time 

st.title('Clinic life management system', text_alignment='center')

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    'Book appointment',
    'View appointments',
    'Search appointment',
    'Cancel appointments',
    'Today schedule'    
])

if 'appointments_data' not in st.session_state:
    st.session_state.appointments_data = []

doctors = [
    'Youssef',
    'Hana',
    'Karim'
]    

def display_sidebar():
    with st.sidebar:
        st.write('**Clinic name: Clinic Life**')
        st.write(f'**Today date: {date.today()}**')
        st.write(f'**Location: Street 1**')
        st.write(f'**Started since 2013**')
        
def validate_appointment(
                        patient_name,
                        appointment_time, 
                        reason_visit
                    ):
    
    return (
            len(patient_name) != 0 
            and len(appointment_time) != 0
            and len(reason_visit) != 0 
    )
    
def schedule_overlapping(doctor, appointment_date, appointment_time):
    appointments_data = st.session_state.appointments_data
    
    for appointment in appointments_data:
        if (appointment['Doctor'] == doctor 
            and appointment['Appointment date'] == appointment_date 
            and appointment['Appointment time'] == appointment_time):
                return True 
    return False 
            
def book_appointment():
    with st.form(key='Book appointment'):
        patient_name = st.text_input('Patient name: ')
        doctor = st.selectbox('Doctors: ', doctors)
        appointment_date = st.date_input("Appointment date: ")
        appointment_time = st.text_input("Appointment time: ")
        reason_visit = st.text_input('Reason for visit')
        book_appointment = st.form_submit_button('Book appointment')
    
    if book_appointment:
        valid_appointment = validate_appointment(patient_name, 
                                                appointment_time, 
                                                reason_visit)
        
        schedule_overlap = schedule_overlapping(doctor, 
                                                appointment_date, 
                                                appointment_time)
        
        if valid_appointment and not schedule_overlap:
            appointment_record = {
                'Patient name' : patient_name,
                'Doctor' : doctor,
                'Appointment date' : appointment_date,
                'Appointment time' : appointment_time,
                'Reason visit' : reason_visit,
                'Status' : 'Scheduled'
            }
            
            st.session_state.appointments_data.append(appointment_record)
            
            with st.spinner('Booking appointment'):
                time.sleep(3)
            
            st.success('Appointment booked successfully')
            
        elif not valid_appointment:
            st.error('Invalid appointment')
        else:
            st.warning('Schadule overlapping')

def view_appointments():
    if not st.session_state.appointments_data:
        st.info('No appointments booked yet')
    else:
        st.table(st.session_state.appointments_data)

def search_patient_helper(patient_name=None, doctor_name=None, appointment_date=None):
    appointments_data = st.session_state.appointments_data
    
    search_result = []
    
    for appointment in appointments_data:
        condition = True
        
        if patient_name != None:
            condition = condition and (appointment['Patient name'] == patient_name)
        if doctor_name != None:
            condition = condition and (appointment['Doctor'] == doctor_name)
        if appointment_date != None:
            condition = condition and (appointment['Appointment date'] == appointment_date)

        if condition:
            search_result.append(appointment)
    
    return search_result 

def search_patient():
    st.subheader('Search categories')
    
    col1, col2 = st.columns(2)
    
    selected = set()
     
    with col1:
        search_categories = [
            'Patient name',
            'Doctor name',
            'Appointment date'
        ]
    
        for category in search_categories:
            if st.checkbox(category):
                selected.add(category)
    
    with col2:
        patient_name = None
        doctor_name = None
        appointment_date = None
        
        if 'Patient name' in selected:
            patient_name = st.text_input('Patient name: ')
        if 'Doctor name' in selected:
            doctor_name = st.selectbox('Doctor name: ', doctors)
        if 'Appointment date' in selected:
            appointment_date = st.date_input('Appointment date')
        
        search_button = st.button('Search')
        
        if search_button:
            search_result = search_patient_helper(patient_name, doctor_name, appointment_date)
            
            if not search_result:
                st.warning('No results')
            else:
                st.table(search_result)

def cancel_appointment_helper(patient_name, doctor, appointment_date, appointment_time):
    appointments_data = st.session_state.appointments_data
    
    for idx in range(len(appointments_data)):
        if (appointments_data[idx]['Patient name'] == patient_name
            and appointments_data[idx]['Doctor'] == doctor
            and appointments_data[idx]['Appointment date'] == appointment_date
            and appointments_data[idx]['Appointment time'] == appointment_time):
                appointments_data[idx]['Status'] = 'Cancelled'
            
                return idx
    
    return -1 
        

def cancel_appointment():
    with st.form(key='Cancel form'):
        patient_name = st.text_input('Patient name: ')
        doctor = st.selectbox('Doctor: ', doctors)
        appointment_date = st.date_input('Appointment date: ')
        appointment_time = st.text_input('Appointment time: ')
        cancel_appointment_button = st.form_submit_button('Cancel appointment')
        
    cancel_appointment_idx = None 
    
    if cancel_appointment_button:
        cancel_appointment_idx = cancel_appointment_helper(patient_name, doctor, appointment_date, appointment_time)
        
        if cancel_appointment_idx == -1:
            st.warning('No appointment with these data')
        else:
            st.session_state.appointments_data[cancel_appointment_idx]['Status'] = 'Cancelled'
            
            with st.spinner('Cancelling appointment'):
                time.sleep(3)
            
            st.success('appointment cancelled successfully')
            time.sleep(2)
            st.rerun()
        
def display_today_schedule():
    today_appoinments = []
    appointments_data = st.session_state.appointments_data 
    
    for appointment in appointments_data:
        today_date = date.today()
        if (appointment['Appointment date'] == today_date 
            and appointment['Status'] == 'Scheduled'):
            today_appoinments.append(appointment)
    
    if not len(today_appoinments):
        st.info('There are no appointments today')
    else:
        st.table(today_appoinments)

def display_statistics():
    pass 

display_sidebar()

with tab1:
    book_appointment()

with tab2:
    view_appointments()
    
with tab3:
    search_patient()
    
with tab4:
    cancel_appointment()
    
with tab5:
    display_today_schedule()