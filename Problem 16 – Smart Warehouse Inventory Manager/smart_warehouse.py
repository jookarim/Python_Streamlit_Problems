import streamlit as st 

WAREHOUSE_NAME = "Best warehouse"

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

#Custom exception for ID not found for deletion
class IDNotFoundForDeleteException(Exception):
    pass 

#Custom exception for quantity not 0 for deleting product
class QuantityNotZeroException(Exception):
    pass 

#Custom exception for product already found
class ProductAlreadyFoundException(Exception):
    pass 

#Custom exception for insuffient quantity
class QuantityInsuffitientException(Exception):
    pass 

#Custom exception for product not found
class ProductNotFoundException(Exception):
    pass 

#Custom exception for invalid price 
class InvalidPriceException(Exception):
    pass 

categories = [
    'Electronics',
    'Clothes'
]

#Product class that stores product data
class Product:
    def __init__(self, id, name, category, quantity, unit_price):
        self.id = id 
        self.name = name
        self.category = category
        self.quantity = quantity 
        self.unit_price = unit_price 
        
#Class that validates insertion
class Validator:
    @staticmethod
    def valid_insertion(new_product: Product, 
                        existing_products: list[Product]):
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
    def valid_search(product_id, 
                    product_name, 
                    product_category, 
                    ):
        
        """Checks if search data are valid not empty data"""
        if not product_id or not product_category or not product_name:
            return False 
        
        return True

    @staticmethod
    def valid_id(product_id):
        """Check if id is valid"""
        return product_id != ''
    
    @staticmethod
    def valid_quantity(quantity):
        """Check if quantity valid"""
        return quantity > 0 
    
    @staticmethod 
    def valid_price(price):
        """Check if price is valid"""
        return price > 0 
    
class Inventory:
    def __init__(self):
        self.products = []

#Class to manage products 
class ProductManager: 
    def __init__(self, inventory):
        """Initialize products list"""
        
        self.inventory = inventory

    def add_product(self, id, name, category, unit_price):
        """Add product but raise exception if invalid product"""
        
        inventory = self.inventory
        
        product = Product(id, name, category, 0, unit_price)
        
        if not Validator.valid_insertion(product, inventory.products):
            raise InvalidProductException("Product is invalid, cannot add it")
                
        for i in range(len(self.inventory.products)):
            if self.inventory.products[i].id == id:
                raise ProductAlreadyFoundException("Product already found")
            
        inventory.products.append(product)
            
    def get_products_list_dict(self):  
        """return data as list of dict to be used when displaying table"""
        products_list_dict = []
        
        inventory = self.inventory 
        
        for product in inventory.products:
            products_list_dict.append({
                'ID' : product.id,
                'Name' : product.name,
                'Category' : product.category,
                'Quantity' : product.quantity,
                'Unit price' : product.unit_price
            })
            
        return products_list_dict

    def search_product(self, id, name, category):
        """Search for specific product using id, name, category"""
        
        inventory = self.inventory
        #If search data are invalid raise exception for invalid search data
        if not Validator.valid_search(id, name, category):
            raise InvalidSearchException("Search data are invalid")
        
        #Search for product data and return it if found
        for product in inventory.products:
            if (id == product.id
                and name == product.name 
                and category == product.category):
                    return product 
        
        #raise exception for not found product
        raise NoSearchResultException("No results with these search data")
        
    def delete_product(self, id):
        """Delete product using id"""
        
        inventory = self.inventory
        #If product id is invalid then raise Invalid id exception
        if not Validator.valid_id(id):
            raise InvalidIDException("ID is invalid for deletion")
        
        #Remove product with id if found
        for product in inventory.products:
            if product.id == id:
                if product.quantity == 0:
                    inventory.products.remove(product)
                    return 
                else:
                    raise QuantityNotZeroException("Cannot delete product with quantity not equal 0")
        
        #If id not found raise id not found exception
        raise IDNotFoundForDeleteException("ID not found to delete product with")

    def update_price(self, id, new_unit_price):
        if not Validator.valid_id(id):
            raise InvalidIDException("Invalid ID cannot update price")
        
        if not Validator.valid_price(new_unit_price):
            raise InvalidPriceException("Invalid price to update with")
        
        inventory = self.inventory 
        
        for product in inventory.products:
            if product.id == id:
                product.unit_price = new_unit_price
                return 
        
        raise ProductNotFoundException("Product not found to update its price")
    
#Class to manage stock operations 
#(restock or delete stock)
#(1 storage location for now)
class StockManager:
    def __init__(self, inventory):
        self.inventory = inventory
    
    def restock_product(self, id, quantity):
        """Class to restock (add quantity to already added products)"""
        if not Validator.valid_quantity(quantity):
            raise QuantityInsuffitientException("Product insuffitient for restock")
        
        if not Validator.valid_id(id):
            raise InvalidIDException("ID is invalid for restock")
        
        inventory = self.inventory 
        
        for product in inventory.products:
            if product.id == id:
                product.quantity += quantity 
                return 
        
        raise ProductNotFoundException("Product not found to restock")
    
    def remove_stock(self, id, quantity):
        """Class to remove stock (Take quantity from already added product)"""
        if not Validator.valid_quantity(quantity):
            raise QuantityInsuffitientException("Product insuffitient for remove stock")
        
        if not Validator.valid_id(id):
            raise InvalidIDException("ID is invalid for restock")
        
        #Get product quantity
        curr_quantity = self.get_quantity(id)
        
        #Raise exception of quantity needed to restock > curr quantity
        if curr_quantity < quantity:
            raise QuantityInsuffitientException("Quantity insuffitient to remove")
        
        #restock of all data are correct
        for product in self.inventory.products:
            if product.id == id:
                product.quantity -= quantity 
                return 
        
        raise ProductNotFoundException("Product not found to remove stock")
    
    def get_quantity(self, id):
        """Get quantity of a specific product using id"""
        inventory = self.inventory
        
        for product in inventory.products:
            if product.id == id:
                return product.quantity 
        
        raise ProductNotFoundException("Product not found to get its quantity")

class InventoryStatistics:
    @staticmethod
    def get_count_products(inventory):
        return len(inventory.products)

    @staticmethod
    def get_total_quantity(inventory):
        total_quantity = 0 
        
        for product in inventory.products:
            total_quantity += product.quantity 
        
        return total_quantity 
    
    @staticmethod 
    def get_total_value(inventory):
        total_value = 0 
        
        for product in inventory.products:
            total_value += (product.unit_price * product.quantity) 
        
        return total_value 
    
def display_sidebar(count_products: int, total_quantity: int, total_value: int) -> None:
    with st.sidebar:
        st.write(f'Ware house name: {WAREHOUSE_NAME}')
        st.write(f'Total number of products: {count_products}')
        st.write(f'Total quantity in stock: {total_quantity}')
        st.write(f'Total inventory value: {total_value}')

class ProductManagerUI:
    def __init__(self, product_manager):
        self.product_manager = product_manager 
    
    def add_product_ui(self):
        product_manager = self.product_manager 
        
        with st.form(key='Add product form'):
            product_id = st.text_input('Product ID: ')
            product_name = st.text_input('Product name: ')
            category = st.selectbox('Category: ', categories)
            unit_price = st.number_input('Unit price: ')
            add_product = st.form_submit_button('Add Product')
            
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
    
    def view_inventory_ui(self):
        if len(self.product_manager.inventory.products) == 0:
            st.warning('No products found in the warehouse')
        else:
            product_manager = self.product_manager 
            products_dict = product_manager.get_products_list_dict()
            st.table(products_dict)

    def delete_product_ui(self):
        product_manager = self.product_manager

        with st.form("Delete product form"):
            product_id = st.text_input("Product ID: ")

            delete_product_button = st.form_submit_button("Delete product")

            if delete_product_button:
                try:
                    product_manager.delete_product(product_id)

                except IDNotFoundForDeleteException as e:
                    st.error(str(e))

                except QuantityNotZeroException as e:
                    st.warning(str(e))

                except InvalidIDException as e:
                    st.error(str(e))

                else:
                    st.success("Product is deleted successfully")
        
    def update_price_ui(self):
        with st.form(key='Update price'):
            product_id = st.text_input('Product ID: ')
            unit_price = st.number_input('Product price: ')
            
            update_price_submit = st.form_submit_button('Update price')
        
        if update_price_submit:
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
                
class StockManagerUI:
    def __init__(self, stock_manager: StockManager):
        self.stock_manager = stock_manager 
    
    def restock_product_ui(self):
        with st.form('Restock product'):
            product_id = st.text_input('ID: ')
            product_quantity = st.number_input('Quantity: ')
            
            restock_product_button = st.form_submit_button('Restock product')
            
        if restock_product_button:   
            try: 
                self.stock_manager.restock_product(product_id, product_quantity)
            except ProductNotFoundException as e:
                st.warning(str(e))
            except QuantityInsuffitientException as e:
                st.error(str(e))
            except InvalidIDException as e:
                st.error(str(e))
            else:
                st.success(f'Product: {product_id} restocked successfully')
                
    def remove_stock_ui(self):
        with st.form('Remove stock'):
            product_id = st.text_input("Product ID: ")
            product_quantity = st.number_input("Product Quantity: ")
            
            remove_stock = st.form_submit_button("Remove stock")
            
            if remove_stock:
                try:
                    self.stock_manager.remove_stock(product_id, product_quantity)
                except ProductNotFoundException as e:
                    st.error(str(e))
                except QuantityInsuffitientException as e:
                    st.error(str(e))
                except InvalidIDException as e:
                    st.error(str(e))
                else:
                    st.success(f'Product {product_id} removed successfully')
        
class InventoryUI:
    def __init__(self, product_manager_ui, stock_manager_ui):
        self.product_manager_ui = product_manager_ui 
        self.stock_manager_ui = stock_manager_ui 
    
    def display(self):
        tabs = st.tabs([
            'Add product',
            'Remove product',
            'View products',
            'Update product price',
            'Restock product',
            'Remove stock'
        ])
        
        with tabs[0]:
            self.product_manager_ui.add_product_ui()
            
        with tabs[1]:
            self.product_manager_ui.delete_product_ui()
            
        with tabs[2]:
            self.product_manager_ui.view_inventory_ui()
        
        with tabs[3]:
            self.product_manager_ui.update_price_ui()
            
        with tabs[4]:
            self.stock_manager_ui.restock_product_ui()
        
        with tabs[5]:
            self.stock_manager_ui.remove_stock_ui()
            
if "inventory" not in st.session_state:
    st.session_state["inventory"] = Inventory()

inventory = st.session_state["inventory"]
product_manager = ProductManager(inventory)
stock_manager = StockManager(inventory)

#Simple console test no UI yet (saperating logic from ui for cleaner code)

product_manager_ui = ProductManagerUI(product_manager)
stock_manager_ui = StockManagerUI(stock_manager)
inventory_ui = InventoryUI(product_manager_ui, stock_manager_ui)

#Try adding product
inventory_ui.display()

count_products = InventoryStatistics.get_count_products(inventory)
total_quantity = InventoryStatistics.get_total_quantity(inventory)
total_inventory = InventoryStatistics.get_total_value(inventory)

display_sidebar(count_products, total_quantity, total_inventory)

