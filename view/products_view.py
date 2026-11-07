import tkinter as tk
from tkinter import ttk, messagebox
from models.products.product import Product
from models.products.category import Category
from models.users.seller import Seller
from models.orders.order import Order
from models.orders.order_item import OrderItem
from models.payments.payment import Payment
from storage.buyer_file import read_buyers, find_buyer
from storage.product_file import read_products, save_products
from validation.validation import quantity_validator


class ProductsWindow:
    def __init__(self, frame):
        self.products = []
        self.buyers = []
        self.order = None
        self.next_order_id = 1

        ttk.Label(frame, text="قیمت‌ها به تومان هستند؛ سفارش‌ها فقط در همین اجرا نگهداری می‌شوند.").pack(pady=6)
        form = ttk.Frame(frame)
        form.pack(fill=tk.X, padx=10)
        self.entries = {}
        fields = [("id", "شناسه"), ("name", "نام محصول"),
                  ("price", "قیمت واحد"), ("stock", "موجودی")]
        for name, label in fields:
            ttk.Label(form, text=label).pack(side=tk.LEFT, padx=4)
            entry = ttk.Entry(form, width=15)
            entry.pack(side=tk.LEFT)
            self.entries[name] = entry
        ttk.Button(form, text="ثبت محصول", command=self.add_product).pack(side=tk.LEFT, padx=8)

        columns = ("id", "name", "price", "stock", "category", "seller")
        self.table = ttk.Treeview(frame, columns=columns, show="headings", height=6, selectmode="browse")
        labels = ["شناسه", "محصول", "قیمت واحد (تومان)", "موجودی", "دسته‌بندی", "فروشنده"]
        for index in range(len(columns)):
            self.table.heading(columns[index], text=labels[index])
            self.table.column(columns[index], width=130, anchor=tk.CENTER)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, padx=10)
        ttk.Label(controls, text="خریدار:").pack(side=tk.LEFT)
        self.buyer_box = ttk.Combobox(controls, state="readonly", width=24)
        self.buyer_box.pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="به‌روزرسانی خریداران", command=self.load_buyers).pack(side=tk.LEFT)
        ttk.Button(controls, text="شروع سفارش جدید", command=self.start_order).pack(side=tk.LEFT, padx=5)
        ttk.Label(controls, text="تعداد خرید:").pack(side=tk.LEFT)
        self.quantity_entry = ttk.Entry(controls, width=6)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.pack(side=tk.LEFT)
        ttk.Button(controls, text="افزودن محصول انتخاب‌شده", command=self.add_item).pack(side=tk.LEFT, padx=5)

        self.order_label = ttk.Label(frame, text="ابتدا یک خریدار انتخاب و سفارش جدید شروع کنید.")
        self.order_label.pack(pady=6)
        columns = ("name", "price", "quantity", "total")
        self.order_table = ttk.Treeview(frame, columns=columns, show="headings", height=6)
        labels = ["محصول", "قیمت واحد (تومان)", "تعداد خرید", "جمع ردیف (تومان)"]
        for index in range(len(columns)):
            self.order_table.heading(columns[index], text=labels[index])
            self.order_table.column(columns[index], width=160, anchor=tk.CENTER)
        self.order_table.pack(fill=tk.BOTH, expand=True, padx=10)
        self.total_label = ttk.Label(frame, text="جمع سفارش: 0 تومان")
        self.total_label.pack(pady=6)
        ttk.Button(frame, text="پرداخت آزمایشی و کاهش موجودی", command=self.pay).pack(pady=6)
        try:
            self.products = read_products()
            self.show_products()
        except (ValueError, OSError) as error:
            messagebox.showerror("خطای محصولات", str(error))
        self.load_buyers()

    def show_products(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for product in self.products:
            self.table.insert("", tk.END, iid=str(product.id), values=(
                product.id, product.name, product.price, product.stock,
                product.category.title, product.seller.store_name))

    def add_product(self):
        try:
            # فایل دوباره خوانده می‌شود تا فایل خراب بازنویسی نشود.
            products = read_products()
            if products:
                category = products[0].category
                seller = products[0].seller
            else:
                category = Category(1, "لوازم تحریر")
                seller = Seller(1, "shop@example.com", "Sample123", "فروشگاه کلاس",
                                "09120000000", "support@example.com")
            product = Product(self.entries["id"].get(), self.entries["name"].get(),
                              self.entries["price"].get(), self.entries["stock"].get(),
                              category, seller)
            for old_product in products:
                if old_product.id == product.id:
                    raise ValueError("شناسهٔ محصول تکراری است.")
            products.append(product)
            save_products(products)
            category.products.append(product)
            self.products = products
            self.show_products()
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except (ValueError, OSError) as error:
            messagebox.showerror("خطا", str(error))

    def load_buyers(self):
        self.buyers = []
        self.buyer_box.set("")
        self.buyer_box["values"] = []
        try:
            self.buyers = read_buyers()
            names = []
            for buyer in self.buyers:
                names.append(str(buyer.id) + " - " + buyer.first_name + " " + buyer.last_name)
            self.buyer_box["values"] = names
            if names:
                self.buyer_box.current(0)
        except (ValueError, OSError) as error:
            messagebox.showerror("خطا", str(error))

    def start_order(self):
        index = self.buyer_box.current()
        if index < 0:
            messagebox.showerror("خطا", "در زبانهٔ خریداران فردی ثبت کنید و سپس فهرست خریداران را به‌روز کنید.")
            return
        try:
            buyer = find_buyer(self.buyers[index].id)
            if self.order is not None and self.order.items and self.order.status != "Paid":
                if not messagebox.askyesno("سفارش جدید", "سفارش پرداخت‌نشدهٔ فعلی کنار گذاشته شود؟"):
                    return
            self.order = Order(self.next_order_id, buyer)
            self.next_order_id += 1
            self.show_order()
        except (ValueError, OSError) as error:
            messagebox.showerror("خطا", str(error))

    def show_order(self):
        for row in self.order_table.get_children():
            self.order_table.delete(row)
        for item in self.order.items:
            self.order_table.insert("", tk.END, values=(item.product.name, item.unit_price,
                                                       item.quantity, item.unit_price * item.quantity))
        self.total_label.configure(text="جمع سفارش: " + str(self.order.total_price) + " تومان")
        status = "در انتظار پرداخت"
        if self.order.status == "Paid":
            status = "پرداخت آزمایشی انجام شد"
        self.order_label.configure(text="سفارش " + str(self.order.id) + " | " +
                                   self.order.buyer.first_name + " " + self.order.buyer.last_name + " | " + status)

    def add_item(self):
        try:
            if self.order is None:
                raise ValueError("ابتدا سفارش جدید شروع کنید.")
            if self.order.status == "Paid":
                raise ValueError("این سفارش پرداخت شده است؛ سفارش جدید شروع کنید.")
            selected = self.table.selection()
            if not selected:
                raise ValueError("یک محصول از جدول بالا انتخاب کنید.")
            quantity = quantity_validator(self.quantity_entry.get())
            for product in self.products:
                if str(product.id) == selected[0]:
                    needed = quantity
                    for item in self.order.items:
                        if item.product.id == product.id:
                            needed += item.quantity
                    if needed > product.stock:
                        raise ValueError("موجودی محصول برای این تعداد کافی نیست.")
                    item = OrderItem(len(self.order.items) + 1, product, quantity, product.price)
                    self.order.add_item(item)
                    self.show_order()
                    return
        except ValueError as error:
            messagebox.showerror("خطا", str(error))

    def pay(self):
        try:
            if self.order is None or not self.order.items:
                raise ValueError("ابتدا محصولی به سفارش اضافه کنید.")
            if self.order.status == "Paid":
                raise ValueError("این سفارش قبلاً پرداخت شده است.")
            buyer = find_buyer(self.order.buyer.id)
            # تغییرها روی لیست تازه انجام می‌شود؛ اگر ذخیره شکست بخورد، فرم تغییر نمی‌کند.
            products = read_products()
            for item in self.order.items:
                found = False
                for product in products:
                    if product.id == item.product.id:
                        found = True
                        if item.quantity > product.stock:
                            raise ValueError("موجودی کافی نیست: " + product.name)
                        product.stock -= item.quantity
                        break
                if not found:
                    raise ValueError("محصول در فایل پیدا نشد: " + item.product.name)
            payment = Payment(self.order.id, self.order.total_price, "Paid", "آزمایشی")
            save_products(products)
            self.order.buyer = buyer
            self.order.set_payment(payment)
            self.order.status = "Paid"
            self.products = products
            self.show_products()
            self.show_order()
            messagebox.showinfo("پرداخت آزمایشی", "موجودی ذخیره شد. هیچ پول واقعی جابه‌جا نشد.")
        except (ValueError, OSError) as error:
            messagebox.showerror("خطا", str(error))
