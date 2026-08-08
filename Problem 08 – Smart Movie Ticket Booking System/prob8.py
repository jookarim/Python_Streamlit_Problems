import streamlit as st

# Create application title
st.title("Smart Movie Ticket Booking System")

st.divider()

# Combo meal price
COMBO_PRICE = 60

# Movies and ticket prices
movies_dict = {
    "Inside Out 2": 120,
    "Minecraft": 150,
    "Sonic 3": 130,
    "Kung Fu Panda 4": 140
}

# Available show times
show_times = [
    "10:00 AM",
    "1:00 PM",
    "4:00 PM",
    "7:00 PM"
]

# Initialize booking report
if 'booking_report_dict' not in st.session_state:
    st.session_state.booking_report_dict = {}
    st.session_state.booking_report_dict['Customer Name '] = []
    st.session_state.booking_report_dict['Movie '] = []
    st.session_state.booking_report_dict['Show Times '] = []
    st.session_state.booking_report_dict['Tickets '] = []
    st.session_state.booking_report_dict['Combo '] = []
    st.session_state.booking_report_dict['Total '] = []

# Initialize total bookings
if 'total_bookings' not in st.session_state:
    st.session_state.total_bookings = 0

# Initialize total tickets sold
if 'count_tickets' not in st.session_state:
    st.session_state.count_tickets = 0

# Initialize movie booking frequency
if 'movies_freq' not in st.session_state:
    st.session_state.movies_freq = {}

# Initialize showtime frequency
if 'show_time_freq' not in st.session_state:
    st.session_state.show_time_freq = {}

# Initialize total ticket sales
if 'ticket_sales' not in st.session_state:
    st.session_state.ticket_sales = 0

# Create application tabs
tab1, tab2, tab3, tab4 = st.tabs([
    'Book tickets',
    'Movie Schedule',
    'Booking Report',
    'Cenima Report'
])


def display_sidebar():
    """
    Display movie prices and cinema rules.
    """

    with st.sidebar:

        # Display movies and prices
        for movie_name, movie_price in movies_dict.items():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.info(movie_name)

            with col2:
                st.info(movie_price)

        st.divider()

        # Display cinema rules
        st.subheader("Cenima Rules")
        st.write("Do not move when the movie is playing")


def is_valid_booking(customer_name, tickets_count):
    """
    Check if booking data is valid.
    """
    return len(customer_name) != 0 and tickets_count > 0


def get_price(movie, tickets_count, combo):
    """
    Calculate booking price.
    """

    price = movies_dict[movie] * tickets_count

    # Add combo price if selected
    if combo == 'Yes':
        price += COMBO_PRICE

    return price


def book_ticket():
    """
    Book movie tickets.
    """

    col1, col2 = st.columns([1, 1])

    # Booking form
    with col1:
        customer_name = st.text_input("Customer Name: ")

        movie = st.selectbox("Movie: ", movies_dict.keys())
        show_time = st.selectbox("Show Time: ", show_times)

        tickets_count = st.number_input(
            "Tickets:",
            step=1
        )

        combo = st.selectbox("Combo: ", [
            'Yes',
            'No'
        ])

        confirm_booking = st.button('Confirm Booking')

    valid_booking = is_valid_booking(customer_name, tickets_count)

    # Booking summary
    with col2:
        st.header("Booking Summary")

        if confirm_booking and valid_booking:

            # Calculate total price
            price = get_price(movie, tickets_count, combo)

            # Update statistics
            st.session_state.total_bookings += 1
            st.session_state.count_tickets += tickets_count
            st.session_state.ticket_sales += price

            # Update movie frequency
            if movie not in st.session_state.movies_freq:
                st.session_state.movies_freq[movie] = 1
            else:
                st.session_state.movies_freq[movie] += 1

            # Update showtime frequency
            if show_time not in st.session_state.show_time_freq:
                st.session_state.show_time_freq[show_time] = 1
            else:
                st.session_state.show_time_freq[show_time] += 1

            # Save booking
            st.session_state.booking_report_dict['Customer Name '].append(customer_name)
            st.session_state.booking_report_dict['Movie '].append(movie)
            st.session_state.booking_report_dict['Show Times '].append(show_time)
            st.session_state.booking_report_dict['Tickets '].append(tickets_count)
            st.session_state.booking_report_dict["Combo "].append(
                "Added" if combo == "Yes" else "Not Added"
            )
            st.session_state.booking_report_dict['Total '].append(price)

            # Display booking summary
            st.write(f"Customer: {customer_name}")
            st.write(f"Movie: {movie}")
            st.write(f"Show Time: {show_time}")
            st.write(f"Tickets: {tickets_count}")

            if combo == 'Yes':
                st.write("Combo: Added")
            else:
                st.write("Combo not added")

            st.write(f"Total: {price} EGP")

            st.success("Booking Confirmed")

        elif confirm_booking and not valid_booking:
            st.error("Invalid Booking")


def display_movies_schedule():
    """
    Display movie schedule.
    """

    col1, col2, col3 = st.columns([1, 1, 1])

    # Display movie names
    with col1:
        for movie_name in movies_dict.keys():
            st.write(movie_name)

    # Display ticket prices
    with col2:
        for ticket_price in movies_dict.values():
            st.write(ticket_price)

    # Display show times
    with col3:
        for _ in movies_dict:
            st.write(" | ".join(show_times))


def get_max_used_showtime():
    """
    Return the most used showtime.
    """

    max_showtime_name = ""
    max_showtime_freq = 0

    for key, value in st.session_state.show_time_freq.items():
        if value > max_showtime_freq:
            max_showtime_name = key
            max_showtime_freq = value

    return max_showtime_name


def get_max_booked_movie():
    """
    Return the most booked movie.
    """

    max_booked_movie_name = ""
    max_book_movie_freq = 0

    for key, value in st.session_state.movies_freq.items():
        if value > max_book_movie_freq:
            max_booked_movie_name = key
            max_book_movie_freq = value

    return max_booked_movie_name


def display_booking_report():
    """
    Display booking report.
    """

    #if booking_dict_report len is 0 
    #then display that no booking has been made yet 
    #else display the table
    
    if len(st.session_state.booking_report_dict) == 0:
        st.write('No Booking has been made yet')
    else:
        st.table(st.session_state.booking_report_dict)


def display_daily_cenima_report():
    """
    Display daily cinema statistics.
    """

    st.header("Daily Cenima Report")

    most_booking_movie = get_max_booked_movie()
    most_used_showtime = get_max_used_showtime()

    st.write(f"Total number of bookings: {st.session_state.total_bookings}")
    st.write(f"Total tickets sold: {st.session_state.count_tickets}")
    st.write(f"Total Tickets Sales: {st.session_state.ticket_sales}")
    st.write(f"Most Booked Movie: {most_booking_movie}")
    st.write(f"Most Used Showtime: {most_used_showtime}")


# Display sidebar
display_sidebar()

# Book tickets tab
with tab1:
    book_ticket()

# Movie schedule tab
with tab2:
    display_movies_schedule()

# Booking report tab
with tab3:
    display_booking_report()

# Daily cinema report tab
with tab4:
    display_daily_cenima_report()