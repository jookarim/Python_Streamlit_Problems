import streamlit as st
from datetime import date

#Appliation title
st.title("Smart Expense Tracker")
st.divider()

expense_categories = [
    'Food',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Bills'
]

#Tabs for adding expenses and show expenses 
#and Give summary about them

tab1, tab2, tab3 = st.tabs([
    'Add Expense',
    'Expense List', 
    'Summary'    
])

#Crease list of dict expenses in session state 
#to not reset by using widgets

if "expenses" not in st.session_state:
    st.session_state.expenses = []

def display_sidebar():
    """Function to Display Sidebar"""
    with st.sidebar:
        st.subheader("Today's date")
        st.write(date.today())
        
        st.divider()
        
        #Display expenses categories
        for category in expense_categories:
            st.info(category)
        
        st.divider()
        
        #Display budget tips
        st.subheader("Budget Tips")
        
        st.info("Do not buy expensive things frequently")
    
def valid_expense(expense_name, expense_amount):
    """Function to check if the 
    expense is valid or invalid"""
    
    return expense_name != "" and expense_amount > 0

def add_expense():
    """Function to enable user to add expense using a form"""
    with tab1:
        with st.form(key="Expenses Form"):
            #Take expense name, category, amount, date
            expense_name = st.text_input("Expense Name: ")
            expense_category = st.selectbox(
                "Expense Category:",
                expense_categories
            )
            
            #Round expenses amount to the nearest 2 digits
            expense_amount = round(st.number_input("Amount: "), 2)
            
            expense_date = st.date_input("Date: ")
            
            #Form Submit button to add expense
            submit_btn = st.form_submit_button("Add Expense")
            
            #Valid is bool that checks if expense is valid or not
            valid = valid_expense(expense_name, expense_amount)
            
            #Store expense if submit pressed and valid expense            
            if submit_btn and valid:
                st.session_state.expenses.append({
                    "Expense Name: " : expense_name,
                    "Expense Category: " : expense_category,
                    "Expense Amount: " : expense_amount,
                    "Expense Date: " : expense_date
                })

                st.success("Expense added successfully")
                
            #If invalid display error
            elif submit_btn and not valid:
                st.error("Please Enter valid expense")

def money_for_category():
    """Function to store each category spending"""
    money_category = {}

    #Loop through all expenses and using category add amount
    for expense in st.session_state.expenses:
        category = expense["Expense Category: "]
        amount = expense["Expense Amount: "]

        if category not in money_category:
            money_category[category] = 0

        money_category[category] += amount

    return money_category

def get_max_expense():
    """Function to get max expense name and amount"""
    
    max_expense_name = ""
    max_expense_amount = 0
    
    #Loop through expenses
    for expense in st.session_state.expenses:
        #Get expense name and amount
        expense_name = expense['Expense Name: ']
        expense_amount = expense['Expense Amount: ']
        
        #If curr expense amout > the maximum expense amount 
        #then store it as new max expense name and amout
        
        if expense_amount > max_expense_amount:
            max_expense_name = expense_name
            max_expense_amount = expense_amount
            
    #Return name and amount as tuple (Because they are unchangable)
    return (max_expense_name, max_expense_amount)

def get_min_expense():
    """Function to get min expense name and amount"""
    
    min_expense_name = ""
    min_expense_amount = 1e18
    
    #Loop through expenses
    for expense in st.session_state.expenses:
        expense_name = expense['Expense Name: ']      
        expense_amount = expense['Expense Amount: ']
        
        #If curr expense amout < the minimum expense amount 
        #then store it as new min expense name and amout
        
        if expense_amount < min_expense_amount:
            min_expense_amount = expense_amount
            min_expense_name = expense_name
            
    #Return name and amount as tuple (Because they are unchangable)
    return (min_expense_name, min_expense_amount)

def get_avg_expense():
    """Function to get avg expenses amount"""

    sum_expenses = 0
    
    #Loop through expenses to get sum
    for expense in st.session_state.expenses:
        sum_expenses += expense['Expense Amount: ']
    
    #Then devide sum / len to get avg
    
    if len(st.session_state.expenses) != 0:
        sum_expenses /= len(st.session_state.expenses)
    
    return sum_expenses

def get_max_category():
    """Function to get max category used (Food, Entertainment, etc...)"""

    #Get category to money dict
    money_categories = money_for_category()

    max_category_name = ""
    max_category_amount = 0

    #Loop through existing categories
    for category in money_categories:
        #If cash for this category > max_category_amount then set max category name and amount
        if money_categories[category] > max_category_amount:
            max_category_name = category
            max_category_amount = money_categories[category]

    #Return data as tuple
    return (max_category_name, max_category_amount)

def expense_list():
    """Function to display expenses as table"""
    with tab2:
        st.header('Expense List: ')
        st.table(st.session_state.expenses)

def display_summary():
    """Display summary of expenses"""
    with tab3:
        st.header("Summary")
        
        #Display total expenses
        st.write(f"Total Expenses: {len(st.session_state.expenses)}")
        
        #Get total spending
        total_spending = 0
        
        for expense in st.session_state.expenses:
            total_spending += expense["Expense Amount: "]
        
        #Display total spending
        st.write(f"Total Spending: {total_spending}")
        
        #Warning if spending > 1000
        if total_spending > 1000:
            st.warning("Expense exceeds 1000 EGP")

        #Display table money for category
        st.table(money_for_category())        
        
        #Display highest expense, 
        #lowest expense, 
        #avg expense, 
        #category with the highest spending
        
        st.subheader("Highest Expense: ")
        st.write(f"{get_max_expense()[0]} - {get_max_expense()[1]} EGP")
        
        st.subheader("Lowest Expense: ")
        st.write(f"{get_min_expense()[0]} - {get_min_expense()[1]} EGP")
        
        st.subheader('Avarage Expense: ')
        st.write(f"{get_avg_expense()} EGP")
        
        st.subheader("Category with the Highest Spending: ")
        st.write(f"{get_max_category()[0]} - {get_max_category()[1]} EGP")    
#Call the functions
display_sidebar()
add_expense()
expense_list()
display_summary()
