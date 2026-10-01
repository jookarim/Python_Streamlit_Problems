import streamlit as st 

#Custom exception for handling invalid products
class InvalidProductException(Exception):
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

#Simple console test no UI yet (saperating logic from ui for cleaner code)
product_manager = ProductManager()
product_manager.add_product('1001', 'Hello', 'Clothes', 10, 60)

print(product_manager.get_products_list_dict())
