import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch
from tkinter import ttk
from storage import product_file, buyer_file
from models.users.buyer import Buyer
from view.products_view import ProductsWindow


class ProductTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.product_path = Path(temporary.name) / 'products.txt'
        self.product_path.write_text('1|دفتر|200|10\n', encoding='utf-8')
        for module, path in [(product_file, self.product_path),
                             (buyer_file, Path(temporary.name) / 'buyers.txt')]:
            patcher = patch.object(module, 'DATA_FILE', path)
            patcher.start()
            self.addCleanup(patcher.stop)
        buyer_file.insert_buyer(Buyer(1, 'ali@example.com', 'Sample123', 'علی'))
        root = tk.Tk()
        root.withdraw()
        self.addCleanup(root.destroy)
        self.window = ProductsWindow(ttk.Frame(root))

    def test_order_and_payment(self):
        window = self.window
        window.start_order()
        window.table.selection_set('1')
        window.quantity_entry.delete(0, tk.END)
        window.quantity_entry.insert(0, '2')
        window.add_item()
        self.assertEqual(window.order.total_price, 400)
        self.assertEqual(len(window.order_table.get_children()), 1)
        self.assertEqual(window.order.items[0].product.category.products[0].id, 1)
        self.assertEqual(window.order.items[0].product.seller.store_name, 'فروشگاه کلاس')
        with patch('view.products_view.messagebox.showinfo'):
            window.pay()
        self.assertEqual(window.order.payment.amount, 400)
        self.assertEqual(window.order.status, 'Paid')
        self.assertEqual(product_file.read_products()[0].stock, 8)
        with patch('view.products_view.messagebox.showerror') as error:
            window.pay()
            error.assert_called_once()
        self.assertEqual(product_file.read_products()[0].stock, 8)

    def test_stock_and_failed_save(self):
        window = self.window
        window.start_order()
        window.table.selection_set('1')
        window.quantity_entry.delete(0, tk.END)
        window.quantity_entry.insert(0, '6')
        window.add_item()
        with patch('view.products_view.messagebox.showerror') as error:
            window.add_item()
            error.assert_called_once()
        self.assertEqual(len(window.order.items), 1)
        with patch('view.products_view.save_products', side_effect=OSError('write failed')):
            with patch('view.products_view.messagebox.showerror'):
                window.pay()
        self.assertEqual(window.order.status, 'Pending')
        self.assertIsNone(window.order.payment)
        self.assertEqual(product_file.read_products()[0].stock, 10)

    def test_add_product_and_reload(self):
        window = self.window
        for name, value in [('id', '2'), ('name', 'مداد'), ('price', '100'), ('stock', '5')]:
            window.entries[name].insert(0, value)
        window.add_product()
        products = product_file.read_products()
        self.assertEqual(len(products), 2)
        self.assertEqual(products[1].price, 100)
        self.assertEqual(products[1].stock, 5)
        self.assertEqual(len(products[1].category.products), 2)
        self.assertEqual(len(window.table.get_children()), 2)

    def test_deleted_buyer_cannot_start_order(self):
        buyer_file.delete_buyer(1)
        with patch('view.products_view.messagebox.showerror') as error:
            self.window.start_order()
            error.assert_called_once()
        self.assertIsNone(self.window.order)
        self.assertEqual(self.window.next_order_id, 1)

    def test_deleted_buyer_cannot_pay(self):
        window = self.window
        window.start_order()
        window.table.selection_set('1')
        window.add_item()
        buyer_file.delete_buyer(1)
        original = self.product_path.read_bytes()
        with patch('view.products_view.messagebox.showerror') as error:
            window.pay()
            error.assert_called_once()
        self.assertEqual(self.product_path.read_bytes(), original)
        self.assertEqual(window.order.status, 'Pending')
        self.assertIsNone(window.order.payment)

    def test_start_order_reads_updated_buyer(self):
        buyer_file.update_buyer(Buyer(1, 'ali@example.com', 'Sample123', 'رضا'))
        self.window.start_order()
        self.assertEqual(self.window.order.buyer.first_name, 'رضا')

    def test_payment_uses_updated_buyer_and_total(self):
        window = self.window
        window.start_order()
        window.table.selection_set('1')
        window.add_item()
        window.order.items[0].quantity = 3
        buyer_file.update_buyer(Buyer(1, 'ali@example.com', 'Sample123', 'رضا'))
        with patch('view.products_view.messagebox.showinfo'):
            window.pay()
        self.assertEqual(window.order.buyer.first_name, 'رضا')
        self.assertEqual(window.order.payment.amount, 600)
        self.assertEqual(product_file.read_products()[0].stock, 7)


if __name__ == '__main__':
    unittest.main()
