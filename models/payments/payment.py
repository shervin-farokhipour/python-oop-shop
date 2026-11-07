from validation.validation import id_validator, price_validator, status_validator, name_validator


class Payment:
    """کلاس پرداخت سفارش"""

    ALLOWED_STATUSES = ["Pending", "Paid", "Failed", "در انتظار", "پرداخت شده", "ناموفق"]

    def __init__(self, payment_id, amount, status="Pending", gateway="زرین‌پال"):
        self.id = payment_id
        self.amount = amount
        self.status = status
        self.gateway = gateway

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = id_validator(value, field_name="شناسه پرداخت")

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = price_validator(value, field_name="مبلغ پرداخت")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = status_validator(value, self.ALLOWED_STATUSES, field_name="وضعیت پرداخت")

    @property
    def gateway(self):
        return self._gateway

    @gateway.setter
    def gateway(self, value):
        self._gateway = name_validator(value, field_name="درگاه پرداخت")
