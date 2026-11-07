from datetime import datetime
from validation.validation import id_validator, email_validator, password_validator


class User:
    """کلاس والد (پایه) برای تمامی کاربران سیستم فروشگاه"""

    def __init__(self, user_id, email, password):
        self.id = user_id
        self.email = email
        self.password = password
        self.created_at = datetime.now()

    # ---------------- ID ----------------
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = id_validator(value, field_name="شناسه کاربر (ID)")

    # ---------------- EMAIL ----------------
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = email_validator(value, field_name="ایمیل")

    # ---------------- PASSWORD ----------------
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = password_validator(value)
