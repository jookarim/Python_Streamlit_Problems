import streamlit as st
import time

st.title('Smart Car Rental System')

GPS_NAVIGATION_COST = 150

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Rent a Car', 'Available Cars', 'Return a Car', 'Rental Summary', 'Rental Managament dashboard'])

st.divider()

available_cars = {
    'Toyota Corolla' : 850,
    'Hyundai Elantra' : 950,
    'Kia Sportage' : 1400,
    'Nissan Sunny' : 800,
    'BMW X3' : 2500 
}

if 'rented_cars' not in st.session_state:
    st.session_state.rented_cars = set()
    
if 'user_rent_data' not in st.session_state:
    st.session_state.user_rent_data = []

if 'return_success_msg' not in st.session_state:
    st.session_state.return_success_msg = ""
        
def display_sidebar():
    with st.sidebar:
        st.header('Rental Rules')
        st.info('Get the car back after the rental time ends')
        st.info('Keep the car clean and unbroken')
        st.divider()
        
        st.info(
            "Rental Company Info: "
            "Youssef Company for Rental has been providing reliable rental services" 
            "since 1945."
        )

def is_valid_car_rental(customer_name, rantal_days):
    return len(customer_name) != 0 and rantal_days > 0

def rent_car():
    with st.form('Rent Car'):
        customer_name = st.text_input('Customer Name: ')
        car = st.selectbox('Select Car: ', available_cars.keys())
        rental_days = st.number_input('Rental Days: ')
        gps_navigation = st.selectbox('GPS Navigation: ', ['Yes', 'No'])
        rental_start_date = st.date_input('Rental start date: ')
        confirm_rental = st.form_submit_button('Confirm rental')
        
        valid_car_rental = is_valid_car_rental(customer_name, rental_days)
        
        if confirm_rental:
            if not valid_car_rental:
                st.error('Rental is invalid')
            elif car in st.session_state.rented_cars:
                st.warning(f'{car} is already rented')
            else:
                rental_cost = available_cars[car] * rental_days
                
                if gps_navigation == 'Yes':
                    rental_cost += GPS_NAVIGATION_COST
                    
                rental_status = True
                
                if gps_navigation == 'Yes':
                    st.session_state.user_rent_data.insert(0, 
                        {
                            'Customer Name': customer_name,
                            'Car': car,
                            'Rental Days': rental_days,
                            'Rental Start Date': rental_start_date,
                            'Price Per Day': available_cars[car],
                            'GPS Status': 'Has GPS',
                            'Basic Rental Cost': rental_cost - GPS_NAVIGATION_COST,
                            'GPS Cost': GPS_NAVIGATION_COST,
                            'Final Total': rental_cost,
                            'Rental Status': rental_status
                        }
                    )
                    
                else:
                    st.session_state.user_rent_data.insert(0, {
                        'Customer Name': customer_name,
                        'Car': car,
                        'Rental Days': rental_days,
                        'Rental Start Date': rental_start_date,
                        'Price Per Day': available_cars[car],
                        'GPS Status': 'No GPS',
                        'Basic Rental Cost': rental_cost,
                        'GPS Cost': 0,
                        'Final Total': rental_cost,
                        'Rental Status': rental_status
                    })
                    
                            
                st.session_state.rented_cars.add(car)

                with st.spinner('Confirming your rental'):
                    time.sleep(2)

                    st.success('Rental Confirmed Successfully')
            
def display_available_cars():
    col1, col2, col3 = st.columns(3)
    
    for car, price in available_cars.items():
        with col1:
            st.write(f'Car: {car}')
        with col2:
            st.write(f'Price/Day: {price} LE')
        with col3:
            if car in st.session_state.rented_cars:
                st.write('Rented')
            else:
                st.write('Available')

def return_car():
    st.header('Return Car')

    customer_name = st.text_input('Customer Name: ')
    car = st.selectbox("Car: ", available_cars.keys())
    submit_return = st.button('Return Car')
    user_rent_data = None

    for user in st.session_state.user_rent_data:
        if (user['Car'] == car and 
            user['Customer Name'] == customer_name
        ):
            user_rent_data = user
            break    
    
    if user_rent_data == None:
        st.info("No active rentals.")
        return
    
    if (
        customer_name == user_rent_data['Customer Name'] 
        and submit_return):
        
        if car in st.session_state.rented_cars:
            st.session_state.rented_cars.remove(car)
            user_rent_data['Rental Status'] = False    
            st.session_state.return_success_msg = f'{car} is Currently available'
            st.rerun()
        elif car not in st.session_state.rented_cars:
            st.warning('Car is already available')
    elif submit_return:
        st.error('Invalid Customer')
    
    if 'return_success_msg' in st.session_state:
        st.success(st.session_state.return_success_msg)
        st.session_state.return_success_msg = ""
        
def display_rental_summary():
    col1, col2 = st.columns(2)

    if not len(st.session_state.user_rent_data):
        return
    
    user_rent_data = st.session_state.user_rent_data[0]

    if not user_rent_data:
        st.warning("No rental summary available yet.")
        return

    with col1:
        st.subheader("Rental Information")

        st.write(f"Customer Name: {user_rent_data['Customer Name']}")
        st.write(f"Car: {user_rent_data['Car']}")
        st.write(f"Rental Days: {user_rent_data['Rental Days']}")
        st.write(f"Rental Start Date: {user_rent_data['Rental Start Date']}")

    with col2:
        st.subheader("Cost Information")

        st.write(f"Price Per Day: {user_rent_data['Price Per Day']} LE")
        st.write(f"Basic Rental Cost: {user_rent_data['Basic Rental Cost']} LE")
        st.write(f"GPS Status: {user_rent_data['GPS Status']}")
        st.write(f"GPS Cost: {user_rent_data['GPS Cost']} LE")
        st.write(f"Final Total: {user_rent_data['Final Total']} LE")
        st.write(f"Rental Status: {user_rent_data['Rental Status']}")

    st.divider()

    left, mid_col, right = st.columns([1, 2, 1])

    with mid_col:
        st.code(
            "=================================\n"
            "Rental Summary\n"
            "=================================\n"
            f"Customer : {user_rent_data['Customer Name']}\n"
            f"Car : {user_rent_data['Car']}\n"
            f"Rental Days : {user_rent_data['Rental Days']}\n"
            f"Rental Date : {user_rent_data['Rental Start Date']}\n"
            f"GPS : {user_rent_data['GPS Status']}\n"
            f"Final Cost : {user_rent_data['Final Total']} EGP\n"
            f"Status : {user_rent_data['Rental Status']}\n"
            "================================="
        )

def rental_management_dashboard():
    st.header("Rental Management Dashboard")

    rentals = st.session_state.user_rent_data

    if len(rentals) == 0:
        st.warning("No rentals yet.")
        return

    st.write(f"Total Rentals: {len(rentals)}")

    total_income = 0

    for user in rentals:
        total_income += user["Final Total"]

    st.write(f"Total Income: {total_income} LE")

    car_count = {}

    for user in rentals:
        car = user["Car"]

        if car not in car_count:
            car_count[car] = 0

        car_count[car] += 1

    most_rented_car = ""
    max_times = 0

    for car, count in car_count.items():
        if count > max_times:
            max_times = count
            most_rented_car = car

    st.write(
        f"Most Rented Car: {most_rented_car} "
        f"({max_times} rentals)"
    )

    available = []

    for car in available_cars:
        if car not in st.session_state.rented_cars:
            available.append(car)

    st.write(f"Available Cars ({len(available)}):")

    for car in available:
        st.write(f"• {car}")

    rented = list(st.session_state.rented_cars)

    st.write(f"Rented Cars ({len(rented)}):")

    for car in rented:
        st.write(f"• {car}")

    total_days = 0

    for user in rentals:
        total_days += user["Rental Days"]

    average_days = total_days / len(rentals)

    st.write(
        f"Average Rental Duration: "
        f"{average_days:.2f} days"
    )

    highest_customer = ""
    highest_bill = 0

    for user in rentals:
        if user["Final Total"] > highest_bill:
            highest_bill = user["Final Total"]
            highest_customer = user["Customer Name"]

    st.write(
        f"Highest Rental Bill: "
        f"{highest_customer} ({highest_bill} LE)"
    )
    
display_sidebar()

with tab1:
    rent_car()
    
with tab2:
    display_available_cars()
    
with tab3:
    return_car()
    
with tab4:
    display_rental_summary()
    
with tab5:
    rental_management_dashboard()