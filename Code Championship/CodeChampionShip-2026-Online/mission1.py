import streamlit as st 

#Display title to make user about (what the app is used for)
st.title('🎈 Escape the room 🎈', text_alignment='center')

#Divider to saperate title from other widgets
st.divider()

#Tickets prices dictionary to set each category to its price
tickets_prices = {
    'Kids' : 150,
    'Adults' : 120,
    'VIP' : 200
}

#Text colors when displaying prices of the categories 
#first green
#second blue
#third orange

text_colors = [
    'green',
    'blue',
    'orange'
]

def display_ticket_prices():
    """Display tickets prices to make the user know 
    what price he is going to pay"""
    
    #Header for clearness
    st.header('🎟️ Ticket Prices (EGP): ')
    
    #Color index to display specific color for each category   
    colors_idx = 0 
    
    #Loop through items, price dict to display category and price 
    #with specific color 
    
    for category, price in tickets_prices.items():
        st.markdown(
            f"- **{category}:** " 
            f":{text_colors[colors_idx]}[{price}] EGP"
        )
        
        colors_idx += 1 
        
    st.divider()

def calculate_total_price(
    ticket_type: str,
    number_of_tickets: int
) -> int:
    """Calculate total price using type price X count of tickets"""
    
    return tickets_prices[ticket_type] * number_of_tickets

def book_ticket():
    """2 columns to get ticket type from first col"""
    """Number of tickets from second column"""
    
    col_type, col_count = st.columns(2)
    
    #Get ticket type from user
    with col_type:
        ticket_type = st.selectbox(
                                    'Choose your ticket type: ',
                                    tickets_prices.keys()
                                )
    
    #Take number of tickets from user
    with col_count:
        number_of_tickets = st.number_input(
                                'Number of tickets: ', 
                                step=1,
                                min_value=1
                            )
    
    #Button for calculating total price
    calculate_total_button = st.button(
        '🎉 Calculate Total'
    )
    
    if calculate_total_button:
        #Display total price by getting ticket type and count tickets
        
        total_price = calculate_total_price(
            ticket_type,
            number_of_tickets
        )

        st.write(f'💰 Total = {total_price} EGP')


#Call the 2 functions that display tickets prices and the book ticket
display_ticket_prices()
book_ticket()