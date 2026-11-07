from models.users.user import User
from validation.validation import name_validator, phone_validator, email_validator


class Seller(User):
    """کلاس فروشنده (فرزند کلاس User)"""

    def __init__(self, user_id, email, password, store_name, phone, support_email):
        super().__init__(user_id, email, password)
        self.store_name = store_name
        self.phone = phone
        self.support_email = support_email

    # ---------------- STORE NAME ----------------
    @property
    def store_name(self):
        return self._store_name

    @store_name.setter
    def store_name(self, value):
        self._store_name = name_validator(value, field_name="نام فروشگاه")

    # ---------------- PHONE ----------------
    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = phone_validator(value)

    # ---------------- SUPPORT EMAIL ----------------
    @property
    def support_email(self):
        return self._support_email

    @support_email.setter
    def support_email(self, value):
        self._support_email = email_validator(value, field_name="ایمیل پشتیبانی")
