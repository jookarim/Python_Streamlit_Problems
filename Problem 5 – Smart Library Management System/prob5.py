import streamlit as st

#Display application title
st.title("Smart Library Management System")
st.divider()

#Initialize action is session state (borrow or return)
if "action" not in st.session_state:
    st.session_state.action = 'None'

#Initialize books dict in session state 
#to enable adding and minus quantity with reset

if "books" not in st.session_state:
    st.session_state.books = {
        "Python Basics": 5,
        "Data Science": 3,
        "Machine Learning": 2,
        "Web Development": 4,
    }

#Init count_borrowed and returned 
#to get count borrowed and returned books

if "count_borrowed" not in st.session_state:
    st.session_state.count_borrowed = 0

if "count_returned" not in st.session_state:
    st.session_state.count_returned = 0

#List to store borrowed and returned books
if "borrowed_returned_books" not in st.session_state:
    st.session_state.borrowed_returned_books = []

#Init cols col1 for action choose and 
#col2 for book selection, statistics and borrowing, return history
col1, col2 = st.columns(2)

def count_books():
    """Function to count books""" 
    count = 0
    
    #Loop through books dict values because 
    #value has quantity for each book
    
    for val in list(st.session_state.books.values()):
        count += val
        
    return count

def display_sidebar():
    """Display sidebar"""
    with st.sidebar:
        #Display library rules and working hours
        
        st.header("Library Rules")
        st.info("Return books on time")
        st.info("Handle books carefully")

        st.divider()

        st.subheader("Working Hours")
        st.info("9:00 AM - 6:00 PM")

        st.divider()
        
        count = count_books()
        
        st.info(f"Available Books: {count}")
        
def get_action_selection():
    """Make checkbox for action selection borrow or return"""
    with col1:
        action = st.selectbox("Choose Action",
        ["Borrow Book", "Return Book", "View Books"])

        #set action in session state to new action 
        #when submit pressed
        if st.button("Submit"):
            st.session_state.action = action

def borrow_book():
    """Borrow selected book"""
    with col2:
        st.header("Borrow Book")

        #Select book from the books dict keys
        book = st.selectbox("Select Book",
                            list(st.session_state.books.keys()),
                            key="borrow_book")

        #Check if borrow button pressed
        if st.button("Borrow"):
            #if quantity > 0 decrease it
            if st.session_state.books[book] > 0:
                st.session_state.books[book] -= 1

                #Display count of available copies
                st.write(f"Available Copies: {st.session_state.books[book]}")

                #Success borrow completed successfully
                st.success("Borrow completed successfully!")
                
                #Increase count borrowed
                st.session_state.count_borrowed += 1
                #add action to borrowed returned book list
                st.session_state.borrowed_returned_books.append(f"Borrowed {book}")
        
            else:
                #If copies = 0 then display error no copies available
                st.error("No copies available.")
                
            #Give user warning when 1 book remaining
            if st.session_state.books[book] == 1:
                st.warning("Only 1 book remaining")

def view_books():
    """Function to view books as table"""
    
    with col2:
        st.table(st.session_state.books)
    
def return_book():
    """Return selected book"""
    with col2:
        st.header("Return Book")

        #Select book from the books dict keys
        book = st.selectbox("Select Book", 
                            list(st.session_state.books.keys()),
                            key="return_book"
                            )

        #Check if return button pressed
        if st.button("Return"):
            #Increase available copies
            st.session_state.books[book] += 1

            #Display count of available copies
            st.write(f"Available Copies: {st.session_state.books[book]}")

            #Success return completed successfully
            st.success("Return completed successfully!")

            #Increase count returned
            st.session_state.count_returned += 1

            #Add action to borrowed returned book list
            st.session_state.borrowed_returned_books.append(f"Returned {book}")


def display_statistics():
    """Display borrowing and returning statistics"""
    with col2:
        st.divider()
        st.header("Statistics")

        #Display borrowed books count
        st.write(f"Borrowed Books: {st.session_state.count_borrowed}")

        #Display returned books count
        st.write(f"Returned Books: {st.session_state.count_returned}")


def display_borrowing_history():
    """Display borrowing and returning history"""
    with col2:
        st.divider()
        st.header("Borrowing History")

        #Check if there are any transactions
        if st.session_state.borrowed_returned_books:

            #Display all borrow and return actions
            for item in st.session_state.borrowed_returned_books:
                st.write(item)
        else:
            #Display message if no transactions exist
            st.write("No transactions yet.")


#Display sidebar
display_sidebar()

#Display action selection
get_action_selection()

#Call borrow functions when borrow action selected
if st.session_state.action == "Borrow Book":
    borrow_book()
    display_statistics()
    display_borrowing_history()

#Call return functions when return action selected
elif st.session_state.action == "Return Book":
    return_book()
    display_statistics()
    display_borrowing_history()
    
elif st.session_state.action == "View Books":
    view_books()
    display_statistics()
    display_borrowing_history()