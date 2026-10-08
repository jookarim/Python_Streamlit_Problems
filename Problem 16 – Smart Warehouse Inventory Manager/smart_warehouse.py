import streamlit as st 
import time 

#Name of the warehouse

WAREHOUSE_NAME = "Best warehouse"

#Time to display success messages before rerun
SUCCESS_TIMER = 0.5

#Custom exception for handling invalid products
class InvalidProductException(Exception):
    pass 

#Custom exception for handling no result from search
class NoSearchResultException(Exception):
    pass 

#Custom exception for handling Invalid search data
class InvalidSearchException(Exception):
    pass 

#Custom exception for handling invalid deleting id
class InvalidIDException(Exception):
    pass 

#Custom exception for quantity not 0 for deleting product
class QuantityNotZeroException(Exception):
    pass 

#Custom exception for product already found
class ProductAlreadyFoundException(Exception):
    pass 

#Custom exception for quantity higher than remove stock one
class HighQuantityException(Exception):
    pass 

#Custom exception for product not found
class ProductNotFoundException(Exception):
    pass 

#Custom exception for invalid price 
class InvalidPriceException(Exception):
    pass 

#Custom exception for invalid quantity
class InvalidQuantityException(Exception):
    pass 

categories = [
    'Electronics',
    'Clothes'
]

#Product class that stores product data
class Product:
    def __init__(self, id: str, name: str, category: str, quantity: int, unit_price: int):
        self.id = id 
        self.name = name
        self.category = category
        self.quantity = quantity 
        self.unit_price = unit_price 

#Repository for products to make data storage and retrival saperated from buiseness logic

class ProductRepository:
    def __init__(self):
        self.products = []
    
    def add_product(self, product: Product) -> None:
        """Add product to products list"""
        self.products.append(product)
    
    def remove_product(self, product: Product) -> None:
        """Remove product from products list"""
        self.products.remove(product)
    
    def get_products_ids(self) -> list[str]:
        """Get all products ids"""
        products_ids = []
        
        for product in self.products:
            products_ids.append(product.id)
        
        return products_ids 
    
    def search_product(self, product_id: str, product_name: str, product_category: str) -> Product | None:
        """Search for product (for now, write the 3 fields)"""
        for product in self.products:
            if (product_id == product.id
                and product_name == product.name 
                and product_category == product.category):
                    return product 
                        
        return None 
    
    def product_found(self, checked_product: Product) -> bool:
        """Check if a product found"""
        for product in self.products:
            if product.id == checked_product.id:
                return True 
        
        return False   
    
    def get_all_products(self) -> list[Product]:
        """Get all products objects"""
        return self.products
    
    def get_product_by_id(self, id: str) -> Product | None:
        """Get product object by a specific id"""
        for product in self.products:
            if product.id == id:
                return product

        return None

class Activity:
    def __init__(self, product_id: str, product_quantity: int):
        self.product_id = product_id 
        self.product_quantity = product_quantity

class ActivityRepository:
    def __init__(self):
        self.activities = {}
        self.activities_list = []
        
    def add_activity(self, product_id: str, operation: int) -> None:
        """Add activity to activity repository"""
        if product_id not in self.activities:
            self.activities[product_id] = []
            
        self.activities[product_id].append(operation)
        self.activities_list.append(Activity(product_id, operation))
        
    def remove_activity(self, product_id: str, operation: int) -> None:
        """Remove activity from activity repository"""
        self.activities[product_id].remove(operation)
        self.activities_list.remove(Activity(product_id, operation))
        
    def get_all_activities(self) -> list[Activity]:
        """Get all activities to be used when displaying activities"""
        return self.activities_list
    
#Class that validates insertion
class Validator:
    @staticmethod
    def valid_product(new_product: Product) -> bool:
        """Checks if the ID, name, or category are empty,
        or if the quantity is less than 0,
        or if the price is less than or equal to 0."""
        
        if (not new_product.id or 
            not new_product.name or 
            not new_product.category or 
            new_product.quantity < 0 or 
            new_product.unit_price <= 0):
            
            return False 
            
        return True

    @staticmethod 
    def valid_search(product_id: str, 
                    product_name: str, 
                    product_category: str, 
                    ) -> bool:
        
        """Checks if search data are valid not empty data"""
        if not product_id or not product_category or not product_name:
            return False 
        
        return True

    @staticmethod
    def valid_id(product_id: str) -> bool:
        """Check if id is valid"""
        return product_id != ''
    
    @staticmethod
    def valid_quantity(quantity: int) -> bool:
        """Check if quantity valid"""
        return quantity > 0 
    
    @staticmethod 
    def valid_price(price: int) -> bool:
        """Check if price is valid"""
        return price > 0 
    

def rerun_success() -> None:
    """Function to rerun code if success happend to 
    update products data display in ui"""
    
    time.sleep(SUCCESS_TIMER)
    st.rerun()
    

class ProductManager: 
    """Class to manager products operations"""
    
    def __init__(self, product_repository: ProductRepository):
        """Initialize products repository"""
         
        self.product_repository = product_repository
        
    def add_product(self, id: str, name: str, category: str, unit_price: int) -> None:
        """Add product but raise exception if invalid product or already found"""
        
        product_repository = self.product_repository
        
        product = Product(id, name, category, 0, unit_price)
        
        if not Validator.valid_product(product):
            raise InvalidProductException("Product is invalid, cannot add it")
                
        if product_repository.product_found(product):
            raise ProductAlreadyFoundException("Product already found")
            
        product_repository.add_product(product)
        
    def get_products_list_dict(self) -> list[dict]:
        """Get products as shape of list dict to be displayed as table in ui"""
        products_list_dict = []
        
        for product in self.product_repository.get_all_products():
            products_list_dict.append({
                'ID' : product.id,
                'Name' : product.name,
                'Category' : product.category,
                'Quantity' : product.quantity,
                'Unit price' : product.unit_price
            })    

        return products_list_dict 
        
    def get_products_ids(self) -> list[str]:
        return self.product_repository.get_products_ids()
    
    def search_product(self, id: str, name: str, category: str) -> Product | None:
        """Search for specific product using id, name, category"""
        
        product_repository = self.product_repository
        #If search data are invalid raise exception for invalid search data
        if not Validator.valid_search(id, name, category):
            raise InvalidSearchException("Search data are invalid")
        
        #Search for product data and return it if found
        product = self.product_repository.search_product(
            id,
            name,
            category
        )

        if product is None:
            raise NoSearchResultException("No results with these search data")

        return product
        
    def delete_product(self, id: str) -> None:
        """Function to delete product and raise exceptions if 
        ID is invalid or product not found or quantity is 0"""
        
        if not Validator.valid_id(id):
            raise InvalidIDException("ID is invalid for deletion")

        product = self.product_repository.get_product_by_id(id)

        if product is None:
            raise ProductNotFoundException("ID not found to delete product with")

        if product.quantity != 0:
            raise QuantityNotZeroException("Cannot delete product with quantity not equal 0")

        self.product_repository.remove_product(product)
    
    def update_price(self, id: str, new_unit_price: int) -> None:
        """Function to update price of a specific product and 
        raise exceptions if 
        ID is invalid or new price is invalid or Product not found"""
        
        if not Validator.valid_id(id):
            raise InvalidIDException("Invalid ID cannot update price")
        
        if not Validator.valid_price(new_unit_price):
            raise InvalidPriceException("Invalid price to update with")
        
        product = self.product_repository.get_product_by_id(id)
        
        if product is None:
            raise ProductNotFoundException("Product not found to update its price")
        
        product.unit_price = new_unit_price
    
class StockManager:
    """Class to manager stock operations"""
    def __init__(self, 
                product_repository: ProductRepository,
                activity_repository: ActivityRepository):
        
        """Store product repository reference 
        (Do not know how data are stored just use the repo function)
        easy to change how data are stored later"""
        
        self.product_repository = product_repository
        self.activity_repository = activity_repository
        
    def restock_product(self, id: str, quantity: int) -> None:
        """Class to restock (add quantity to already added products) 
        Raise exception when ID is invalid or quantity is invalid
        or product not found"""
        
        
        if not Validator.valid_id(id):
            raise InvalidIDException("ID is invalid for restock")
                
        elif not Validator.valid_quantity(quantity):
            raise InvalidQuantityException("Quantity is invalid for restock")
        
        product = self.product_repository.get_product_by_id(id)

        if product is None:
            raise ProductNotFoundException("Product not found to restock")

        product.quantity += quantity
        
        self.activity_repository.add_activity(product.id, quantity)
        
    def get_products_ids(self) -> list[str]:
        return self.product_repository.get_products_ids()
        
    def remove_stock(self, id: str, quantity: int) -> None:
        """Class to remove stock 
        (Take quantity from already added product)
        Raise exceptions if ID is invalid
        or Quantity is invalid
        or Quantity to remove is greater than product quantity 
        or product not found"""
        
        if not Validator.valid_id(id):
            raise InvalidIDException("ID is invalid for restock")
                
        elif not Validator.valid_quantity(quantity):
            raise InvalidQuantityException("Quantity is invalid for remove stock")
        
        #Get product quantity
        curr_quantity = self.get_quantity(id)
        
        #Raise exception of quantity needed to restock > curr quantity
        if curr_quantity < quantity:
            raise HighQuantityException("Removed quantity is higher than current product quantity")
        
        #restock of all data are correct
        product = self.product_repository.get_product_by_id(id)
        
        if product is None:
            raise ProductNotFoundException("Product not found to remove stock")

        product.quantity -= quantity
    
        self.activity_repository.add_activity(product.id, -quantity)
        
    def low_stock_report(self, threshold: int) -> list[dict]:
        """Get low stock products (Quantity < threshold)
        Raise exceptions when quantity is invalid"""
        
        if not Validator.valid_quantity(threshold):
            raise InvalidQuantityException("Quantity is invalid")
        
        low_stock = []
        
        for product in self.product_repository.get_all_products():
            if product.quantity < threshold:
                low_stock.append({
                    'Name: ' : product.name,
                    'Quantity: ' : product.quantity
                })
        
        return low_stock 
    
    def get_quantity(self, id: str) -> int:
        """Get quantity of a specific product using id
        Raise exception when product is not found"""
        
        product = self.product_repository.get_product_by_id(id)

        if product is None:
            raise ProductNotFoundException("Product not found to get its quantity")

        return product.quantity

class ActivityReportHelper:
    @staticmethod
    def get_activity_type(quantity: int) -> None:
        """Helper function that uses quantity to 
        determine is it a restock or remove"""
        
        return 'Restock' if quantity > 0 else 'Remove'
    
    @staticmethod
    def get_sign_type(quantity: int) -> str:
        activity_type = ActivityReportHelper.get_activity_type(quantity)
        return '+' if activity_type == 'Restock' else ''

#Make activity report manager to get data as dict (type, quantity)

class ActivityReportManager:
    def __init__(self, activity_repository: ActivityRepository):
        self.activity_repository = activity_repository
    
    def get_data_dict_shape(self):
        dict_shape = []
        
        for activity in self.activity_repository.get_all_activities():
            dict_shape.append({
                'Product id: ' : activity.product_id,
                'Activity type: ' : ActivityReportHelper.get_activity_type(
                    activity.product_quantity
                ),
                'Quantity: ' : activity.product_quantity
            })
            
            return dict_shape 
        
#UI display for activities
class ActivityReportUI:
    def __init__(self, activity_report_manager: ActivityReportManager):
        self.activity_report_manager = activity_report_manager

    def display(self) -> None:
        """Get all activities then 
        display ID of product and activity type"""
        
        activities = self.activity_report_manager.get_data_dict_shape()

        if not activities:
            st.info('There are no activities done yet')
        else:        
            st.table(activities)
                
class InventoryStatistics:
    """class to get some statistics about products"""

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository 
        
    def get_count_products(self) -> int:
        """Function to get count products"""
        return len(self.product_repository.get_all_products())

    def get_total_quantity(self) -> int:
        """Get total quantity of products"""

        total_quantity = 0 

        for product in self.product_repository.get_all_products():
            total_quantity += product.quantity 

        return total_quantity 

    def get_total_value_by_category(self) -> dict[str, int]:
        category_value = {}
        
        for product in self.product_repository.get_all_products():
            if product.category not in category_value:
                category_value[product.category] = 0 
            
            category_value[product.category] += (product.unit_price * product.quantity)
        
        return category_value
            
    def get_total_value(self) -> int:
        """Get total products values"""

        total_value = 0 

        for product in self.product_repository.get_all_products():
            total_value += (product.unit_price * product.quantity)

        return total_value 

    def get_highest_stock_product(self) -> Product | None:
        products = self.product_repository.get_all_products()

        if len(products) == 0:
            return None

        highest_stock_product = products[0]

        for product in products:
            if product.quantity > highest_stock_product.quantity:
                highest_stock_product = product

        return highest_stock_product
    
    def get_lowest_stock_product(self) -> Product | None:
        products = self.product_repository.get_all_products()

        if len(products) == 0:
            return None

        lowest_stock_product = products[0]

        for product in products:
            if product.quantity < lowest_stock_product.quantity:
                lowest_stock_product = product

        return lowest_stock_product
    
    def get_count_products_per_category(self) -> dict[str, int]:
        name_count = {}
        
        for product in self.product_repository.get_all_products():
            if product.name not in name_count:
                name_count[product.category] = 0
                
            name_count[product.category] += 1    
        
        return name_count

class ProductManagerUI:
    """Display UI of product management"""

    def __init__(self, product_manager: ProductManager) -> None:
        """Add product manager reference"""

        self.product_manager = product_manager 
        
    def add_product_ui(self) -> None:
        """Function to display UI of adding product"""

        product_manager = self.product_manager 

        #Form to get products data
        with st.form(key='Add product form'):
            product_id = st.text_input('Product ID: ').strip()
            product_name = st.text_input('Product name: ')
            category = st.selectbox('Category: ', categories)
            unit_price = st.number_input('Unit price: ')
            add_product = st.form_submit_button('Add Product', type='primary')

            #Display status if add_product button pressed
            if add_product:
                try:
                    self.product_manager.add_product(
                        id=product_id.strip(),
                        name=product_name.strip(),
                        category=category,
                        unit_price=unit_price
                    )

                except InvalidProductException as e:
                    st.error(str(e))
                except ProductAlreadyFoundException as e:
                    st.warning(str(e))
                else:
                    st.success('Product is added successfully')        
                    rerun_success()

    #View products as table
    def view_products_ui(self) -> None:
        if len(self.product_manager.get_products_list_dict()) == 0:
            st.warning('No products found in the warehouse')
        else:
            product_manager = self.product_manager 

            products_dict = product_manager.get_products_list_dict()
            st.table(products_dict)

    
    def _confirm_delete(self, product_id):
        @st.dialog(f"Are you sure you want to delete product {product_id}?")
        def confirm_delete_logic():
            if st.button("Confirm delete"):
                try:
                    self.product_manager.delete_product(product_id)

                except ProductNotFoundException as e:
                    st.error(str(e))

                except QuantityNotZeroException as e:
                    st.warning(str(e))

                except InvalidIDException as e:
                    st.error(str(e))

                else:
                    st.success("Product is deleted successfully")
                    rerun_success()
                    st.rerun()

        confirm_delete_logic()
    
    def _confirm_update_price(self, product_id, unit_price):
        @st.dialog(f'Are you sure you want to update the unit price of {product_id}')
        
        def confirm_update_logic():
            confirm_update_button = st.button('Confirm update')
            
            if confirm_update_button:
                try:
                    self.product_manager.update_price(product_id, unit_price)
                except ProductNotFoundException as e:
                    st.error(str(e))
                except InvalidIDException as e:
                    st.error(str(e))
                except InvalidPriceException as e:
                    st.error(str(e))
                else:
                    st.success('Product price is updated successfully')
                    rerun_success()
                    
        confirm_update_logic()
            
    def delete_product_ui(self) -> None:
        """Function to delete product"""

        product_manager = self.product_manager

        with st.form("Delete product form"):
            product_id = st.selectbox("Product ID: ", product_manager.get_products_ids())

            delete_product_button = st.form_submit_button("Delete product")

            if delete_product_button:
                self._confirm_delete(product_id)


    def update_price_ui(self) -> None:
        """Update price of a product"""

        #Take product data in the form
        with st.form(key='Update price'):
            product_id = st.selectbox('Product ID: ', self.product_manager.get_products_ids())
            unit_price = st.number_input('Product price: ')

            update_price_submit = st.form_submit_button('Update price')

        #Display status if update_price button pressed

        if update_price_submit:
            self._confirm_update_price(product_id, unit_price)

class StockManagerUI:
    """Display UI of stock management"""

    def __init__(self, stock_manager: StockManager) -> None:
        """Put stock manager as a reference"""

        self.stock_manager = stock_manager 

    def restock_product_ui(self) -> None:
        """Display the UI for restocking an existing product."""

        #Create a form to get the product ID and quantity to restock
        with st.form('Restock product'):
            product_id = st.selectbox('Product ID: ', self.stock_manager.get_products_ids())

            product_quantity = st.number_input('Quantity: ')

            restock_product_button = st.form_submit_button('Restock product')

        #Display status when the restock button is pressed
        if restock_product_button:  
            try:
                self.stock_manager.restock_product(product_id, product_quantity)
            except ProductNotFoundException as e:
                st.error(str(e))
            except InvalidQuantityException as e:
                st.error(str(e))
            except InvalidIDException as e:
                st.error(str(e))
            else:
                st.success(f'Product: {product_id} restocked successfully')
                rerun_success()

    def low_stock_ui(self) -> None:
        """Display the UI for checking products with low stock."""

        #Create a form to get the stock threshold
        with st.form("Low stock form"):        
            threshold = st.number_input(":red[Threshold]")
            submit_threshold = st.form_submit_button("Submit threshold")

        #Display the low stock report when the threshold is submitted
        if submit_threshold:
            try:    
                low_stock_products = self.stock_manager.low_stock_report(threshold)
            except InvalidQuantityException as e:
                st.error(str(e))
            else:                    
                #Display a message when no products are below the threshold
                if len(low_stock_products) == 0:
                    st.info('All products currently have sufficient stock')
                else:
                    #Display the products that have low stock
                    st.table(low_stock_products)
                    st.warning('Low stock products exist')

    def remove_stock_ui(self) -> None:
        """Display the UI for removing quantity from product stock."""

        #Create a form to get the product ID and quantity to remove
        with st.form('Remove stock'):
            product_id = st.selectbox("Product ID: ", self.stock_manager.get_products_ids())

            product_quantity = st.number_input("Product Quantity: ")

            remove_stock = st.form_submit_button("Remove stock")

            #Display status when the remove stock button is pressed
            if remove_stock:
                try:
                    self.stock_manager.remove_stock(product_id, product_quantity)
                except ProductNotFoundException as e:
                    st.error(str(e))
                except InvalidQuantityException as e:
                    st.error(str(e))
                except InvalidIDException as e:
                    st.error(str(e))
                except HighQuantityException as e:
                    st.warning(str(e))
                else:
                    st.success(f'Product {product_id} removed successfully')
                    rerun_success()


class InventoryUI:
    """Display the main inventory UI and connect the management UIs."""

    def __init__(self, 
                product_manager_ui: ProductManagerUI, 
                stock_manager_ui: StockManagerUI,
                inventory_statistics: InventoryStatistics, 
                activity_report_ui: ActivityReportUI) -> None:
        
        #Store the product and stock management UI references
        self.product_manager_ui = product_manager_ui 
        self.stock_manager_ui = stock_manager_ui 
        self.inventory_statistics = inventory_statistics 
        self.activity_report_ui = activity_report_ui
        
        st.title(f'Warehouse name: {WAREHOUSE_NAME}', text_alignment='center')
        st.divider()
        
        st.set_page_config(layout="wide", page_title=f'Warehouse name: {WAREHOUSE_NAME}')
    
    def display_statistics(self):
        """Display inventory statistics
        (count, total quantity, total value, highest stock pay
        highest stock pay product, lowest stock pay,
        lowest stock pay product)"""
        
        #Initialize statistics variables
        inventory_statistics = self.inventory_statistics
        count_products = inventory_statistics.get_count_products()
        total_quantity = inventory_statistics.get_total_quantity()
        total_inventory_value = inventory_statistics.get_total_value()
        hieghst_stock_pay = inventory_statistics.get_highest_stock_product()
        lowest_stock_pay = inventory_statistics.get_lowest_stock_product()
        count_products_per_category = inventory_statistics.get_count_products_per_category()
        total_price_per_category = inventory_statistics.get_total_value_by_category()
        
        #Display statistics
        st.write(f"Total products: {count_products}")
        st.write(f"Total quantity: {total_quantity}")
        st.write(f"Total inventory value: {total_inventory_value}")
        
        if hieghst_stock_pay is not None:
            st.write(f"Highest stock product: {hieghst_stock_pay.name}")
            st.write(f"Highest stock quantity: {hieghst_stock_pay.quantity}")
            st.write(f"Lowest stock product: {lowest_stock_pay.name}")
            st.write(f"Lowest stock quantity: {lowest_stock_pay.quantity}")
        
        st.divider()
        
        st.subheader('Category : count products')
        
        st.table(count_products_per_category)
        
        st.subheader('Category : total_price')
        
        st.table(total_price_per_category)
        
    def display(self) -> None:
        """Display all inventory operations using separate tabs."""

        #Create tabs for the different inventory operations
        
        tabs_names = [
            'Add product',
            'Remove product',
            'View products',
            'Update product price',
            'Restock product',
            'Remove stock',
            'Low stock',
            'Inventory statistics',
            'Activity report'
        ]
        
        tabs = st.tabs(tabs_names)

        #Display the add product UI
        with tabs[0]:
            st.header(f'{tabs_names[0]}', text_alignment='center')
            self.product_manager_ui.add_product_ui()

        #Display the remove product UI
        with tabs[1]:
            st.header(f'{tabs_names[1]}', text_alignment='center')
            self.product_manager_ui.delete_product_ui()

        #Display the view products UI
        with tabs[2]:
            st.header(f'{tabs_names[2]}', text_alignment='center')
            self.product_manager_ui.view_products_ui()

        #Display the update price UI
        with tabs[3]:
            st.header(f'{tabs_names[3]}', text_alignment='center')
            self.product_manager_ui.update_price_ui()

        #Display the restock product UI
        with tabs[4]:
            st.header(f'{tabs_names[4]}', text_alignment='center')
            self.stock_manager_ui.restock_product_ui()

        #Display the remove stock UI
        with tabs[5]:
            st.header(f'{tabs_names[5]}', text_alignment='center')
            self.stock_manager_ui.remove_stock_ui()

        #Display the low stock UI
        with tabs[6]:
            st.header(f'{tabs_names[6]}', text_alignment='center')
            self.stock_manager_ui.low_stock_ui()

        #Display statistics UI
        with tabs[7]:
            st.header(f'{tabs_names[7]}', text_alignment='center')
            self.display_statistics()
            
        with tabs[8]:
            st.header(f'{tabs_names[8]}', text_alignment='center')
            self.activity_report_ui.display()
            
    def display_sidebar(self) -> None:
        """Display inventory statistics in the Streamlit sidebar."""

        #Get the current number of products
        count_products = self.inventory_statistics.get_count_products()

        #Get the total quantity of all products
        total_quantity = self.inventory_statistics.get_total_quantity()

        #Get the total value of all products
        total_value = self.inventory_statistics.get_total_value()

        #Display the statistics inside the Streamlit sidebar
        with st.sidebar:
            st.write(f'Ware house name: {WAREHOUSE_NAME}')
            st.write(f'Total number of products: {count_products}')
            st.write(f'Total quantity in stock: {total_quantity}')
            st.write(f'Total product_repository value: {total_value}')

#Create the product repository once and keep it in Streamlit session state
if "product_repository" not in st.session_state:
    st.session_state["product_repository"] = ProductRepository()

#Get the shared product repository from session state
product_repository = st.session_state["product_repository"]

#Create the product manager using the shared repository
product_manager = ProductManager(product_repository)

#Create activity repository instance

if 'activity_repository' not in st.session_state:
    st.session_state['activity_repository'] = ActivityRepository()

activity_repository = st.session_state['activity_repository']

#Create the stock manager using the shared repository
stock_manager = StockManager(product_repository, activity_repository)

#Create the product management UI
product_manager_ui = ProductManagerUI(product_manager)

#Create the stock management UI
stock_manager_ui = StockManagerUI(stock_manager)

#Create inventory statistics instance
inventory_statistics = InventoryStatistics(product_repository)

activity_manager = ActivityReportManager(activity_repository)

activity_report_ui = ActivityReportUI(activity_manager)

#Create the main inventory UI using both management UIs
inventory_ui = InventoryUI(product_manager_ui, 
                           stock_manager_ui, 
                           inventory_statistics,
                           activity_report_ui
                           )

#Display the main inventory interface
inventory_ui.display()

#Display the inventory statistics in the sidebar
inventory_ui.display_sidebar()