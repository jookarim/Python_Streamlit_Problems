import streamlit as st 
import random 

#Title to make the user know what the app is about
st.title('🎓 NileTech Student Email 🎓')
st.divider()

#Map faculty to code to be used when generating email
faculty_to_code = {
    'Engineering' : 'eng',
    'Medicine' : 'med',
    'Business' : 'bus',
    'Computer Science' : 'cs',
    'Arts' : 'art',
    'Law' : 'law'
}

def validate_data(
    first_name, 
    last_name,
    national_id
):
    """Checks if the user data is valid"""
    
    return bool(first_name and 
                last_name and 
                national_id)

def generate_email(
    first_name,
    last_name,
    national_id,
    faculty
):
    """Function that takes user data and generates email"""
    
    random_digit_1 = random.randint(0, 9)
    random_digit_2 = random.randint(0, 9)
    faculty_code = faculty_to_code[faculty]
    
    email = f"""
        {first_name[0]}.
        {last_name}.
        {faculty_code}.
        {national_id[-3:]}.
        {random_digit_1}
        {random_digit_2}
        @NileTech.edu
    """
    
    #Removes all new lines and spaces
    email = ''.join(email.split())
    
    return email 

def display_app_ui():
    """Function that gets data from user and displayes output"""
    
    col1, col2 = st.columns(2)
    
    #Get user first name and national ID from first col
    
    with col1:
        first_name = st.text_input(
            'Enter your first name: ',
            icon='👦'
        )
        
        national_id = st.text_input(
            'Enter your national ID: ',
            icon='🪪'
        )
    
    #Get lastname and faculty from the second col (col2)
    with col2:
        last_name = st.text_input(
            'Enter your last name: ',
            icon='👦'
        )
        
        faculty = st.selectbox(
            'Choose your faculty: ',
            faculty_to_code.keys()   
        )

    #Button for email generation    
    generate_email_button = st.button(
        '🎓 Generate Student Email'
    )
    
    #Detects if the button is pressed
    
    if generate_email_button:
        #Check if user data is valid
        is_valid = validate_data(
            first_name,
            last_name,
            national_id 
        )
        
        #If data are valid display success message + email
        if is_valid:
            st.success(
                'Student email generated successfully!'
            )
            
            st.header('📧 Your Student Email: ')
            
            generated_email = generate_email(
                first_name,
                last_name,
                national_id,
                faculty
            )
            
            st.code(generated_email)
        
        #Display error if invalid
        else:
            st.error('Invalid data. Please try again')
            
display_app_ui()