from models.products.category import Category
from models.users.seller import Seller
from validation.validation import id_validator, name_validator, price_validator, stock_validator, object_validator


class Product:
    """کلاس کالا (محصول)"""

    def __init__(self, product_id, name, price, stock, category_obj=None, seller_obj=None):
        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category_obj
        self.seller = seller_obj

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = id_validator(value, field_name="شناسه کالا")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = name_validator(value, field_name="نام کالا")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = price_validator(value, field_name="قیمت کالا")

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = stock_validator(value)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value is not None:
            object_validator(value, Category, field_name="دسته‌بندی")
        self._category = value

    @property
    def seller(self):
        return self._seller

    @seller.setter
    def seller(self, value):
        if value is not None:
            object_validator(value, Seller, field_name="فروشنده")
        self._seller = value
