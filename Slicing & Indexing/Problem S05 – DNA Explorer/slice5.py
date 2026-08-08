import streamlit as st

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

if "wrong_sequence" not in st.session_state:
    st.session_state.wrong_sequence = False
        
def create_app():
    
    dna_base_count = {
        'A' : 0,
        'T' : 0,
        'C' : 0,
        'G' : 0
    }
    
    dna_sequence = st.text_input("Enter DNA Sequence: ")
    
    first_20_button = st.button("First 20 Characters")
    last_20_button = st.button("Last 20 Characters")
    middle_section = st.button("Middle section")
    reverse_sequence = st.button("Reverse sequence")
    every_second_base = st.button("Every second base")    
    every_third_base = st.button("Every third base")
    dna_length = st.button("DNA Length")
    
    for dna in dna_sequence:
        dna_base_count[dna] += 1
        
    for key, value in dna_base_count.items():
        st.write(f"{key} : {value}")
        st.session_state.button_clicked = True
            
    if first_20_button:
        if len(dna_sequence) >= 20:
            st.write(f"First 20 Bases: {dna_sequence[:20]}")
        else:
            st.write("DNA Sequence is soo small")
            
        st.session_state.button_clicked = True
    elif last_20_button:
        if len(dna_sequence) >= 20:
            st.write(f"Last 20 Bases: {dna_sequence[len(dna_sequence) - 20:]}")
        else:
            st.write("DNA Sequence is soo small")
            
        st.session_state.button_clicked = True
        
    elif middle_section:
        st.write(dna_sequence[len(dna_sequence) // 4: len(dna_sequence) * 3 // 4])
        st.session_state.button_clicked = True
        
    elif reverse_sequence:
        st.write(dna_sequence[::-1])
        st.session_state.button_clicked = True
        
    elif every_second_base:
        st.write(dna_sequence[::2])
        st.session_state.button_clicked = True
        
    elif every_third_base:
        st.write(dna_sequence[::3])
        st.session_state.button_clicked = True
        
    elif dna_length:
        st.write(len(dna_sequence))
        st.session_state.button_clicked = True
        
    st.subheader("DNA Preview")
    
    st.write(f"First 10 Bases: {dna_sequence[:10]}")
    st.write(f"Last 10 Bases: {dna_sequence[len(dna_sequence) - 10:]}")
    
    if st.session_state.button_clicked:
        for sequence in dna_sequence:
            if sequence not in dna_base_count:
                st.session_state.wrong_sequence = True
                break

    if st.session_state.wrong_sequence or len(dna_sequence) < 20:
        st.write("Wrong DNA Sequence")
    else:
        st.write("Valid DNA Sequence")
        
create_app()