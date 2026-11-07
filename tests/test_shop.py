import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from models.users.buyer import Buyer
from models.products.product import Product
from models.orders.order import Order
from models.orders.order_item import OrderItem
from models.payments.payment import Payment
from storage import buyer_file
from validation.validation import (price_validator, stock_validator, quantity_validator,
                                   email_validator, password_validator, phone_validator)


class ShopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'buyers.txt'
        self.patch = patch.object(buyer_file, 'DATA_FILE', self.path)
        self.patch.start()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(self.patch.stop)

    def buyer(self, name='علی'):
        return Buyer(1, 'ali@example.com', 'Sample123', name, 'احمدی', '09123456789', 'تهران')

    def test_save_reload_search_update_delete(self):
        buyer_file.insert_buyer(self.buyer())
        self.assertEqual(buyer_file.read_buyers()[0].phone, '09123456789')
        self.assertEqual(buyer_file.search_buyers('ALI')[0].first_name, 'علی')
        self.assertEqual(buyer_file.search_buyers('احمدی')[0].id, 1)
        buyer_file.update_buyer(self.buyer('رضا'))
        self.assertEqual(buyer_file.read_buyers()[0].first_name, 'رضا')
        buyer_file.delete_buyer('1')
        self.assertEqual(buyer_file.read_buyers(), [])

    def test_duplicate_and_missing(self):
        buyer_file.insert_buyer(self.buyer())
        with self.assertRaises(ValueError):
            buyer_file.insert_buyer(self.buyer())
        with self.assertRaises(ValueError):
            buyer_file.delete_buyer(2)
        buyer_file.delete_buyer(1)
        with self.assertRaises(ValueError):
            buyer_file.update_buyer(self.buyer())

    def test_corrupt_file_is_not_overwritten(self):
        for text in ['broken', '1|two', '1|bad|password|name|family|phone|address']:
            self.path.write_text(text, encoding='utf-8')
            with self.assertRaises(ValueError):
                buyer_file.insert_buyer(self.buyer())
            self.assertEqual(self.path.read_text(encoding='utf-8'), text)

    def test_failed_write_preserves_original(self):
        buyer_file.insert_buyer(self.buyer())
        original = self.path.read_bytes()
        with patch('storage.buyer_file.Path.replace', side_effect=OSError('cannot replace file')):
            with self.assertRaises(OSError):
                buyer_file.update_buyer(self.buyer('رضا'))
        self.assertEqual(self.path.read_bytes(), original)

    def test_plain_text_format_and_separators(self):
        buyer_file.insert_buyer(self.buyer())
        text = self.path.read_text(encoding='utf-8')
        self.assertEqual(text, '1|ali@example.com|Sample123|علی|احمدی|09123456789|تهران\n')
        for address in ['تهران|خیابان', 'تهران\nخیابان', 'تهران\rخیابان']:
            buyer = self.buyer()
            buyer.address = address
            with self.assertRaises(ValueError):
                buyer_file.update_buyer(buyer)
            self.assertEqual(self.path.read_text(encoding='utf-8'), text)

    def test_validation_and_order(self):
        for number in ['nan', 'inf', -1]:
            with self.assertRaises(ValueError):
                price_validator(number)
        for validator in [stock_validator, quantity_validator]:
            for number in [1.5, True, -1]:
                with self.assertRaises(ValueError):
                    validator(number)
        product = Product(1, 'دفتر', 200, 10)
        order = Order(1, self.buyer())
        order.add_item(OrderItem(1, product, 2, product.price))
        order.set_payment(Payment(1, order.total_price))
        self.assertEqual(order.total_price, 400)
        self.assertEqual(order.payment.amount, 400)

    def test_form_operations(self):
        import tkinter as tk
        from view.view import ShopWindow
        root = tk.Tk()
        root.withdraw()
        self.addCleanup(root.destroy)
        window = ShopWindow(root)
        values = dict(user_id='1', first_name='علی', last_name='احمدی',
                      email='ali@example.com', password='Sample123',
                      phone='09123456789', address='تهران')
        for name, value in values.items():
            window.entries[name].insert(0, value)
        with patch('view.view.messagebox.showinfo'), patch('view.view.messagebox.showerror') as error:
            window.add_buyer()
            self.assertEqual(len(window.table.get_children()), 1)
            window.table.selection_set('1')
            window.select_buyer()
            self.assertEqual(window.entries['phone'].get(), '09123456789')
            window.entries['first_name'].delete(0, tk.END)
            window.entries['first_name'].insert(0, 'رضا')
            window.edit_buyer()
            self.assertEqual(buyer_file.read_buyers()[0].first_name, 'رضا')
            window.table.selection_set('1')
            window.select_buyer()
            with patch('view.view.messagebox.askyesno', return_value=True):
                window.remove_buyer()
            self.assertEqual(buyer_file.read_buyers(), [])
            error.assert_not_called()

    def test_simple_text_validation(self):
        self.assertEqual(email_validator(' ali@example.com '), 'ali@example.com')
        for email in ['ali', '@example.com', 'ali@@example.com', 'ali@.com', 'ali@example.', 'a b@example.com']:
            with self.assertRaises(ValueError):
                email_validator(email)
        self.assertEqual(password_validator('Sample123'), 'Sample123')
        for password in ['short', 'sample123', 'Sampleabc']:
            with self.assertRaises(ValueError):
                password_validator(password)
        self.assertEqual(phone_validator('09123456789'), '09123456789')
        for phone in ['9123456789', '08123456789', '0912345678a']:
            with self.assertRaises(ValueError):
                phone_validator(phone)


if __name__ == '__main__':
    unittest.main()
