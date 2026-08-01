import streamlit as st

def create_app():
    word_input = st.text_input("Enter Text: ")
    
    st.write("".join(word_input))
    st.write("".join(word_input[::-1]))
    
    # l = 0
    # r = 0

    # while r < len(word_input):
    #     if word_input[r] != ' ':
    #         r += 1
    #     else:
    #         word_input[l:r] = word_input[l:r][::-1]
    #         r += 1
    #         l = r
            
    # st.write("".join(word_input))
    
    word_split_list = word_input.split(" ")

    for i in range(len(word_split_list)):
        word_split_list[i] = word_split_list[i][::-1]

    st.write(" ".join(word_split_list))
    
create_app()