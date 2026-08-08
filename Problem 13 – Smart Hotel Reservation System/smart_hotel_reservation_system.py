import streamlit as st
from datetime import datetime

st.title('Smart Hotel Reservation System')

BREAKFAST_PRICE = 250

tab1, tab2, tab3, tab4 = st.tabs([
    'Make Reservation',
    'Available Rooms',
    'Cancel Reservation',
    'Reservation Summary' 
])

hotel_rooms = {
    'Standard' : 1200,
    'Deluxe' : 1800,
    'Family' : 2500,
    'Suite' : 4000
}

start_available_rooms = {
    'Standard' : 10,
    'Deluxe' : 6,
    'Family' : 4,
    'Suite' : 2
}

if 'available_rooms' not in st.session_state:
    st.session_state.available_rooms = {
        'Standard' : 10,
        'Deluxe' : 6,
        'Family' : 4,
        'Suite' : 2
    }

if 'reservation_data' not in st.session_state:
    st.session_state.reservation_data = []
    
if 'success_msg' not in st.session_state:
    st.session_state.success_msg = ""
    
def display_sidebar():
    with st.sidebar:
        st.title("🏨 Hotel Stay")
        st.divider()

        st.subheader("⏰ Quick Times")
        st.write("Check-In: 3:00 PM")
        st.write("Check-Out: 11:00 AM")
        st.divider()

        st.subheader("📞 Hotel Info")
        st.write("📍 Address: 123 Main Street")
        st.write("☎️ Phone: +1 234-567-8900")
        st.write("📶 Wi-Fi: Hotel_Guest (Open)")
        st.divider()
        
        st.subheader("🏊 Facilities")
        st.write("Pool: 6 AM – 10 PM")
        st.write("Gym: Open 24 Hours")
        st.write("Restaurant: 7 AM – 11 PM")
        st.write("Parking: Free on-site")
    
def get_available_rooms():
    available_rooms_names = []
    available_rooms_quantity = []
    
    for (
            room_name,
            room_quantity
        ) in st.session_state.available_rooms.items():
            if st.session_state.available_rooms[room_name] >= 0:
                available_rooms_names.append(room_name)
                available_rooms_quantity.append(room_quantity)
    
    return dict(zip(available_rooms_names,available_rooms_quantity))

def validate_reservation(guest_name, number_of_nights):
    return (
                guest_name != "" and 
                number_of_nights > 0
            )

def make_reservation():
    with st.form('Reservation'):
        all_room_types = list(st.session_state.available_rooms.keys())
        
        guest_name = st.text_input('Guest Name: ')
        room_type = st.selectbox("Room Type: ", all_room_types)
        number_of_nights = st.number_input("Number of Nights: ", min_value=1, step=1)
        check_in_date = st.date_input('Check-in Date: ')
        breakfast = st.selectbox("Breakfast: ", ['Yes', 'No'])
        
        reserve_room = st.form_submit_button("Reserve Room")
        
        if reserve_room:
            if st.session_state.available_rooms.get(room_type, 0) > 0:
                valid_reservation = validate_reservation(guest_name, number_of_nights)
                
                if valid_reservation:
                    st.session_state.available_rooms[room_type] -= 1
                    
                    st.session_state.reservation_data.insert(0, {
                        "Guest Name" : guest_name, 
                        "Room Type" : room_type,
                        "Number of Nights" : number_of_nights,
                        "Check-In Date" : check_in_date,
                        "Breakfast" : "Has Breakfast" if breakfast == 'Yes' else 'No Breakfast'
                    })
                    
                    if st.session_state.available_rooms[room_type] == 1:
                        st.warning(f"Only 1 room of {room_type} remains")
                    
                    st.success("Reservation Completed successfully")
                    
                    room_cost = (hotel_rooms[room_type] * number_of_nights)
                    breakfast_cost = (BREAKFAST_PRICE * number_of_nights if breakfast == 'Yes' else 0)
                    final_cost = room_cost + breakfast_cost
                    
                    st.write(f"Room Cost: {room_cost}")
                    st.write(f"Breakfast: {breakfast_cost}")
                    st.write(f"Final Cost: {final_cost}")
                else:
                    st.error('Invalid reservation data. Please verify your inputs.')
            else:
                st.warning("All rooms of this type are already reserved!")

            
def display_available_rooms():
    available_rooms = get_available_rooms()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Room Type**")
    
    with col2:
        st.write("**Price/Night**")
    
    with col3:
        st.write("**Available**")
        
        
    with col2:
        for (
            available_room_name,
            available_room_quantity
        ) in available_rooms.items():
            
                with col1:
                    st.write(available_room_name)
                with col2:
                    st.write(hotel_rooms[available_room_name])
                with col3:
                    st.write(available_room_quantity)
        
def cancel_reservation():
    guest_name = st.text_input("Guest Name: ")
    available_rooms = get_available_rooms().keys()
    room_type = st.selectbox("Room Types", available_rooms)
    cancel_clicked = st.button("Cancel Reservation")
    canceled_reservation_idx = -1
    
    if cancel_clicked:
        for i in range(len(st.session_state.reservation_data)):
            if (
                cancel_clicked and
                guest_name == st.session_state.reservation_data[i]['Guest Name'] and 
                room_type == st.session_state.reservation_data[i]['Room Type'] 
            ):
                canceled_reservation_idx = i
                break


        if canceled_reservation_idx != -1 and (
            start_available_rooms[room_type] > 
            st.session_state.available_rooms[room_type]):
            
            st.session_state.reservation_data.remove(
                st.session_state.reservation_data[canceled_reservation_idx]
            )
            
            st.session_state.success_msg = "Reservation Canceled Successfully"
            st.session_state.available_rooms[room_type] += 1
        
            st.rerun()
            
        elif guest_name == "":
            st.error("Information are invalid")
                    
        elif (
                start_available_rooms[room_type] <=
                st.session_state.available_rooms[room_type]
            ):
                st.warning('Rooms are already canceled')
        
        if canceled_reservation_idx == -1:
            st.warning('User currently is not in reservation list')
          
def display_reservation_summary():
    if len(st.session_state.reservation_data) == 0:
        st.info("No Reservations has been made yet")
    else:
        col1, col2 = st.columns(2)
        
        reservation_data = st.session_state.reservation_data[0]
        
        with col1:
            st.header("Reservation Information")
            st.write(f"Guest Name: {reservation_data['Guest Name']}")
            st.write(f"Room Type: {reservation_data['Room Type']}")
            st.write(f"Number of nights: {reservation_data['Number of Nights']}")
            st.write(f"Check-In Date: {reservation_data['Check-In Date']}")
        
        with col2:
            st.header('Cost Information')
            
            st.write("Price per night:" 
                    f"{hotel_rooms[reservation_data['Room Type']]}")
            
            room_cost = (hotel_rooms[reservation_data['Room Type']] * 
                        reservation_data['Number of Nights'])
            
            st.write(f"Room Cost: {room_cost}")
            
            st.write(f"Breakfast Status: {reservation_data['Breakfast']}")
            
            breakfast_price = (reservation_data['Number of Nights'] * BREAKFAST_PRICE
                            if reservation_data['Breakfast'] == 'Has Breakfast' 
                            else 0)
            
            st.write(f"Breakfast Cost: {breakfast_price}")
            
            st.write(f"Final Total: {breakfast_price + room_cost}")
            
            st.write("Reservation State: Confirmed")
        
        left, mid, right = st.columns([1,2,1])
        
        with mid:
            st.code("=====================================\n"
                    "Reservation Summary\n"
                    "=====================================\n"
                    f"Guest: {reservation_data['Guest Name']}\n"
                    f"Room: {reservation_data['Room Type']}\n"
                    f"Check-in: {reservation_data['Check-In Date']}\n"
                    f"Nights: {reservation_data['Number of Nights']}\n"
                    f"Breakfast: {reservation_data['Breakfast']}\n"
                    f"Final Cost: {breakfast_price + room_cost}\n"
                    "Reservation Status: Confirmed\n"
                    "=====================================\n")

with tab1:
    make_reservation()
    
with tab2:
    display_available_rooms()
    
with tab3:
    cancel_reservation()

    if st.session_state.success_msg == "Reservation Canceled Successfully":
        st.success(st.session_state.success_msg)
        del st.session_state.success_msg
            
with tab4:
    display_reservation_summary()
    
display_sidebar()