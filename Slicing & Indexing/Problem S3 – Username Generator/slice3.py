import streamlit as st

def solve_problem():
    first_name = st.text_input("Enter first name:")
    second_name = st.text_input("Enter second name:")

    if first_name and second_name:
        st.write(first_name + second_name)
        st.write(first_name[:3] + "_" + second_name[:3])
        st.write(first_name[0] + second_name)
        st.write(first_name + "_" + second_name[0])
        st.write(second_name + "_" + first_name[0])

solve_problem()