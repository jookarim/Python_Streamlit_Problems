import streamlit as st
import time
from datetime import datetime

#Title for the Banking system
st.title('Smart ATM Banking System')
st.divider()

#Define 4 tabs for the app 
#(Login screen, ATM operations, Account Information, Transaction history)
tab1, tab2, tab3, tab4 = st.tabs(
    ['Login', 'ATM Operations', 'Account Information', 'Transaction History']
)

#Define accounts_dict that stores 5 customers data
if 'accounts_dict' not in st.session_state:
    st.session_state.accounts_dict = [
    {
        'Account Number': '1001',
        'Customer Name': 'Ahmed Ali',
        'PIN': '1234',
        'Balance': 5000
    },
    {
        'Account Number': '1002',
        'Customer Name': 'Fatima Hassan',
        'PIN': '5678',
        'Balance': 7500
    },
    {
        'Account Number': '1003',
        'Customer Name': 'John Doe',
        'PIN': '4321',
        'Balance': 3200
    },
    {
        'Account Number': '1004',
        'Customer Name': 'Sarah Smith',
        'PIN': '8765',
        'Balance': 12000
    },
    {
        'Account Number': '1005',
        'Customer Name': 'Omar Farooq',
        'PIN': '0000',
        'Balance': 450
    }
]

#List of dict that stores transactions history
if 'transaction_history' not in st.session_state:
    st.session_state.transaction_history = []
    
#Boolean to chech that user has logged in or no
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

#Store Last transaction that user made 
if 'last_transaction' not in st.session_state:
    st.session_state.last_transaction = ''
    
#Store transaction status to determine 
#that the transaction status valid or invalid
if 'transaction_status' not in st.session_state:
    st.session_state.transaction_status = False

#Dict to store account number as a key 
#and total account deposites as value
if 'total_deposites' not in st.session_state:
    st.session_state.total_deposites = {}

#Dict to store account number as key 
#and total account withdrawals as value
if 'total_withdraw' not in st.session_state:
    st.session_state.total_withdraw = {}
 
#Store current account idx to access account data easly
if 'account_used_idx' not in st.session_state:
    st.session_state.account_used_idx = 0  

def customer_login():
    """Function to make user login 
    and check if login is valid
    it lets user to use atm operations 
    and see transactions history 
    and account details and 
    if invalid it displayes an error message"""
    
    #Scan account number and PIN from user 
    #if not logged in 
    #else put a greeting message

    account_number = st.text_input("Account Number: ")
    pin = st.text_input("PIN: ", type = "password", max_chars = 4)
    
    #Submit button to check account number and PIN

    login = st.button('Login')
          
    #Check if submit button pressed    
    if login:
        idx = 0 
        login_success = False
        
        #loop through all accounts
        for account in st.session_state.accounts_dict:
            #Check if the user inputed account details are in accounts dict
            if (account_number == account['Account Number'] 
                and pin == account['PIN']):
                #Set logged_in to true and store account idx to the idx
                st.success('PIN is entered successfully')  
                st.session_state.logged_in = True
                st.session_state.account_used_idx = idx
                login_success = True
                break 
            
            idx += 1
        
        #If login is invalid 
        #then display an error message 
        #and set logged_in = false
        if not login_success:
            st.error('Invalid pin or account number')
            st.session_state.logged_in = False

def withdraw(amount):
    #Get current user account data
    account_dict = st.session_state.accounts_dict
    account = account_dict[st.session_state.account_used_idx]

    total_withdraw = st.session_state.total_withdraw
    #Check if withdraw amount is larger than balance
    if amount > account['Balance']:
        st.error('Withdraw amount is great than the balance')
        st.session_state.transaction_status = False
    else:
        #Subtract amount from current balance
        account['Balance'] -= amount
        
        #Check if account number not in total withdraw dict 
        #to set it to 0
        if ((account['Account Number']) 
            not in (total_withdraw)):
            
            total_withdraw[account['Account Number']] = 0
            
        #Add amount to total withdraw dict and 
        #set last transaction text 
        #and set status to true

        total_withdraw[account['Account Number']] += amount
        st.session_state.last_transaction = f'Withdraw {amount}'
        st.session_state.transaction_status = True
        
def deposite(amount):
    #Get current user account data
    account_dict = st.session_state.accounts_dict
    account = account_dict[st.session_state.account_used_idx]
    #Add amount to current balance
    account['Balance'] += amount
    
    #Check if account number not in total deposites dict to set it to 0
    if (account['Account Number'] 
        not in st.session_state.total_deposites):
        total_deposites = st.session_state.total_deposites
        total_deposites[account['Account Number']] = 0
    
    #Add amount to total deposites dict and 
    #set last transaction text and s
    #set status to true
    st.session_state.total_deposites[account['Account Number']] += amount
    st.session_state.last_transaction = f'Deposite {amount}'
    st.session_state.transaction_status = True   
    
def append_transaction(transaction_type, amount, date):
    #Get current user account data
    account_dict = st.session_state.accounts_dict
    account = account_dict[st.session_state.account_used_idx]
    #Store transaction data 
    #as string with 2 decimal points into history list
    st.session_state.transaction_history.insert(0, {
        'Account Number' :  account['Account Number'],
        'Transaction Type' : transaction_type,
        'Amount' : f"{amount:.2f}",
        'Date' : date,
        'Balance After Transaction' : f"{account['Balance']:.2f}" 
    })
    
def display_current_balance():
    account_dict = st.session_state.accounts_dict
    account = account_dict[st.session_state.account_used_idx]
    st.write(f"Current Balance: {account['Balance']}")
    
def create_atm_operations():
    #Create 2 columns for the UI layout
    col1, col2 = st.columns(2)
    
    perform_operation = None
    
    amount = 0
    
    with col1:
        #Display selectbox for operation and number input for amount
        operation = st.selectbox("Select Operation: ", ['Withdraw', 'Deposite', 'Check Balance'])
        
        if not operation == 'Check Balance':
            amount = st.number_input("Amount: ")
        
        #Button to perform the selected operation
        perform_operation = st.button("Perform Operation")
        
        #Check if perform button pressed to show loading spinner
        if perform_operation:
            with st.spinner("Processing your transaction... Please wait"):
                time.sleep(2) 
                 
        #Check if perform button pressed and amount less than or equal to 0
        if perform_operation and amount <= 0 and operation != 'Check Balance':
            st.error('Invalid deposite or withdraw amount')
            st.session_state.transaction_status = False
            
        #Check if perform button pressed to match operation type
        elif perform_operation:
            match operation:
                case 'Withdraw':
                    withdraw(amount)
                case 'Deposite':
                    deposite(amount)
                    
            #Call append function to save transaction details into history
            if st.session_state.transaction_status and not operation == 'Check Balance':
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                append_transaction(operation, amount, time_now)
    
    #Check if perform button pressed to display details in column 2
    if perform_operation:
        with col2:
            #If operation is just check balance then display only balance not other info
            if operation == 'Check Balance':
                display_current_balance()
            else:
                display_current_balance()
                st.write(f"Last Transaction: {st.session_state.last_transaction}")
                
                #Check transaction status to display success or error message
                if st.session_state.transaction_status == True:
                    st.success('Transaction Completed Successfully!')
                else:
                    st.error('Transaction failed')
     
def display_account_info():
    #Get current user data and account number
    account_dict = st.session_state.accounts_dict
    account = account_dict[st.session_state.account_used_idx]
    
    account_num = account['Account Number']
    
    #Get total deposites and withdrawals or set to 0 if not found
    total_dep = st.session_state.total_deposites.get(account_num, 0)
    total_wit = st.session_state.total_withdraw.get(account_num, 0)
    
    #Display customer data with 2 decimal points format
    st.write(f"Customer Name: {account['Customer Name']}")
    st.write(f"Account Number: {account_num}")
    st.write(f"Current Balance: {account['Balance']:.2f}")
    st.write(f"Total Deposites: {total_dep:.2f}")
    st.write(f"Total Withdraw: {total_wit:.2f}") 

def display_transaction_history():
    #List to store transactions for current account number
    transaction_history_account_num = []
    account_dict = st.session_state.accounts_dict
    account = account_dict[st.session_state.account_used_idx]
    current_acc_num = account['Account Number']
    
    #Loop through history to find transactions that match current account number
    for transaction in st.session_state.transaction_history:
        if transaction['Account Number'] == current_acc_num:
            transaction_history_account_num.append(transaction)
        
    #Check if history list is not empty 
    #to display table or show warning message
    if len(transaction_history_account_num) != 0:
        st.table(transaction_history_account_num)
    else:
        st.warning('Currently there are no transactions')

#Display login function inside tab 1
with tab1:
    customer_login()
    
#Display atm operations function inside tab 2 
#if logged in else show warning
with tab2:
    if st.session_state.logged_in:
        create_atm_operations()
    else:
        st.warning('Please login first before using atm operations')
        
#Display account information function inside tab 3
#if logged in else show warning
with tab3:
    if st.session_state.logged_in:
        display_account_info()
    else:
        st.warning('Please login first to display account information')
        
#Display transaction history function inside tab 4 
#if logged in else show warning
with tab4:
    if st.session_state.logged_in:
        display_transaction_history()
    else:
        st.warning('Please login first to display transaction history')