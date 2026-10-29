from enum import Flag, auto
from dataclasses import dataclass, field  
from typing import Protocol 

class ProductType(Flag):
    DIGITAL = auto(),
    PHYSICAL = auto() 
    ALL = DIGITAL | PHYSICAL 
    
class ProductUtils:
    def __init__(cls):
        cls._product_id = 0 
    
    @classmethod 
    def generate_product_id(cls) -> int:
        cls._product_id += 1 
        return cls._product_id 
    
@dataclass
class Product:
    product_type: ProductType 
    product_price: int
    
    product_id: str = field(
        init=False, 
        default_factory=ProductUtils.generate_product_id
    )
   
    product_quantity: int = 0
    shipping_fee: int | None
    
    def get_total_price(self) -> int:
        price = self.product_price * self.product_quantity
        
        if self.product_type == ProductType.PHYSICAL:
            price += self.shipping_fee 
        
        return price 


class ProductRepository(Protocol):
    def add_product(self, product: Product) -> None:
        ...

    def get_by_id(self, product_id: str) -> Product | None:
        ...

    def get_all_products(self) -> list[Product]:
        ...

    def delete_product(self, product_id: str) -> None:
        ...

    def search_product(self, query: str) -> list[Product]:
        ...
    
    
class InMemoryProductRepository:
    def __init__(self):
        self.products = {}
    
    def add_product(self, new_product: Product) -> None:
        self.products[new_product.product_id] = new_product
    
    def get_by_id(self, product_id: str) -> Product | None:
        return self.products.get(product_id, None)
    
    def get_all_products(self) -> list[Product]:
        products_output = []
        
        for product_id, product in self.products.items():
            products_output.append(product) 
        
        return products_output 
    
    def delete_product(self, product_id: str) -> None:
        del self.products[product_id]
    
    def search_product(self, query: Product) -> list[Product]:
        if query.product_id:
            product = self.get_by_id(query.product_id)
            return [product] if product is not None else []
    
        search_result = []
    
        for product in self.products.values():
            valid_result = True
    
            if query.product_type is not None:
                if product.product_type != query.product_type:
                    valid_result = False
    
            if query.product_price is not None:
                if product.product_price != query.product_price:
                    valid_result = False
    
            if query.product_quantity is not None:
                if product.product_quantity != query.product_quantity:
                    valid_result = False
    
            if query.shipping_fee is not None:
                if product.shipping_fee != query.shipping_fee:
                    valid_result = False
    
            if valid_result:
                search_result.append(product)
    
        return search_result
    
class ProductAlreadyFoundException(Exception):
    ... 
    
class InvalidProductException(Exception):
    ... 

class NoProductResultException(Exception):
    ...  

class ProductValidator:
    @staticmethod 
    def validate_product_already_found(
        product_already_found: bool  
    ) -> None:
        if product_already_found:
            raise ProductAlreadyFoundException(
                "Cannot add product that is already found"
            )
    
    def validate_product(
        product: Product 
    ) -> None:
        if product.product_price <= 0:
            raise InvalidProductException(
                "Product price is invalid"
            )
        
        elif product.product_type not in ProductType.ALL:
            raise InvalidProductException(
                "Product type is invalid"
            )
        
        elif product.product_quantity <= 0:
            raise InvalidProductException(
                "Product Quanity is invalid"
            )

class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository     
    ):
        self._product_repository = product_repository 
    
    def add_product(
        self,
        product: Product 
    ) -> None:
        product_found = self._product_repository.get_by_id(product.product_id)
        
        if product_found:
            ProductValidator.validate_product_already_found(
                product_found
            )
            
        else:
            ProductValidator.validate_product(
                product 
            )
        
    # def get_by_id(
    #     self,
    #     product_id: str
    # ) -> Product | None:
    #     product_found = self._product_repository.get_by_id(product_id)
        
    #     if not product_found:
    #         raise NoProductResultException(
    #             "No result by id exception"
    #         )
        
        