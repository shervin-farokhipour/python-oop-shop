from models.users.user import User
from validation.validation import name_validator, phone_validator, address_validator


class Buyer(User):
    """کلاس خریدار (فرزند کلاس User)"""

    def __init__(self, user_id, email, password, first_name, last_name="تستی", phone="09120000000", address="تهران"):
        super().__init__(user_id, email, password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address

    # ---------------- FIRST NAME ----------------
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = name_validator(value, field_name="نام")

    # ---------------- LAST NAME ----------------
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = name_validator(value, field_name="نام خانوادگی")

    # ---------------- PHONE ----------------
    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = phone_validator(value)

    # ---------------- ADDRESS ----------------
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = address_validator(value, field_name="آدرس")
