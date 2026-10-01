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

class InvalidDeleteID(Exception):
    pass 

class IDNotFoundForDeleteException(Exception):
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
class ProductValidator:
    @staticmethod
    def valid_insertion(new_product: Product, existing_products: list[Product]):
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
            new_product.quantity <= 0 or 
            new_product.unit_price <= 0):
            
            return False 
            
        return True

    @staticmethod 
    def valid_search(product_id, 
                    product_name, 
                    product_category, 
                    existing_products: list[Product]):
        
        """Checks if search data are valid not empty data"""
        if not product_id or not product_category or not product_name:
            return False 
        
        return True

    @staticmethod 
    def valid_id(product_id):
        return product_id != ''
     
#Class to manage products 
class ProductManager: 
    def __init__(self):
        """Initialize products list"""
        
        if 'products' not in st.session_state:
            st.session_state['products'] = []

    def add_product(self, id, name, category, quantity, unit_price):
        """Add product but raise exception if invalid product"""
        
        product = Product(id, name, category, quantity, unit_price)
        
        if not ProductValidator.valid_insertion(product, st.session_state['products']):
            raise InvalidProductException("Product is invalid, cannot add it")
        else:
            st.session_state['products'].append(product)
            
    def get_products_list_dict(self):  
        """return data as list of dict to be used when displaying table"""
        products_list_dict = []
        
        for product in st.session_state['products']:
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
        
        #If search data are invalid raise exception for invalid search data
        if not ProductValidator.valid_search(id, name, category, st.session_state['products']):
            raise InvalidSearchException("Search data are invalid")
        
        #Search for product data and return it if found
        for product in st.session_state['products']:
            if (id == product.id
                and name == product.name 
                and category == product.category):
                    return product 
        
        #raise exception for not found product
        raise NoSearchResultException("No results with these search data")
        
    def delete_product(self, id):
        """Delete product using id"""
        
        #If product id is invalid then raise Invalid id exception
        if not ProductValidator.valid_id(id):
            raise InvalidDeleteID("ID is invalid for deletion")
        
        #Remove product with id if found
        for product in st.session_state['products']:
            if product.id == id:
                st.session_state['products'].remove(product)
                return 
        
        #If id not found raise id not found exception
        raise IDNotFoundForDeleteException("ID not found to delete product with")
        
        
#Simple console test no UI yet (saperating logic from ui for cleaner code)
product_manager = ProductManager()

#Try adding product
try:
    product_manager.add_product('1001', 'Hello', 'Clothes', 10, 60)
except InvalidProductException as e:
    print(str(e))

#display products
print(product_manager.get_products_list_dict())

#Try searching for a product
try:
    product = product_manager.search_product('1001', 'v', 'Clothes')
    print(product.unit_price)
except InvalidSearchException as e:
    print(str(e))
except NoSearchResultException as e:
    print(str(e))
    
#Try deleting product
try:
    product_manager.delete_product('1001')
except InvalidDeleteID as e:
    print(str(e))
except IDNotFoundForDeleteException as e:
    print(str(e))