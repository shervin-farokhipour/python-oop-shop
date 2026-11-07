from models.products.product import Product
from validation.validation import id_validator, quantity_validator, price_validator, object_validator


class OrderItem:
    """کلاس آیتم‌های درون یک سفارش"""

    def __init__(self, item_id, product_obj, quantity, unit_price):
        self.id = item_id
        self.product = product_obj
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = id_validator(value, field_name="شناسه آیتم سفارش")

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._product = object_validator(value, Product, field_name="کالا")

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = quantity_validator(value)

    @property
    def unit_price(self):
        return self._unit_price

    @unit_price.setter
    def unit_price(self, value):
        self._unit_price = price_validator(value, field_name="قیمت واحد")
