import tkinter as tk
from tkinter import ttk, messagebox
from models.users.buyer import Buyer
from storage.buyer_file import read_buyers, insert_buyer, update_buyer, delete_buyer, search_buyers
from view.products_view import ProductsWindow


class ShopWindow:
    def __init__(self, root):
        self.root = root
        self.buyers = []
        root.title("فروشگاه ساده — خریداران، محصولات و سفارش")
        root.geometry("1180x720")
        root.minsize(1100, 680)
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)
        buyers_tab = ttk.Frame(notebook)
        products_tab = ttk.Frame(notebook)
        notebook.add(buyers_tab, text="خریداران")
        notebook.add(products_tab, text="محصولات و سفارش")

        form = ttk.Frame(buyers_tab, padding=15)
        form.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Label(form, text="اطلاعات خریدار").pack(pady=8)
        fields = [
            ("user_id", "شناسه"), ("first_name", "نام"),
            ("last_name", "نام خانوادگی"), ("email", "ایمیل"),
            ("password", "رمز عبور (۸ کاراکتر، حرف بزرگ و عدد)"),
            ("phone", "شماره موبایل"), ("address", "آدرس"),
        ]
        self.entries = {}
        for name, label in fields:
            ttk.Label(form, text=label).pack(pady=(5, 0))
            entry = ttk.Entry(form, width=30)
            if name == "password":
                entry.configure(show="*")
            entry.pack()
            self.entries[name] = entry

        for text, command in [
            ("ثبت", self.add_buyer), ("ویرایش", self.edit_buyer),
            ("حذف", self.remove_buyer), ("پاک کردن فرم", self.clear_form),
        ]:
            ttk.Button(form, text=text, command=command).pack(fill=tk.X, pady=4)

        panel = ttk.Frame(buyers_tab, padding=10)
        panel.pack(fill=tk.BOTH, expand=True)
        search_frame = ttk.Frame(panel)
        search_frame.pack(fill=tk.X, pady=8)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="جستجو", command=self.search).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="نمایش همه", command=self.show_all).pack(side=tk.LEFT)

        columns = ("id", "first_name", "last_name", "email", "phone", "address")
        self.table = ttk.Treeview(panel, columns=columns, show="headings", selectmode="browse")
        labels = ["شناسه", "نام", "نام خانوادگی", "ایمیل", "موبایل", "آدرس"]
        for index in range(len(columns)):
            column = columns[index]
            label = labels[index]
            self.table.heading(column, text=label)
            self.table.column(column, width=110, minwidth=60, anchor=tk.CENTER)
        scrollbar = ttk.Scrollbar(panel, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(fill=tk.BOTH, expand=True)
        self.table.bind("<<TreeviewSelect>>", self.select_buyer)
        self.show_all()
        self.products_window = ProductsWindow(products_tab)

    def clear_form(self):
        for entry in self.entries.values():
            entry.configure(state="normal")
            entry.delete(0, tk.END)
        self.table.selection_remove(self.table.selection())

    def make_buyer(self):
        values = {}
        for name, entry in self.entries.items():
            values[name] = entry.get()
        return Buyer(values["user_id"], values["email"], values["password"],
                     values["first_name"], values["last_name"],
                     values["phone"], values["address"])

    def fill_table(self, buyers):
        self.buyers = buyers
        for row in self.table.get_children():
            self.table.delete(row)
        for buyer in buyers:
            self.table.insert("", tk.END, iid=str(buyer.id), values=(
                buyer.id, buyer.first_name, buyer.last_name,
                buyer.email, buyer.phone, buyer.address,
            ))

    def show_all(self):
        try:
            self.fill_table(read_buyers())
            self.search_entry.delete(0, tk.END)
        except (ValueError, OSError) as error:
            messagebox.showerror("خطای خواندن فایل", str(error))

    def select_buyer(self, event=None):
        selected = self.table.selection()
        if not selected:
            return
        user_id = int(selected[0])
        for buyer in self.buyers:
            if buyer.id == user_id:
                values = dict(user_id=buyer.id, first_name=buyer.first_name,
                              last_name=buyer.last_name, email=buyer.email,
                              password=buyer.password, phone=buyer.phone, address=buyer.address)
                for name, value in values.items():
                    entry = self.entries[name]
                    entry.configure(state="normal")
                    entry.delete(0, tk.END)
                    entry.insert(0, value)
                self.entries["user_id"].configure(state="readonly")
                return

    def add_buyer(self):
        try:
            insert_buyer(self.make_buyer())
            self.show_all()
            self.clear_form()
            messagebox.showinfo("ثبت", "خریدار در فایل ذخیره شد.")
        except (ValueError, OSError) as error:
            messagebox.showerror("خطا", str(error))

    def edit_buyer(self):
        try:
            update_buyer(self.make_buyer())
            self.show_all()
            self.clear_form()
            messagebox.showinfo("ویرایش", "اطلاعات ویرایش شد.")
        except (ValueError, OSError) as error:
            messagebox.showerror("خطا", str(error))

    def remove_buyer(self):
        if not messagebox.askyesno("حذف", "خریدار حذف شود؟"):
            return
        try:
            delete_buyer(self.entries["user_id"].get())
            self.show_all()
            self.clear_form()
        except (ValueError, OSError) as error:
            messagebox.showerror("خطا", str(error))

    def search(self):
        try:
            self.fill_table(search_buyers(self.search_entry.get()))
        except (ValueError, OSError) as error:
            messagebox.showerror("خطا", str(error))


def run():
    root = tk.Tk()
    ShopWindow(root)
    root.mainloop()
