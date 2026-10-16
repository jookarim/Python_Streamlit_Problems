import streamlit as st 
import random 

#Title for application to make the user know what is the app about
st.title('BlazeX Email Creator')

#Department to its code to gen code in the email from department
departments_codes = {
    'Technology' : 'dev',
    'Marketing' : 'mkt',
    'Operation' : 'op',
    'Finance' : 'fin',
    'Sales' : 'sl',
    'Human Resources' : 'hr'
}

def validate_data(
    first_name,
    last_name,
    phone_number
) -> bool:
    """Function that validates user data
    Returns true if valid else false"""
    
    return (
        (len(first_name) > 0 and len(first_name) <= 12)
        and (len(last_name) > 0 and len(last_name) <= 12)
        and (len(phone_number) == 11)
    )

def generate_email(
    first_name,
    last_name,
    phone_number,
    department
):
    """Function that takes user data and generates email from it"""
    
    #Generate 2 random digits each one from 0 to 9
    first_random_digit = random.randint(0, 9)
    second_random_digit = random.randint(0, 9)
    
    #Generate the email
    #use rounded brackets because it concatinates strings
    
    email = (
        f"{first_name}.{last_name}."
        f"{departments_codes[department]}."
        f"{phone_number[-2:]}."
        f"{first_random_digit}"
        f"{second_random_digit}"
        "@BlazeX.com"
    )
    
    return email 
            
def display_ui():
    """Function to gets user data, validate them and display"""
    
    #2 columns for entering user data in a clean way
    col1, col2 = st.columns(2)
    
    #Enter first,last names in the first column
    with col1:
        first_name = st.text_input('Enter your first name: ')
        last_name = st.text_input('Enter your last name: ')
    
    #Enter phone number, department in the second column
    with col2:
        phone_number = st.text_input('Enter your phone number: ')
        department = st.selectbox(
            'Choose your department: ',
            departments_codes.keys()
        )
    
    #Button to generate business email
    generate_email_button = st.button('Generate Business Email')
    
    #Make actions if button pression
    if generate_email_button:
        
        #Validate data after button press
        valid_data = validate_data(
            first_name,
            last_name,
            phone_number
        )
        
        if valid_data:
            #Displayes success message and email if the data are valid
            
            st.success('Business email generated successfully!')
            
            st.header('Your business Email: ')
            
            email = generate_email(
                first_name,
                last_name,
                phone_number,
                department
            )
            
            st.code(email)
        
        #Displayes error message if data are invalid
        else:
            st.error('Data is invalid. Please enter valid data')
            
display_ui()