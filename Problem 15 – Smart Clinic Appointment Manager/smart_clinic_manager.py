import streamlit as st
from datetime import date, datetime 
import time 

st.title('Clinic life management system', text_alignment='center')

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    'Book appointment',
    'View appointments',
    'Search appointment',
    'Cancel appointments',
    'Today schedule',
    'Statistics',
    'Recent appointment',
    'Weekly clinic dashboard' 
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
                        reason_visit,
                        appointment_date
                    ):
    
    return (
            len(patient_name) != 0 
            and len(appointment_time) != 0
            and len(reason_visit) != 0 
            and (
                appointment_date > date.today()
                or (
                    appointment_date == date.today()
                    and datetime.strptime(appointment_time, "%H:%M").time()
                        >= datetime.now().time()
                )
            )
    )
    
def schedule_overlapping(doctor, appointment_date, appointment_time):
    appointments_data = st.session_state.appointments_data
    
    for appointment in appointments_data:
        if (appointment['Doctor'] == doctor 
            and appointment['Appointment date'] == appointment_date 
            and appointment['Appointment time'] == appointment_time):
                return True 
    return False 

def display_appointment_summary(patient, doctor, date, time, reason, status):
    st.code(f"""
        ===================================
        Appointment Summary
        ===================================
        Patient: {patient}
        Doctor: Dr. {doctor}     
        Date: {date}
        Time: {time}
        Reason: {reason}
        Status: {status}
        ===================================
    """)    

def book_appointment():
    st.header('Book appointment', text_alignment='center')
    
    st.divider()
    
    with st.form(key='Book appointment'):
        patient_name = st.text_input('👤Patient name: ')
        doctor = st.selectbox('👨‍⚕️ Doctors: ', doctors)
        appointment_date = st.date_input("📅 Appointment date: ")
        appointment_time = st.text_input("🕐 Appointment time: ")
        reason_visit = st.text_input('Reason for visit❓')
        book_appointment = st.form_submit_button('Book appointment', type='primary')
    
    if book_appointment:
        valid_appointment = validate_appointment(patient_name, 
                                                appointment_time, 
                                                reason_visit,
                                                appointment_date)
        
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
    st.header('View appointments', text_alignment='center')
    
    st.divider()
    
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
            condition = (condition and
                        (appointment['Patient name'] == patient_name))
            
        if doctor_name != None:
            condition = (condition and 
                        (appointment['Doctor'] == doctor_name))
        
        if appointment_date != None:
            condition = (condition and 
                        (appointment['Appointment date'] == appointment_date))

        if condition:
            search_result.append(appointment)
    
    return search_result 

def search_patient():
    st.header('Search patient', text_alignment='center')
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    selected = set()
     
    with col1:
        st.subheader('Search categories')
        
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
            patient_name = st.text_input('👤 Patient name: ')
        if 'Doctor name' in selected:
            doctor_name = st.selectbox('👨‍⚕️ Doctor name: ', doctors)
        if 'Appointment date' in selected:
            appointment_date = st.date_input('📅 Appointment date')
        
        search_button = st.button('Search')
        
        if search_button:
            search_result = search_patient_helper(patient_name, 
                                                doctor_name, 
                                                appointment_date)
            
            if not search_result:
                st.warning('No results')
            else:
                st.table(search_result)

def cancel_appointment_helper(patient_name, 
                            doctor,
                            appointment_date, 
                            appointment_time):
    appointments_data = st.session_state.appointments_data
    
    for idx in range(len(appointments_data)):
        if (appointments_data[idx]['Patient name'] == patient_name
            and appointments_data[idx]['Doctor'] == doctor
            and appointments_data[idx]['Appointment date'] == appointment_date
            and appointments_data[idx]['Appointment time'] == appointment_time):
            
                return idx
    
    return -1 
        

def cancel_appointment():
    st.header('Cancel appointment', text_alignment='center')
    
    st.divider()
    
    with st.form(key='Cancel form'):
        patient_name = st.text_input('👤 Patient name: ')
        doctor = st.selectbox('👨‍⚕️ Doctor: ', doctors)
        appointment_date = st.date_input('📅 Appointment date: ')
        appointment_time = st.text_input('🕐 Appointment time: ')
        cancel_appointment_button = st.form_submit_button(
            ':red[Cancel appointment]', 
            type='secondary')
        
    cancel_appointment_idx = None 
    
    if cancel_appointment_button:
        cancel_appointment_idx = cancel_appointment_helper(
            patient_name, 
            doctor, 
            appointment_date,
            appointment_time)
        
        appointments_data = st.session_state.appointments_data 
        
        if cancel_appointment_idx == -1:
            st.warning('No appointment with these data')
        else:
            appointments_data[cancel_appointment_idx]['Status'] = 'Cancelled'
            
            with st.spinner('Cancelling appointment'):
                time.sleep(3)
            
            st.success('appointment cancelled successfully')
            time.sleep(2)
            st.rerun()
        
def display_today_schedule():
    st.header("Today's schedule",text_alignment='center')
    
    st.divider()
    
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
    st.header('Statistics', text_alignment='center')
    
    st.divider()
    
    appointments_data = st.session_state.appointments_data

    count_active = 0
    count_today_appointments = 0

    doctor_to_appointment = {}

    for idx in range(len(appointments_data)):
        doctor = appointments_data[idx]['Doctor']

        if appointments_data[idx]['Status'] == 'Scheduled':
            count_active += 1

        if appointments_data[idx]['Appointment date'] == date.today():
            count_today_appointments += 1

        if doctor not in doctor_to_appointment:
            doctor_to_appointment[doctor] = 1
        else:
            doctor_to_appointment[doctor] += 1

    col1, col2 = st.columns(2, border=True)

    with col1:
        st.write('Total active appointments:', count_active)
        st.write('Number of appointments today:', count_today_appointments)

    if doctor_to_appointment:
        max_appointments = max(doctor_to_appointment.values())

        max_name = ''

        for doctor, count_appointments in doctor_to_appointment.items():
            if count_appointments == max_appointments:
                max_name = doctor
                break

        with col2:
            st.subheader('Number of appointments for each doctor')
            st.table(doctor_to_appointment)
            st.write('Doctor with the most appointments:', max_name)

def weekly_clinic_dashboard():
    date_to_appointment = {}
    doctor_to_appointments = {}
    completeness_to_appointment = {}
    day_count_appointment = {}
    
    appointments_data = st.session_state.appointments_data

    for appointment in appointments_data:

        appointment_date = appointment['Appointment date']
        doctor = appointment['Doctor']

        appointment_data = {
            "Patient": appointment['Patient name'],
            "Doctor": appointment['Doctor'],
            "Time": appointment['Appointment time'],
            "Date": str(appointment['Appointment date']),
            "Reason": appointment['Reason visit'],
            "Status": appointment['Status']
        }
        
        if str(appointment_date) not in date_to_appointment:
            date_to_appointment[str(appointment_date)] = []

        date_to_appointment[str(appointment_date)].append(
            appointment_data
        )

        if doctor not in doctor_to_appointments:
            doctor_to_appointments[doctor] = []

        doctor_to_appointments[doctor].append(
            appointment_data
        )

        if appointment_date > date.today():
            status = "Upcoming"

        elif appointment_date == date.today():

            appointment_time = datetime.strptime(
                appointment['Appointment time'],
                "%H:%M"
            ).time()

            if appointment_time >= datetime.now().time():
                status = "Upcoming"
            else:
                status = "Completed"

        else:
            status = "Completed"

        if status not in completeness_to_appointment:
            completeness_to_appointment[status] = []

        completeness_to_appointment[status].append(
            appointment_data
        )
        
        if appointment_date.strftime("%A") not in day_count_appointment:
            day_count_appointment[appointment_date.strftime("%A")] = 0 
         
        day_count_appointment[appointment_date.strftime("%A")] += 1   
            
    for appointment_date, appointments in date_to_appointment.items():
        st.subheader(appointment_date)
        st.table(appointments)

    for doctor, appointments in doctor_to_appointments.items():
        st.subheader(doctor)
        st.table(appointments)

    for completeness, appointments in completeness_to_appointment.items():
        st.subheader(completeness)
        st.table(appointments)
    
    for day, count_appointments in day_count_appointment.items():
        st.subheader(f'{day}: {count_appointments}')
        
def get_recent_appointment_data():
    if not st.session_state.appointments_data:
        return (None, None, None, None, None, None)
    
    latest_appointment_data = st.session_state.appointments_data[0]
    
    return (
            latest_appointment_data['Patient name'],
            latest_appointment_data['Doctor'],
            latest_appointment_data['Appointment date'],
            latest_appointment_data['Appointment time'],
            latest_appointment_data['Reason visit'],
            latest_appointment_data['Status']
    )
            
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
    
with tab6:
    display_statistics()

with tab7:
    (patient_name,
    doctor,
    appointment_date,
    appointment_time, 
    reason,
    status) = get_recent_appointment_data()
    
    display_appointment_summary(
        patient_name, 
        doctor, 
        appointment_date, 
        appointment_time, 
        reason, 
        status
    )
    
with tab8:
    weekly_clinic_dashboard()