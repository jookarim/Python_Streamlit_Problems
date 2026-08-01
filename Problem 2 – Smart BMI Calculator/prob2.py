import streamlit as st

#dictionary to store history of each user
if "history_dict" not in st.session_state:
    st.session_state.history_dict = {}

#create advices dict to display advices for each BMI category
advices_dict = {
    "Underweight" : "Eat a balanced diet and consult a nutritionist",
    "Normal Weight" : "Keep up the healthy lifestyle",
    "Overweight" : "Increase physical activity and improve eating habits.",
    "Obese" : "Consult a healthcare professional for a health plan."
}

def get_bmi_category(bmi):
    """Return BMI category depending on bmi value"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi >= 18.5 and bmi <= 24.9:
        return "Normal Weight"
    elif bmi >= 25 and bmi <= 29.9:
        return "Overweight"
    elif bmi > 29.9:
        return "Obese"
    else: return "Unknown"
    
        
#Put title for the BMI app
st.title("Smart BMI Calculator")
st.divider()

#2 cols to make col1 for the form and col2 for the result
col1, col2 = st.columns([1,1])

#display BMI formula and categories in the sidebar to give users info
with st.sidebar:
    #BMI calculation formula from weight and height
    st.header("BMI Formula")
    st.info("Weight / (Height * Height)")
    
    st.divider()
    
    #BMI categories 
    st.header("BMI Categories: ")
    st.info("Underweight (BMI less than 18.5)")
    st.info("Normal Weight (BMI from 18.5 to 24.9)")
    st.info("Overweight (BMI from 25 to 29.9)")
    st.info("Obese (BMI greater than or equal to 30)")
    
#create input form to enter user data and it is in col1
with col1:
    with st.form(key="bmi_form"):
        #Enter name
        name = st.text_input("Name: ")
        #Enter weight
        weight = st.number_input("Weight (kg): ")
        #Enter height
        height = st.number_input("Height (m): ")
        #Form submit button
        submit = st.form_submit_button("Calculate BMI")


#condition that the user input is correct
if not(weight <= 0 or height <= 0 or name == "") and submit:
    #use col2 to make the output on the right of the form
    with col2:
        #Display BMI Value, Category and needed advice for each category 
        st.header("BMI Report")
        bmi = round(weight / (height * height), 2)
        st.write("BMI Value: ", bmi)
        category = get_bmi_category(bmi)
        st.write("BMI Category: ", category)
        
        if category == "Underweight" or category == "Overweight":
            st.warning("BMI Category: " + category)
        elif category == "Obese":
            st.error("BMI Category: " + category)
        elif category == "Normal Weight":
            st.success("BMI Category: " + category)
            
        st.info("Advice: " + advices_dict[category])  
        
        #Add bmi value to history dict 
        #to use it when displaying user history dict
        if name not in st.session_state.history_dict:
            st.session_state.history_dict[name] = [bmi]
        else:
            st.session_state.history_dict[name].append(bmi)
            
        
        #store bmi_categories from history_dict[name] to be used in the table
        bmi_categories = []
        
        for bmi in st.session_state.history_dict[name]:
            bmi_categories.append(get_bmi_category(bmi))
            
        st.header("History of costumer: " + name)
        
        
        #display BMI table in the 2 columns inside col2 
        #to make 1 col fro BMI val and the other for BMI category
        with col2:
            st.table({
                "BMI Value": st.session_state.history_dict[name],
                "BMI Category": bmi_categories
            })
            

#Error message when invalid input
    
elif (weight <= 0 or height <= 0 or name == "") and submit:
    st.error("Invalid input, please try again")