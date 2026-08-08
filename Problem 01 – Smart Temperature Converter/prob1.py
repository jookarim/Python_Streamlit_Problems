import streamlit as st

#Function to print info about the application to 
#Guide the user to use the app correctly

def display_info():
    st.title("Smart Temperature Converter")
    
    st.divider()
    
    with st.sidebar:
        
        st.header("Instructions: ")
        st.info("-Use temperature field to enter temperature")
        st.info("-Choose source and destination units")
        st.info("-Press convert to show result")
        
        st.header("Supported Units")

        st.info("-Celsius")
        st.info("-Fahrenheit")
        st.info("-Kelvin")
        
#convert from celsius to fahrenheit
def cel_feh(temperature):
    st.write("Src Unit: ",
                round(temperature, 2), ' C')
        
    st.write("Dest unit: ", round(temperature * 9 / 5 + 32, 2), ' F')
    st.success("Conversion completed successfully!")
    
#convert from fahrenheit to celsius
def feh_cel(temperature):
    st.write("Src Unit: ",
                round(temperature, 2), ' F')
        
    st.write("Dest unit: ", round((temperature - 32) * 5 / 9, 2), ' C')
        
    st.success("Conversion completed successfully!")
        
#convert from celsius to kelvin
def cel_kel(temperature):
    st.write("Src Unit: ",
                round(temperature, 2), ' C')
        
    st.write("Dest unit: ", round(temperature + 273.15, 2), ' K')
        
    st.success("Conversion completed successfully!")
       
#convert from kelvin to celsius
def kel_cel(temperature):
    st.write("Src Unit: ",
                round(temperature, 2), ' K')
        
    st.write("Dest unit: ", round(temperature - 273.15, 2), ' C')
        
    st.success("Conversion completed successfully!") 
    
#convert from fahrenheit to kelvin
def feh_kel(temperature):
    st.write("Src Unit: ",
                round(temperature, 2), ' F')
        
    st.write("Dest unit: ", round((temperature - 32) * 5 / 9 + 273.15, 2), ' K')
        
    st.success("Conversion completed successfully!")
        
#convert from kelvin to fahrenheit
def kel_feh(temperature):
    st.write("Src Unit: ",
                round(temperature, 2), ' K')
        
    st.write("Dest unit: ", round((temperature - 273.15) * 9 / 5 + 32, 2), ' F')
        
    st.success("Conversion completed successfully!")
        
#Add title, header, supported units and show instructions
display_info()

#define cols to make half of the screen for form 
#and the other half for result
col1, col2 = st.columns([1, 1])
    
#temperature form to select source and destination units 
# and enter temperature
#Used select box to avoid violation


with col1:
    with st.form("Temperature form"):
        #temperature value input
        temperature = st.number_input("Enter temperature: ")
            
        #Src units selection
        src_unit = st.selectbox("Src Units: ", [
            "Celsius",
            "Fahrenheit",
            "Kelvin"
        ])
        
        #Destination units selection
        dest_unit = st.selectbox("Dest Units: ", [
            "Celsius",
            "Fahrenheit",
            "Kelvin"
        ])
        
        #Submit button to 
        #convert temperature from src unit to dest unit
        btn_submit = st.form_submit_button("Convert")

with col2:
    
    #Checking if leaving space empty
    if (src_unit == "" or dest_unit == "") and btn_submit:
        st.error("Cannot leave space empty")

    #Checking if src and dest units are the same
    if (src_unit == dest_unit 
        and btn_submit 
        and src_unit != "" 
        and dest_unit != ""):
        
        st.warning("Src and Dest units could not be the same")

    # checking if src is celsius and dest is fahrenheit 
    # then convert between them
    if (src_unit == "Celsius" 
        and dest_unit == "Fahrenheit" 
        and btn_submit):
        
        cel_feh(temperature)

    # checking if src is fahrenheit and dest is celsius 
    # then convert between them
    if (src_unit == "Fahrenheit" 
        and dest_unit == "Celsius" 
        and btn_submit):
    
        feh_cel(temperature)

    # checking if src is celsius and dest is kelvin 
    # then convert between them
    if (src_unit == "Celsius" 
        and dest_unit == "Kelvin" 
        and btn_submit):
        
        cel_kel(temperature)

    # checking if src is kelvin and dest is celsius 
    # then convert between them
    if (src_unit == "Kelvin" 
        and dest_unit == "Celsius" 
        and btn_submit):
        
        kel_cel(temperature)

    # checking if src is fahrenheit and dest is kelvin 
    # then convert between them
    if (src_unit == "Fahrenheit" 
        and dest_unit == "Kelvin" 
        and btn_submit):
    
        feh_kel(temperature)        

    # checking if src is kelvin and dest is fahrenheit 
    # then convert between them
    if (src_unit == "Kelvin" 
        and dest_unit == "Fahrenheit" 
        and btn_submit):
    
        kel_feh(temperature)