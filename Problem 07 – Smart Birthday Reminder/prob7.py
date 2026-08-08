import streamlit as st
from datetime import date

#Create relationships list
relationship_list = [
    'Family',
    'Friend',
    'Classmate',
    'Coworker'    
]

#Display Title
st.title('Smart Birthday Remainder')
st.divider()

#Create 4 tabs to add birthday, 
#show birthday list, 
#search for birthday by person name 
#and lastly statistics
tab1, tab2, tab3, tab4 = st.tabs([
    'Add Birthday',
    'Birthday List',
    'Search',
    'Statistics'
])

#Init birthdays data session state list of dict 
#(session state to make it does not reset when using widgets)

if 'birthdays' not in st.session_state:
    st.session_state.birthdays = []

def display_sidebar():
    """Function to display sidebar 
    (Today's date, Relationship list and Birthday tips)"""
    
    with st.sidebar:
        st.write(f"Today's date: {date.today()}")
        
        st.divider()
        
        st.subheader('Relationship list: ')
        
        for relationship in relationship_list:
            st.info(relationship)
        
        st.divider()
        
        st.subheader('Birthday tips: ')
        st.info('Go on time')
    
def add_birthday_record():
    """Function to add birthday record"""
    with tab1:
        """Creating form to set birthday data"""
        with st.form(key="AddBirthdayForm"):
            #Take name, date, relationship and lastly save button
            name = st.text_input('Name: ')
            birthday = st.date_input('Birthday: ')
            relationship = st.selectbox('Relationship: ', relationship_list)
            save_button = st.form_submit_button('Save Birthday')
            
            #If it is a valid input then add data to birthdays list of dict            
            if name != '' and birthday and save_button:
                st.session_state.birthdays.append({
                    "Name: " : name,
                    "Birthday: " : birthday, 
                    "Relationship: " : relationship,
                    "Next Birthday: " : f"After {(date(date.today().year, birthday.month, birthday.day) - date.today()).days % 365} Days",
                    "Current Age: " : date.today().year - birthday.year
                })
                
                #Tell success message after adding data
                st.success('Birthday saved successfully!')
                
                #Check if the birthday is today and if this then tell that it is true
                if date(2026, birthday.month, birthday.day) == date.today():
                    st.warning(f"Today is {name}'s Birthday")
            
            #If input is invalid then say error message
            elif save_button and (name == '' or not birthday):
                st.error('Person not found')
            
def display_birthday_list():
    """Display birthday data as table"""
    with tab2:
        #Create cols
        col1, col2, col3, col4, col5 = st.columns(5)
        #Loop through all birthdays
        for birthday in st.session_state.birthdays:
            #Display each category in a col
            with col1:
                st.write(f"Name: {birthday['Name: ']}")
            with col2:
                st.write(f"Birthday: {birthday['Birthday: ']}")
            with col3:
                st.write(f"Relationship: {birthday['Relationship: ']}")
            with col4: 
                st.write(f"Next Birthday: {birthday['Next Birthday: ']}")
            with col5:
                st.write(f"Current Age: {birthday['Current Age: ']}")
def search():
    """Search for birthdat by person's name"""
    with tab3:
        #Use form to enter name
        with st.form(key="SearchForm"):
            name = st.text_input('Name: ').lower()
            search_button = st.form_submit_button('Search')
            
            #If input is valid 
            if search_button and not name == '':
                found_name = False
                #Loop through thxe birthdays
                for birthday in st.session_state.birthdays:
                    if birthday['Name: '].lower() == name:
                        found_name = True
                        st.table(birthday)
                        
                        if birthday['Next Birthday: '] == 0:
                            st.warning(f"Today is {birthday['Name: ']}'s Birthday")

            elif search_button and name == '':
                st.error('Please do not keep the name empty')
            
            elif search_button and not found_name:
                st.error("Please enter name for a found person")
                
def get_youngest_person():
    """Function to look up the youngest person's name"""
    youngest_person_name = ""
    youngest_person_age = 1e18
    
    #Loop through the birthdays
    for birthday in st.session_state.birthdays:
        age = birthday["Current Age: "]
         
        #If age is smaller than youngest person age then save this name
        if age < youngest_person_age:
            youngest_person_age = age 
            youngest_person_name = birthday['Name: ']
            
    return youngest_person_name

def get_oldest_person():
    """Function to look up the oldest person's name"""
    oldest_person_name = ""
    oldest_person_age = -1
    
    #Loop through the birthdays
    for birthday in st.session_state.birthdays:
        age = birthday["Current Age: "]
         
        #If age is bigger than oldest person age then save this name
        if age > oldest_person_age:
            oldest_person_age = age 
            oldest_person_name = birthday['Name: ']
            
    return oldest_person_name

def get_count_by_relationship(relationship):
    """Function to count people by relationship type"""
    count_relationship = 0
    
    #Loop through the birthdays
    for birthday in st.session_state.birthdays:
        #If relationship matches then add 1 to count
        if birthday['Relationship: '] == relationship:
            count_relationship += 1
    
    return count_relationship

def show_statistics():
    """Function to display statistics data"""
    with tab4:
        #Display Header and statistics text summary values
        st.header('Statistics: ')
        st.write(f"Total number of people: {len(st.session_state.birthdays)}")
        st.write(f"Youngest Person: {get_youngest_person()}")
        st.write(f"Oldest Person: {get_oldest_person()}")
        st.write(f"Number of Family Members: {get_count_by_relationship('Family')}")
        st.write(f"Number of Friends: {get_count_by_relationship('Friend')}")
        st.write(f"Number of Classmates: {get_count_by_relationship('Classmate')}")
        st.write(f"Number of Coworkers: {get_count_by_relationship('Coworker')}")
        
#Run all dashboard functions
display_sidebar()
add_birthday_record()
display_birthday_list()
search()
show_statistics()
