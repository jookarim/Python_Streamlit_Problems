import streamlit as st

def app_create():
    paragraph = st.text_area("Enter Text: ")
    
    first_10_chars = st.button("First 10 Characters")
    last_10_chars = st.button("Last 10 Characters")
    reverse_text = st.button("Reverse Text")
    every_second_char = st.button("Every second character")
    every_third_char = st.button("Every third char")
    mid_section = st.button("Middle section")
    
    if first_10_chars:
        st.write(paragraph[:10])

    elif last_10_chars:
        st.write(paragraph[-10:])

    elif reverse_text:
        st.write(paragraph[::-1])

    elif every_second_char:
        st.write(paragraph[::2])

    elif every_third_char:
        st.write(paragraph[::3])

    elif mid_section:
        start = len(paragraph) // 4
        end = 3 * len(paragraph) // 4
        st.write(paragraph[start:end])
app_create()