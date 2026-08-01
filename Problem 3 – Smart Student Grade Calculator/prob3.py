import streamlit as st

#Display title of the App
st.title("Student Grade Calculator")
st.divider()

#Grading scale to guide users of the letter grades meaning
grading_scale_dict = {
    'A' : '90-100',
    'B' : '80-89',
    'C' : '70-79',
    'D' : '60-69',
    'F' : "Below 60"
}

#Initialize student_grades list that stores name and avg score
#Init it if it is not found in session state
#I use session state to store grades and 
#do not get removed when button pressed
if 'student_grades' not in st.session_state:
    st.session_state.student_grades = []
    
#Create columns that are used in displaying form and student report
col1, col2 = st.columns([1,1])

def display_sidebar():
    """Display sidebar grading scale and passing score to guide user about grading"""
    with st.sidebar:
        st.header("Grading Scale")
        for key in grading_scale_dict.keys():
            st.info(key + ' : ' + grading_scale_dict[key])
        st.divider()
        st.info(f"Passing Score: {60}")

def calculate_avg(math_result, science_result, english_result):
    """Get avarage of grades"""
    return (math_result + science_result + english_result) / 3

def calculate_grade_letters(grade_num):
    """Get grade letters depending on grade_num"""
    if grade_num >= 90 and grade_num <= 100:
        return 'A'
    elif grade_num >= 80 and grade_num <= 89:
        return 'B'
    elif grade_num >= 70 and grade_num <= 79:
        return 'C'
    elif grade_num >= 60 and grade_num <= 69:
        return 'D'
    else: return 'F'
    
def get_achievement(degree_num):
    """Determine student achievement depending on avg score"""
    if degree_num >= 95: 
        return "Outstanding"
    elif degree_num >= 90 and degree_num <= 94.99:
        return "Honor student"
    elif degree_num >= 80 and degree_num <= 89.99:
        return "Excellent Work"
    else: 
        return "Keep Improving"
    
def valid_degrees(math_degree, science_degree, english_degree):
    """determine if grade is valid (0,100 range) or not"""
    return not(math_degree < 0 or math_degree > 100 or
                science_degree < 0 or science_degree > 100 or
                english_degree < 0 or english_degree > 100)
    
def get_stats():
    """Function that gots lowest and highest avg score with letters and student names and count passed and failed and avg score"""
    
    # Check if empty to prevent division by zero crash
    if not st.session_state.student_grades:
        return ("", 0, "", "", 101, "", 0, 0, 0)

    #Init vars
    highest_avg_name = ""
    highest_avg = 0
    highest_avg_letter = ''
    lowest_avg_name = ""
    lowest_avg = 101
    lowest_avg_letter = ''
    count_passed = 0
    count_failed = 0
    avg_score = 0
    
    #Loop through grades
    for sg in st.session_state.student_grades:
        #Get highest and lowest avg and store the name of the students of 
        #highest and lowest avg and letter of degree
        #and get count passed and failed
        #and lastly get avg score
        if sg["Avg: "] > highest_avg:
            highest_avg = round(sg["Avg: "], 2)
            highest_avg_name = sg["Name: "]
            highest_avg_letter = sg["Grade Letter: "]
        if sg["Avg: "] < lowest_avg:
            lowest_avg = round(sg["Avg: "], 2)
            lowest_avg_name = sg["Name: "]
            lowest_avg_letter = sg["Grade Letter: "]
        if sg["Avg: "] >= 60:
            count_passed += 1
        else:
            count_failed += 1
        avg_score += round(sg['Avg: '])
        
    avg_score /= len(st.session_state.student_grades)
    
    avg_score = round(avg_score, 2)
    #Return data as tuple to be used down
    return (highest_avg_name, highest_avg, highest_avg_letter, lowest_avg_name, lowest_avg, lowest_avg_letter, count_passed, count_failed, avg_score)

def student_info_form_display():
    """Create Student data form and Display Student Report
    and The history of last 5 students"""
    
    #display form is col1
    with col1:
        with st.form(key='student_form'):
            student_name = st.text_input('Student Name ')
            math_degree = st.number_input("Math ")
            science_degree = st.number_input("Science ")
            english_degree = st.number_input("English ")
            
            #Submit button to submit the form
            submit_button = st.form_submit_button("Calculate Result")
            
            
    with col2:
            #Check if english, math, science degrees are valid
            valid_degree = valid_degrees(math_degree, science_degree, english_degree)
            
            #If degree is valid and pressed on submit then display report and history table
            if valid_degree and submit_button:
                #Display student report
                st.header("Student Report")
                #Get avg of degrees
                avg = round(calculate_avg(math_degree, science_degree, english_degree), 2)
                st.write("Avarage: ", avg)
                grade_letter = calculate_grade_letters(avg)
                #Display Grade in letters
                st.write('Grade: ' + grade_letter)
                
                #If Grade not F or D then display passed in success
                if grade_letter != 'F' and grade_letter != 'D':
                    st.success("Passed")
                #If grade is F then display failed as error
                elif grade_letter == 'F': 
                    st.error("Failed")
                #If grade is D then display passed but as warning
                else: st.warning('Passed')
                
                #Display student achievement depending on avg mark
                st.subheader('Achievement')
                achievement = get_achievement(avg)
                
                #If student grades len = 5 then shift history by 1 
                #(Erase the first one of history and add new element to keep last 5)
                if len(st.session_state.student_grades) == 5:
                    st.session_state.student_grades = st.session_state.student_grades[1:len(st.session_state.student_grades)]
                    st.session_state.student_grades.append({
                        "Name: " : student_name, 
                        "Avg: " : avg,
                        "Grade Letter: " : grade_letter
                    })
                    
                #But if len < 5 then just add new element until len reach 5
                else:
                    st.session_state.student_grades.append({
                        "Name: " : student_name, 
                        "Avg: " : avg,
                        "Grade Letter: " : grade_letter
                    })
                    
                #Display student achievement
                st.write(achievement)
                
                #Display students history as table
                st.table(st.session_state.student_grades)   
                
                #Display some statistics about last 5 students
                st.write(f"Highest Avg Student {get_stats()[0]} That got {get_stats()[1]} With letter mark {get_stats()[2]}")
                st.write(f"Lowest Avg Student {get_stats()[3]} That got {get_stats()[4]} With letter mark {get_stats()[5]}")
                st.write(f"Count passed students: {get_stats()[6]}")
                st.write(f"Count failed students: {get_stats()[7]}")
                st.write(f"Avg score of students: {get_stats()[8]}")
            #If degree is invalid and user pressed Calculate Result 
            #then display Invalid degrees     
            elif (not valid_degree or student_name == '') and submit_button:
                with col2:
                    st.error("Invalid degrees")
    
display_sidebar()
student_info_form_display()