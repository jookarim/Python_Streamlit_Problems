import streamlit as st 

class Sidebar:
    def __init__(self) -> None:
        self.orders_types = [
            'Dine-In',
            'Takeaway',
            'Delivery',
            'Drive-thru'
        ]

    def display_sidebar(self):
        with st.sidebar:
            customer_name = st.text_input(
                'Customer Name: ',
                placeholder='Enter customer name'
            )
            
            phone_number = st.text_input(
                'Phone Number: ',
                placeholder='Enter phone number'
            )
            
            order_type = st.selectbox(
                'Order type: ',
                self.orders_types
            )
            
            special_requests = st.text_area(
                'Special requests'
            )

class MenuDisplay:
    def __init__(
        self,
        meat_pizza: dict[str, int],
        cheese_pizza: dict[str, int]
    ):
        self._meat_pizza = meat_pizza 
        self._cheese_pizza = cheese_pizza 
    
    def _display_pizza_type(
        self,
        pizza_data: dict[str, int]
    ):
        for pizza, price in pizza_data.items():
            st.markdown(f"- {pizza} -> {price} EGP")  
            
    def display_menu(self):
        col1, col2 = st.columns(2, border=True)
        
        with col1:
            st.header('Cheese Pizza')
        
            self._display_pizza_type(
                self._cheese_pizza
            )
        
        with col2:
            st.header('Meat Pizza')
            
            self._display_pizza_type(
                self._meat_pizza
            )
    
class EnteranceSystem:
    def __init__(
        self,
        meat_pizzas: dict[str, int],
        cheese_pizzas: dict[str, int],
        sizes: dict[str, int]
    ):
        self.meat_pizzas = meat_pizzas 
        self.cheese_pizzas = cheese_pizzas
        self.sizes = sizes 
        
    def _get_count_pizzas(self):
        count_slider_value = st.slider(
            'Number of pizzas',
            min_value=1,
            max_value=10
        )
        
        return count_slider_value 

    def _calculate_price(
        self,
        pizza_type,
        pizza_size
    ):
        pizza_price = 0 
                    
        if pizza_type in self.cheese_pizzas:
            pizza_price = self.cheese_pizzas[pizza_type]
        else:
            pizza_price = self.meat_pizzas[pizza_type]
            
        pizza_price += self.sizes[pizza_size]
        
        return pizza_price 
    
    def enter_pizzas(self):
        count_pizzas = self._get_count_pizzas()
        
        total_price = 0 
        
        for i in range(count_pizzas):
            st.header(f'Pizza #{i + 1}')
            
            col1, col2 = st.columns(2)
            
            with col1:
                pizza_type = st.selectbox(
                    'Pizza: ',
                    list(self.cheese_pizzas.keys()) + list(self.meat_pizzas.keys()),
                    key=f'Type {i}'
                )
            
            with col2:
                pizza_size = st.selectbox(
                    'Size: ',
                    list(self.sizes.keys()),
                    key=f'Size: {i}'
                )
            
            pizza_price = self._calculate_price(
                pizza_type,
                pizza_size 
            )
            
            total_price += pizza_price 
            
            st.write(f'Subtotal: {pizza_price}')
        
        st.divider()
        
        calculate_order = st.button(
            'Calculate order',
            type='primary',
            width='stretch'
        )

        return (
            calculate_order,
            total_price
        )

class TotalCalculation:
    @staticmethod 
    def _calculate_total(
        order_total: int,
        theshold: int,
        discount: int
    ):
        if order_total <= theshold:
            return (order_total, False) 
        else:
            return (order_total * (1.0 - discount), True)
    
    @staticmethod
    def display_total(
        order_total: int,
        threshold: int,
        discount: int
    ):
        actual_total, has_discount = TotalCalculation._calculate_total(
            order_total,
            threshold,
            discount
        )
        
        if has_discount:
            st.success(
                f"Order Total: {order_total} EGP | "
                f"{discount * 100}% discount: {order_total * discount} EGP | "
                f"Final Price: {actual_total} EGP"
            )

        else:
            st.success(f"Order Total: {order_total}| Final Price: {actual_total}")
    
sidebar = Sidebar()

beef_pizzas =  {
    'Pepperoni': 150,
    'BBQ Chicken': 160,
    'Supreme': 180
}

cheese_pizzas = {
    'Margherita': 100,
    'Veggie': 120,
    'Mashroom': 130
}

sizes = {
    'Small': 0,
    'Medium' : 30,
    'Large' : 55
}

menu_display = MenuDisplay(
    beef_pizzas,
    cheese_pizzas
)

enterance = EnteranceSystem(
    beef_pizzas,
    cheese_pizzas,
    sizes
)

total_calculation = TotalCalculation(
    
)

sidebar.display_sidebar()
menu_display.display_menu()
button_clicked, total_value = enterance.enter_pizzas()

if button_clicked:
    total_calculation.display_total(
        total_value,
        400,
        0.15    
    )
