import streamlit as st

#Display the title to make the user know what is the app about
st.title('🍔 BurgerX Cashier System 🍔')

#Chicken burgers names,prices to get price using name
chicken_burgers = {
    'Chicken Classic': 120,
    'Chicken Ranch': 140,
    'Chicken Cheese': 155
}

#Beef burgers names,prices to get price using name
beef_burgers = {
    'Beef Classic': 150,
    'Beef BBQ': 170,
    'Beef Cheese': 185
}

#Combos names,prices to get price using name (None if no combo)
combos = {
    'Fries & Cola': 65,
    'Fries & Juice': 75,
    'None': 0
}

#List to choose from where the user knew about BurgerX
from_where_know_us = [
    'Social media',
    'Friend',
    'AI suggestion',
    'Other'
]

def display_sidebar():
    """Display sidebar 
    (User enters data and where he knew about the resturant)"""
    
    with st.sidebar:
        st.header('🤦🏿‍♂️Customer information')
        
        customer_name = st.text_input(
            '👱 Customer Name', 
            placeholder="Enter customer name"
        )
        
        phone_number = st.text_input(
            "📞 Phone Number",
            placeholder="Enter phone number"
        )
        
        from_where = st.selectbox(
            'From where you know us?',
            from_where_know_us
        )
        
        #Suggestion to help the resturant enhance 
        #and correct its mistakes
        #Text area for multiline text
        customer_suggestion = st.text_area(
            'Customer suggestions',
            placeholder='Enter suggestion or special requists...'
        )
        
        
def display_menu():
    """Function to display the menu food name -> Price"""
    
    #2 columns to display chicken burgers in a column 
    #and beef burgers in the other column 
    
    col1, col2 = st.columns(2, border=True)
    
    with col1:
        st.header('🍗 Chicken Burger')
        
        for burger_name, burger_price in chicken_burgers.items():
            st.markdown(f"- * {burger_name} -> {burger_price} EGP *")
    
    with col2:
        st.header('🥩 Beef Burger')
                
        for burger_name, burger_price in beef_burgers.items():
            st.markdown(f"- * {burger_name} -> {burger_price} EGP *")

def create_order():
    """Function to create order and displays output +
    discount if found"""
    
    #Slider to let the user enter any count of burgers (0,20)
    number_of_burgers = st.slider('Number of burgers 🍔',
                                    min_value=0,
                                    max_value=20
                                )
    st.divider()
    
    total_price = 0 
    
    #Take burger and combo from user 
    #and display subtotal and adds to final total
    
    for i in range(number_of_burgers):
        st.header(f'🍔 Burger #{i + 1}')
        
        #2 Columns 1 for burger and 1 for combo for clean looking app
        col1, col2 = st.columns(2)
        burgers_options = (list(chicken_burgers.keys()) + 
                        list(beef_burgers.keys()))
        
        with col1:
            burger = st.selectbox(
                key=f"Burger #{i}",
                label='Burger: ',
                options=burgers_options
            )
            
        with col2:
            combo = st.selectbox(
                key=f'Combo #{i}',
                label='Combo: ',
                options=combos
            )
        
        #Calculate subtotal
        burger_price = 0 
        
        if burger in chicken_burgers:
            burger_price = chicken_burgers[burger]
        else:
            burger_price = beef_burgers[burger]
        
        burger_price += combos[combo]
        
        #Add to final total
        total_price += burger_price 
        
        st.write(f'Subtotal: {burger_price} EGP')
        
    st.divider()
    
    #Button that when pressed calculate final total
    calculate_order = st.button(
        '💰 Calculate Order',
        type='primary',
        width='stretch'
    )

    if calculate_order:
        #Display total without discount if total price <= 250
        if total_price <= 250:
            total_price_text = (
                f"📃 Order Total: {total_price} EGP| "
                f"💰 Final Price: {total_price} EGP"
            )
            
            st.success(total_price_text)
            
        #Display total price - discount if total price > 250
        else:
            discount = total_price * 0.1 
            
            price_after_discount = total_price - discount 
            
            total_price_text = (
                f"📃 Order Total: {total_price} EGP| "
                f"🎉 10% discount Discount: {discount} EGP| "
                f"💰 Final price: {price_after_discount} EGP"
            )

            st.success(total_price_text)
          
display_sidebar()
display_menu()
create_order()
