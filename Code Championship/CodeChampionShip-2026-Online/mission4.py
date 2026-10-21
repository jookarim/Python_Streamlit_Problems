import streamlit as st 

#Display app title to maake the user know what the app about
st.title(
    '🎬 StarScreen Cinema 🎬',
    text_alignment='center'
)

#Divider to saperate the application cleanly
st.divider()

#Dict to store seat categories and prices 
#to get price from category in o(1) avarage time

seats_prices = {
    'Standard' : 90,
    'Premium' : 130,
    'IMAX' : 180
}

#Colors in a list 
#because each cenima category price 
#needs to be displayed in a different color

colors = [
    'red',
    'green',
    'orange'
]

def display_seats_prices():
    """Function to display seats categories and prices"""
    
    st.header('🎟️ Seat Prices (EGP)')
    
    #Color idx to increase it every iteration 
    #to use different color from colors list
    
    color_idx = 0 
    
    for category, price in seats_prices.items():
        st.markdown(f"- **{category}:** " 
                    f":{colors[color_idx]}[{price}] EGP")
        
        color_idx += 1 
        
    st.divider()

def get_total_price(
    category,
    number_tickets
):
    """Function that uses category and
    number of tickets to return total price"""
    
    category_price = seats_prices[category]
    total_price = category_price * number_tickets 
    return total_price 

def enter_user_data():
    """Function that gets user data and displays total price"""
    
    #2 columns to make seat category enterance col1
    #and number of tickets seat 2
    
    col1, col2 = st.columns(2)
    
    #Enter seat category in col1
    with col1:
        seat_category = st.selectbox(
            'Choose your seat category',
            seats_prices.keys()
        )
    
    #Enter number of tickets in col2
    with col2:
        number_tickets = st.number_input(
            'Number of tickets: ',
            min_value=1,
            max_value=10
        )
    
    calculate_total = st.button('🎉 Calculate Total')
    
    #Check if calculate button pressed
    #if pressed calculate total and display it
    if calculate_total:
        total_price = get_total_price(
            seat_category,
            number_tickets
        )
        
        st.write(f'💰 Total = :green[{total_price}] EGP')
        
display_seats_prices()
enter_user_data()