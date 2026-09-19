
import streamlit as st

st.title("Password Strength Recognizer")

tab1, tab2, tab3 = st.tabs([
    "Password Entering",
    "Invalid Password",
    "Passwords Table"
])

if "invalid_passwords" not in st.session_state:
    st.session_state.invalid_passwords = []

if 'passwords_table' not in st.session_state:
    st.session_state.passwords_table = {
        'Password' : [],
        'Type' : []
    }
    
def analyze_password(password):
    if len(password) < 8:
        return "Invalid Password"

    has_uppercase = False
    has_lowercase = False
    has_digits = False

    for char in password:
        if char.islower():
            has_lowercase = True
        elif char.isupper():
            has_uppercase = True
        elif char.isdigit():
            has_digits = True

    if not has_lowercase or not has_uppercase or not has_digits:
        return "Invalid Password"

    if len(password) <= 11:
        return "Weak Password"
    elif len(password) <= 15:
        return "Medium Password"
    else:
        return "Strong Password"

def analyze_character(c):
    if c.isupper():
        return 'Uppercase'
    elif c.islower():
        return 'Lowercase'
    elif c.isdigit():
        return 'Digit'
    
with tab1:
    password = st.text_input("Enter Password:")

    if password:
        password_analyzation = analyze_password(password)

        for char in password:
            if char.isalpha() or char.isdigit():
                st.write(f"'{char}': Passed -> {analyze_character(char)}")
            else:
                st.write(f"'{char}': Failed -> {analyze_character(char)}")
                
        if password_analyzation == "Invalid Password":
            if password not in st.session_state.invalid_passwords:
                st.session_state.invalid_passwords.append(password)

        st.write(
            f"{password} is {password_analyzation}"
        )

        st.session_state.passwords_table['Password'].append(password)
        st.session_state.passwords_table['Type'].append(password_analyzation)

with tab2:
    st.header("Invalid Passwords")

    invalid_passwords = st.session_state.invalid_passwords

    for invalid_password in invalid_passwords:
        st.write(invalid_password)


with tab3:
    st.table(st.session_state.passwords_table)