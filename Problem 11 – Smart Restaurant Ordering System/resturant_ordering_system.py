import streamlit as st
import time

PRICE_DISCOUNT_MIN = 300
PREPARE_ORDER_TIME = 2

if 'bill' not in st.session_state:
    st.session_state.bill = 0
    
if 'discount' not in st.session_state:
    st.session_state.discount = 0

if 'orders' not in st.session_state:
    st.session_state.orders = []
    
st.title("🍔 Smart Restaurant Ordering System")
st.divider()

st.header('Orders')
if len(st.session_state.orders):
    st.table(st.session_state.orders)
else:
    st.info('There is no order yet')
    
tab1, tab2, tab3, tab4 = st.tabs(['New Order', 'Menu', 'Bill', 'Daily Sales Report'])

meals = {
    'Burger' : 180,
    'Pizza' : 220,
    'Pasta' : 170,
    'Fried Chicken' : 200 
}

drinks = {
    'Cola' : 35, 
    'Orange juice' : 45,
    'Water' : 20,
    'Coffee' : 50
}

desserts = {
    'Ice Cream' : 60,
    "Cake" : 70,
    "Donut" : 45
}

def display_sidebar():
    with st.sidebar:
        st.write("Today's special")
        st.info('Restaurant Opens from 7:00 am to 1:00 am')
        st.info("Best Restaurant ever")
        
def buy_new_order():
    with st.form('New Order Form'):
        customer_name = st.text_input('Customer Name: ')
        main_meal = st.selectbox("Main meal: ", meals.keys())
        drink = st.selectbox('Drink: ', drinks.keys())
        dessert = st.selectbox('Dessert: ', ['No Dessert'] + list(desserts.keys()))
        place_order = st.form_submit_button('Place Order')

    if place_order and dessert == 'No Dessert':
        st.warning('Dessert would be better for you')
        
    if place_order and not len(customer_name) == 0:
        meal_p = meals.get(main_meal, 0)
        drink_p = drinks.get(drink, 0)
        dessert_p = desserts.get(dessert, 0)
        
        orig_total = meal_p + drink_p + dessert_p
        
        if orig_total >= PRICE_DISCOUNT_MIN:
            disc_amount = orig_total / 10
        else:
            disc_amount = 0
            
        fin_total = orig_total - disc_amount
            
        st.session_state.orders.insert(0, {
            'Customer Name' : customer_name,
            'Meal' : main_meal,
            'Drink' : drink,
            'Dessert' : dessert,
            'Meal Price' : meal_p,
            'Drink Price' : drink_p,
            'Dessert Price' : dessert_p,
            'Original Total' : orig_total,
            'Discount' : disc_amount, 
            'Final Total' : fin_total
        })
            
        with st.spinner("Preparing the order... "):
            time.sleep(PREPARE_ORDER_TIME)
        
        st.success('Order is prepared successfully!')
        
        st.rerun()
        
    elif place_order:
        st.error('Customer name is invalid')
        
def display_menu():
    st.header('Menu')
    
    st.subheader('Main Meals')
    for meal in meals.items():
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{meal[0]}")
        with col2:
            st.write(f"{meal[1]} LE")
            
    st.subheader('Drinks')
    for drink in drinks.items():
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{drink[0]}")
        with col2:
            st.write(f"{drink[1]} LE")
    
    st.subheader('Desserts')
    for dessert in desserts.items():
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{dessert[0]}")
        with col2:
            st.write(f"{dessert[1]} LE")

def display_bill():
    if len(st.session_state.orders) == 0:
        st.info('There is no order yet')
    else:
        col1, col2 = st.columns(2)
        current_order = st.session_state.orders[0]
        
        with col1:
            st.write(f"Customer name: {current_order['Customer Name']}")
            st.write(f"Meal: {current_order['Meal']}")
            st.write(f"Drink: {current_order['Drink']}")
            st.write(f"Dessert: {current_order['Dessert']}")
        with col2:
            st.write(f"Meal Price: {current_order['Meal Price']} LE")
            st.write(f"Drink Price: {current_order['Drink Price']} LE")
            st.write(f"Dessert Price: {current_order['Dessert Price']} LE")
            st.write(f"Original Total: {current_order['Original Total']} LE")
            st.write(f"Discount: {current_order['Discount']} LE")
            st.write(f"Final Total: {current_order['Final Total']} LE")
            
        st.divider()

        receipt_text = f"""
        ==================================
                ORDER SUMMARY           
        ==================================
        Customer: {current_order['Customer Name']}
        ----------------------------------
        {current_order['Meal']:<18} {current_order['Meal Price']:>6} LE
        {current_order['Drink']:<18} {current_order['Drink Price']:>6} LE
        {current_order['Dessert']:<18} {current_order['Dessert Price']:>6} LE
        ----------------------------------
        Subtotal:          {current_order['Original Total']:>6} LE
        Discount:         {current_order['Discount']:>6} LE
        ==================================
        TOTAL DUE:         {current_order['Final Total']:>6} LE
        ==================================
            Thank you for ordering!
        """ 
        
        st.code(receipt_text, language="text")

def daily_statistics_report():
    total_sales = 0

    most_meals_dict = {}
    most_drinks_dict = {}
    most_desserts_dict = {}
    top_customers_dict = {}

    count_orders = len(st.session_state.orders)

    for order in st.session_state.orders:
        total_sales += order['Final Total']

        if order['Meal'] in most_meals_dict:
            most_meals_dict[order['Meal']] += 1
        else:
            most_meals_dict[order['Meal']] = 1

        if order['Drink'] in most_drinks_dict:
            most_drinks_dict[order['Drink']] += 1
        else:
            most_drinks_dict[order['Drink']] = 1

        if order['Dessert'] != 'No Dessert':
            if order['Dessert'] in most_desserts_dict:
                most_desserts_dict[order['Dessert']] += 1
            else:
                most_desserts_dict[order['Dessert']] = 1

        if order['Customer Name'] in top_customers_dict:
            top_customers_dict[order['Customer Name']] += order['Final Total']
        else:
            top_customers_dict[order['Customer Name']] = order['Final Total']

    most_meal = None
    most_meal_count = 0

    for meal in most_meals_dict:
        if most_meals_dict[meal] > most_meal_count:
            most_meal = meal
            most_meal_count = most_meals_dict[meal]

    most_drink = None
    most_drink_count = 0

    for drink in most_drinks_dict:
        if most_drinks_dict[drink] > most_drink_count:
            most_drink = drink
            most_drink_count = most_drinks_dict[drink]

    most_dessert = None
    most_dessert_count = 0

    for dessert in most_desserts_dict:
        if most_desserts_dict[dessert] > most_dessert_count:
            most_dessert = dessert
            most_dessert_count = most_desserts_dict[dessert]

    top_customer = None
    top_customer_total = 0

    for customer in top_customers_dict:
        if top_customers_dict[customer] > top_customer_total:
            top_customer = customer
            top_customer_total = top_customers_dict[customer]

    return (
        total_sales,
        count_orders,
        most_meal,
        most_drink,
        most_dessert,
        top_customer
    )

def display_daily_statistics_report():
    total_sales,count_orders,most_meal,most_drink,most_dessert,top_customer=daily_statistics_report()
    
    st.header('Daily Statistics Report')
    
    st.write(f"Total Orders: {count_orders:.0f}")
    st.write(f"Total Sales: {total_sales:.2f} LE")
    st.write(f"Most Ordered Meal: {most_meal}")
    st.write(f"Most Ordered Drink: {most_drink}")
    st.write(f"Most Ordered Dessert: {most_dessert}")
    st.write(f"Top Customer: {top_customer}")
    
    if count_orders != 0:
        st.write(f"Avg Order Value: {total_sales / count_orders:.2f}")
    
display_sidebar()
        
with tab1:
    buy_new_order()

with tab2:
    display_menu()

with tab3:
    display_bill()
    
with tab4:
    display_daily_statistics_report()