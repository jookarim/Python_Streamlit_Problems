import streamlit as st 

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
class InvalidDeleteID(Exception):
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
        """Checks if id conflicts 
        then check is id or name or category are empty 
        or quantity less than or equal to 0 
        or price less than or equal to 0"""
        
        for p in existing_products:
            if p.id == new_product.id:
                return False 
        
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
        
        for i in range(len(self.inventory.products)):
            if self.inventory.products[i].id == id:
                raise ProductAlreadyFoundException("Product already found")
            
        if not Validator.valid_insertion(product, inventory.products):
            raise InvalidProductException("Product is invalid, cannot add it")
       
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
            raise InvalidDeleteID("ID is invalid for deletion")
        
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
        
    def get_quantity(self, id):
        """Get quantity of a specific product using id"""
        inventory = self.inventory
        
        for product in inventory.products:
            if product.id == id:
                return product.quantity 
        
        raise ProductNotFoundException("Product not found to get its quantity")
    
inventory = Inventory()

# Store the ProductManager object in Streamlit session state
if "product_manager" not in st.session_state:
    st.session_state["product_manager"] = ProductManager(inventory)

if "stock_manager" not in st.session_state: 
    st.session_state["stock_manager"] = StockManager(inventory)
    
product_manager = st.session_state["product_manager"]
stock_manager = st.session_state["stock_manager"]

#Simple console test no UI yet (saperating logic from ui for cleaner code)

#Try adding product
try:
    product_manager.add_product('1001', 'Hello', 'Clothes', 60)
except InvalidProductException as e:
    print(str(e))
except ProductAlreadyFoundException as e:
    print(str(e))

#display products
print(product_manager.get_products_list_dict())

#Try searching for a product
try:
    product = product_manager.search_product('1001', 'Hello', 'Clothes')
    print(product.unit_price)
except InvalidSearchException as e:
    print(str(e))
except NoSearchResultException as e:
    print(str(e))
    
try:
    stock_manager.restock_product("1001", 20)
    stock_manager.remove_stock("1001", 5)
    print(stock_manager.get_quantity("1001"))
except QuantityInsuffitientException as e:
    print(str(e))
except ProductNotFoundException as e:
    print(str(e))
    
#Try deleting product
try:
    product_manager.delete_product('1001')
except InvalidDeleteID as e:
    print(str(e))
except IDNotFoundForDeleteException as e:
    print(str(e))
except QuantityNotZeroException as e:
    print(str(e))