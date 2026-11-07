from datetime import datetime
from models.users.buyer import Buyer
from models.orders.order_item import OrderItem
from models.payments.payment import Payment
from validation.validation import id_validator, status_validator, object_validator


class Order:
    """کلاس سفارش (دارای رابطه Composition با OrderItem و Payment)"""

    ALLOWED_STATUSES = ["Pending", "Paid", "Shipped", "Cancelled", "در انتظار", "تکمیل شده", "لغو شده"]

    def __init__(self, order_id, buyer_obj, status="Pending"):
        self.id = order_id
        self.buyer = buyer_obj
        self.created_at = datetime.now()
        self.status = status

        # لیست آیتم‌ها و وضعیت پرداخت (Composition)
        self.items = []
        self.payment = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = id_validator(value, field_name="شناسه سفارش")

    @property
    def buyer(self):
        return self._buyer

    @buyer.setter
    def buyer(self, value):
        self._buyer = object_validator(value, Buyer, field_name="خریدار")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = status_validator(value, self.ALLOWED_STATUSES, field_name="وضعیت سفارش")

    @property
    def total_price(self):
        # جمع از روی ردیف‌های فعلی محاسبه می‌شود، پس با تغییر تعداد قدیمی نمی‌ماند.
        total = 0
        for item in self.items:
            total += item.unit_price * item.quantity
        return total

    def add_item(self, order_item_obj):
        """اضافه کردن یک ردیف معتبر به سفارش"""
        object_validator(order_item_obj, OrderItem, field_name="آیتم سفارش")
        self.items.append(order_item_obj)

    def set_payment(self, payment_obj):
        """ثبت وضعیت پرداخت سفارش"""
        object_validator(payment_obj, Payment, field_name="پرداخت")
        self.payment = payment_obj
