import streamlit as st

def create_app():
    """App to take password from user
    and display some sliced data from it"""

    password = st.text_input("Enter Password: ")
    masked_password = ""

    st.write(f"Password Length: {len(password)}")
    for i in range(len(password)):
        masked_password += "*"

    st.write("Masked Password: " + masked_password)

    st.write("First 2 Characters: " + password[:2])
    st.write("Last 2 Characters: " + password[-2:])
    st.write("First Half: " + password[:len(password) // 2])
    st.write("Second Half: " + password[len(password) // 2:])
    st.write("Reversed Password: " + password[::-1])

create_app()