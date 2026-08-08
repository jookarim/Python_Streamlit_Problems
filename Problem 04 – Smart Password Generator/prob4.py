import streamlit as st
import string
import random

#initialize password history list if not init yet
if 'password_history' not in st.session_state:
    st.session_state.password_history = []
    
#Title for the password generator app
st.title("Smart Password Generator")
st.divider()

#create 2 cols 1 for form and 1 for result
col1, col2 = st.columns([1,1])

def is_valid_password(password_len, uppercase, lowercase, digits, special_chars):
    """Check if password is valid of not Invalid if all cases are no"""
    if (uppercase == 'No' 
        and lowercase == 'No' 
        and digits == 'No' 
        and special_chars == 'No'):
        return False
    return True

def generate_password(password_len, uppercase, lowercase, digits, special_chars):
    """Generate password by adding all used cases inside password 
    and then choose random chars from the used data 
    to get random password each time"""
    
    password = ""
    used_data = ""
    
    #conditions to add cases to used_data
    if uppercase == 'Yes':
        used_data += string.ascii_uppercase
    if lowercase == 'Yes':
        used_data += string.ascii_lowercase
    if digits == 'Yes':
        used_data += string.digits
    if special_chars == 'Yes':
        used_data += string.punctuation
    
    #use random chars from used_data by random.choice
    for i in range(int(password_len)):
        password += random.choice(used_data)
    
    return password

def determine_strength(password_len):
    """Determine password strength by password length"""
    if password_len >= 4 and password_len <= 7:
        return 'Weak'
    elif password_len >= 8 and password_len <= 11:
        return 'Medium'
    else:
        return 'Strong'
    
def display_sidebar():
    with st.sidebar:
        #Display password tips
        st.header("Password Tips: ")
        st.info("Use at least 8 characters")
        st.info("Mix letters with digits")
        st.info("Include symbols")
        
        st.divider()
        
        #Display character groups that 
        # could be used in the generated password
        
        st.header("Character groups: ")
        st.info("Lowercase -> a to z")
        st.info("Uppercase -> A to Z")
        st.info("Digits -> 1 to 9")
        st.info("Special Characters: @#$ ...etc")    
        
def display_app():
    """Function to take data of password from user 
    and display generated password and all prev passwords"""
    
    #Display form in col1 (col1 for form and col2 for result display)
    with col1:
        with st.form(key="password_input"):
            password_len = st.slider("Password Length: ", 4, 32)
            uppercase = st.selectbox("Uppercase: ", ['Yes', 'No'])
            lowercase = st.selectbox("Lowercase: ", ['Yes', 'No'])
            digits = st.selectbox("Digits: ", ['Yes', 'No'])
            special_chars = st.selectbox("Special characters", ['Yes', 'No'])
            form_button = st.form_submit_button("Generate Password")
            
    #Result display in col2
    with col2:
        #Valid bool that checks if password is valid 
        #if valid generate result else display Invalid password
        valid = is_valid_password(password_len, uppercase, lowercase, digits, special_chars)
        
        #If form submit button pressed and password is valid
        if form_button and valid:            
            #generate password and determine its strength
            password = generate_password(password_len, uppercase, lowercase, digits, special_chars)
            password_strength = determine_strength(password_len)
            
            #append password in the history list
            st.session_state.password_history.append({
                "Password" : password,
                "Length" : int(password_len),
                "Strength" : password_strength
            })
            
            #Display generated password and password strength
            st.write(f"Generated Password: {password}")
            st.write(f"Strength: {password_strength}")
            st.success("Password generated successfully!")

        #If password is invalid Display error 
        elif form_button and not valid:
            st.error("Invalid password")

        #Display password history as table
        st.header('Password History')
        st.table(st.session_state.password_history)
    

#Call display sidehar and display app funcs
display_sidebar()
display_app()