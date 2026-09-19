import streamlit as st
import time 

#Application title
st.title("Smart employee payroll system", text_alignment='center')

#4 tabs for application sections 
tab1, tab2, tab3, tab4 = st.tabs([
                                "Payroll calculator",
                                "Recent payroll", 
                                'All employees payroll', 
                                'Monthly dashboard'
                                ])
 
#Employees data ID,Name,Hourly rate foreach employees 
#to be able to choose and pay employee

if 'employees_data' not in st.session_state:
    st.session_state.employees_data = [
        {
            'ID' : 1001,
            'Name' : 'Ahmed',
            'Hourly rate' : 120
        },
        
        {
            'ID' : 1002,
            'Name' : 'Sara',
            'Hourly rate' : 150
        },
        
        {
            'ID' : 1003,
            'Name' : 'Omar',
            'Hourly rate' : 180
        },
        
        {
            'ID' : 1004,
            'Name' : 'Mariam',
            'Hourly rate' : 200
        },
    ]    

#Employees payroll list 
#to store all payrolls the employees made

if 'employees_payroll' not in st.session_state:
    st.session_state.employees_payroll = []
    
def display_sidebar():
    """Display payroll formulas and working hours in sidebar 
    to guide users how each part of the salary is calculated"""
    
    #Creating sidebar section
    with st.sidebar:
        
        #Displaying payroll formulas
        #to guide users how each part of the salary is calculated
        
        st.subheader("Payroll Formulas")
        st.markdown("**Basic Salary** = Hourly Rate × Working Hours")
        st.markdown("**OT Pay** = Hourly Rate × Overtime Hours × 1.5")
        st.markdown("**Gross Salary** = Basic Salary + OT Pay + Bonus")
        st.markdown("**Net Salary** = Gross Salary − Deduction")
        
        #Displaying working hours
        st.subheader('Working Hours: 8am to 8pm')


def calculate_payroll(
                    employee, 
                    working_hours, 
                    overtime_hours, 
                    deduction, 
                    bonus):
    """Calculate payroll using employee data taken from the form"""
    
    idx = 0
    
    #Search for employee to get his data taken from form
    for employee_data in st.session_state.employees_data:
        if employee_data['Name'] == employee:
            break 
        idx += 1 
    
    #Getting employee hourly rate to calculate net salary
    hourly_rate = st.session_state.employees_data[idx]['Hourly rate']
    
    #Calculating basic salary
    basic_salary = hourly_rate * working_hours
    
    #Calculating overtime pay
    ot_pay = hourly_rate * overtime_hours * 1.5 
    
    #Calculating gross salary
    gross_salary = basic_salary + ot_pay + bonus 
    
    #Calculating net salary after deduction
    net_salary = gross_salary - deduction

    #Returning all calculated payroll values
    return (hourly_rate, 
            basic_salary, 
            ot_pay,
            gross_salary, 
            net_salary)    


def get_employee(name):
    """Get employee by name to get his data 
    to get performance and salary"""
    
    #Search for employee using his name
    for employee in st.session_state.employees_data:
        if employee['Name'] == name:
            return employee 
      

def get_performance(overtime_hours):
    """Get employee performance based on overtime hours"""
    
    #Employee has standard performance without overtime
    if overtime_hours == 0:
        return 'Standard'
    
    #Employee has good performance with 1 to 10 overtime hours
    elif overtime_hours >= 1 and overtime_hours <= 10:
        return 'Good'
    
    #Employee has excellent performance with 11 to 20 overtime hours
    elif overtime_hours >= 11 and overtime_hours <= 20:
        return 'Excellent'
    
    #Employee has outstanding performance with more than 20 overtime hours
    elif overtime_hours > 20:
        return 'Outstanding'
    
    return ''


def payroll_calculator():
    """Function to get payroll data then"""
    
    #Creating form for entering payroll information
    with st.form("Payroll calculator"):
        employees_names = []
        
        #Getting all employee names to create the employee selectbox
        for employee_data in st.session_state.employees_data:
            employees_names.append(employee_data['Name'])
            
        #Getting employee payroll information from user
        employee = st.selectbox("Select employee: ", employees_names)
        working_hours = st.number_input("Working hours: ", min_value=1)
        overtime_hours = st.number_input("Overtime hours: ", min_value=0)
        bonus = st.number_input("Bonus: ", min_value=0)
        deduction = st.number_input("Deduction: ", min_value=0)
        
        #Creating button to submit the form
        submit = st.form_submit_button("Calculate payroll", type='primary')
        
    #Only calculate payroll after user submits the form
    if submit:
        with st.spinner("Calculating payroll"):
            time.sleep(2)
            
        #Calculating employee payroll
        (
        hourly_rate, 
        basic_salary, 
        ot_pay,
        gross_salary, 
        net_salary) = calculate_payroll(
                                    employee, 
                                    working_hours, 
                                    overtime_hours, 
                                    deduction, 
                                    bonus
                                )
        
        #Getting complete employee data
        employee_data = get_employee(employee)
        
        #Getting employee performance
        performance = get_performance(overtime_hours)
        
        #Saving the calculated payroll 
        #at the beginning of the payroll list
        #to display payrolls and get recent payroll
        st.session_state.employees_payroll.insert(0, {
            'Employee ID' : employee_data['ID'],
            'Employee Name' : employee_data['Name'],
            'Hourly rate' : hourly_rate,
            'Working hours' : working_hours,
            'Overtime hours' : overtime_hours,
            'Basic salary' : basic_salary,
            'OT pay' : ot_pay,
            'Bonus' : bonus,
            'Gross salary'  : gross_salary,
            'Deduction' : deduction, 
            'Net salary' : net_salary,
            'Performance' : performance 
        })
        
        #Displaying the calculated net salary
        st.write(f"Total payroll: {net_salary} EGP")

        #Display success message
        st.success('Payroll calculated successfully')
        #Warning the user if overtime is very high
        if overtime_hours > 20:
            st.warning("Much overtime")
            

def display_latest_payroll():
    
    #Check if there is no payroll data
    if not len(st.session_state.employees_payroll):
        st.info('No payroll yet')
        
    #Display the most recent payroll
    else:
        st.header('Recent employee payroll')
        
        #Getting the payroll list
        employees_payroll = st.session_state.employees_payroll
        
        #Getting the latest payroll because new payroll is inserted at index 0
        latest_payroll = employees_payroll[0]
        
        #Creating two columns for displaying payroll information
        left_column, right_column = st.columns(2, border=True)
        
        #Displaying employee information in the left column
        with left_column:
            left_column.code(f"""
                Employee ID: {latest_payroll['Employee ID']}
                Employee Name: {latest_payroll['Employee Name']}
                Hourly rate: {latest_payroll['Hourly rate']}
                Working hours: {latest_payroll['Working hours']}
                Overtime hours: {latest_payroll['Overtime hours']}    
            """)
            
        #Displaying salary information in the right column
        with right_column:
            right_column.code(f"""
            OT pay: {latest_payroll['OT pay']} EGP 
            Bonus: {latest_payroll['Bonus']} EGP
            Deduction: {latest_payroll['Deduction']} EGP
            Basic salary: {latest_payroll['Basic salary']} EGP 
            Gross salary: {latest_payroll['Gross salary']} EGP
            Net salary: {latest_payroll['Net salary']} EGP
            Performance: {latest_payroll['Performance']}
            """)

def display_payrolls():
    #Displaying all employee payroll records
    
    if len(st.session_state.employees_payroll):
        st.header('All Employees Payroll')
        st.table(st.session_state.employees_payroll)
    else:
        st.info("There are no employees paid yet")


def get_salaries_data():
    
    #Return default values if there is no payroll data
    if not st.session_state.employees_payroll:
        return (0, 0, 0, 0, "No Employees", 0, 0)

    #Creating variables to store payroll statistics
    total_salaries = 0
    total_bonuses = 0
    total_deduction = 0
    
    #Starting with values that can be replaced by real salary values
    max_salary = -1
    min_salary = 1e18
    
    #Using the first employee to initialize highest overtime
    max_overtime = st.session_state.employees_payroll[0]['Overtime hours']
    max_overtime_employee = (
        st.session_state.employees_payroll[0]['Employee Name']
    )
    
    #Loop through every payroll record
    for employee_payroll in st.session_state.employees_payroll:
        
        #Adding salary, bonus and deduction to their totals
        total_salaries += employee_payroll['Net salary']
        total_bonuses += employee_payroll['Bonus']
        total_deduction += employee_payroll['Deduction']
        
        #Updating highest and lowest salary
        max_salary = max(employee_payroll['Net salary'], max_salary)
        min_salary = min(employee_payroll['Net salary'], min_salary)
        
        #Check if this employee has more overtime than the current maximum
        if employee_payroll['Overtime hours'] > max_overtime:
            max_overtime = employee_payroll['Overtime hours']
            max_overtime_employee = employee_payroll['Employee Name']
            
    #Calculating the average salary
    avg_salary = total_salaries / len(st.session_state.employees_payroll)
    
    #Returning all dashboard statistics
    return (total_salaries, 
            avg_salary, 
            max_salary, 
            min_salary, 
            max_overtime_employee,
            total_bonuses,
            total_deduction)
    

def monthly_payroll_dashboard():
    
    #Do not display dashboard if there is no payroll data
    if len(st.session_state.employees_payroll) == 0: 
        return 
    
    #Displaying dashboard title
    st.header('Monthly Payroll Dashboard')
    
    #Getting all payroll statistics
    (total_salaries, 
    avg_salary, 
    max_salary,
    min_salary,
    max_overtime_employee, 
    total_bonuses, 
    total_deduction) = get_salaries_data()
    
    #Displaying number of employees processed
    st.write(f'Total employees processed: ' 
            f'{len(st.session_state.employees_payroll)}')
    
    #Displaying total salaries
    st.write(f'Total salaries paid: {total_salaries:,.2f}')
    
    #Displaying average salary
    st.write(f'Average salary: {avg_salary:,.2f}')
    
    #Displaying highest salary
    st.write(f'Highest salary: {max_salary:,.2f}')
    
    #Displaying lowest salary
    st.write(f'Lowest salary: {min_salary:,.2f}')
    
    #Displaying total bonuses
    st.write(f'Total bonuses paid: {total_bonuses:,.2f}')
    
    #Displaying total deductions
    st.write(f'Total deductions: {total_deduction:,.2f}')
    
    #Displaying employee with the highest overtime
    st.write(f'Employee with highest overtime: {max_overtime_employee}')

        
#Displaying the sidebar
display_sidebar()

#Displaying payroll calculator in tab 1
with tab1:
    payroll_calculator()
    
#Displaying latest payroll in tab 2
with tab2:
    display_latest_payroll()
    
#Displaying all payroll records in tab 3
with tab3:
    display_payrolls()

#Displaying monthly payroll statistics in tab 4
with tab4:
    monthly_payroll_dashboard()