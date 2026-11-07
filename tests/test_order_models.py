import unittest
from models.users.buyer import Buyer
from models.products.product import Product
from models.orders.order import Order
from models.orders.order_item import OrderItem


class OrderModelTests(unittest.TestCase):
    def setUp(self):
        self.product = Product(1, "دفتر", 100, 10)
        self.buyer = Buyer(1, "ali@example.com", "Sample123", "علی")

    def test_order_item_requires_product(self):
        for invalid in [None, "دفتر", 1, self.buyer]:
            with self.assertRaises(ValueError):
                OrderItem(1, invalid, 2, 100)

    def test_rejected_product_keeps_previous_value(self):
        item = OrderItem(1, self.product, 2, 100)
        with self.assertRaises(ValueError):
            item.product = None
        self.assertIs(item.product, self.product)

    def test_total_follows_quantity_and_unit_price(self):
        order = Order(1, self.buyer)
        item = OrderItem(1, self.product, 2, 100)
        order.add_item(item)
        self.assertEqual(order.total_price, 200)
        item.quantity = 3
        self.assertEqual(order.total_price, 300)
        item.unit_price = 150
        self.assertEqual(order.total_price, 450)
        order.add_item(OrderItem(2, self.product, 1, 100))
        self.assertEqual(order.total_price, 550)

    def test_total_is_derived_from_items(self):
        order = Order(1, self.buyer)
        self.assertEqual(order.total_price, 0)
        with self.assertRaises(AttributeError):
            order.total_price = 500


if __name__ == "__main__":
    unittest.main()
