# setterهای کلاس‌ها توابع این فایل را صدا می‌زنند.
import math


def id_validator(value, field_name="شناسه"):
    text = str(value).strip()
    if not text.isdecimal() or int(text) < 1:
        raise ValueError(field_name + " باید عدد صحیح مثبت باشد.")
    return int(text)


def email_validator(email, field_name="ایمیل"):
    email = email.strip()
    parts = email.split("@")
    if len(parts) != 2 or not parts[0] or "." not in parts[1]:
        raise ValueError(field_name + " نامعتبر است.")
    for part in parts[1].split("."):
        if not part:
            raise ValueError(field_name + " نامعتبر است.")
    for char in email:
        if not char.isalnum() and char not in "._-@":
            raise ValueError(field_name + " نامعتبر است.")
    return email


def password_validator(password):
    has_upper = False
    has_digit = False
    for char in password:
        if "A" <= char <= "Z":
            has_upper = True
        if "0" <= char <= "9":
            has_digit = True
    if len(password) < 8 or not has_upper or not has_digit:
        raise ValueError("رمز باید حداقل ۸ نویسه، یک حرف بزرگ انگلیسی و یک عدد انگلیسی داشته باشد.")
    return password


def name_validator(value, field_name="نام"):
    value = value.strip()
    if len(value) < 2 or len(value) > 50:
        raise ValueError(field_name + " باید بین ۲ تا ۵۰ نویسه باشد.")
    return value


def phone_validator(phone):
    phone = phone.strip()
    if len(phone) != 11 or not phone.startswith("09") or not phone.isdecimal():
        raise ValueError("موبایل باید ۱۱ رقم باشد و با 09 شروع شود.")
    return phone


def address_validator(value, field_name="آدرس"):
    value = value.strip()
    if len(value) < 3 or len(value) > 250:
        raise ValueError(field_name + " باید بین ۳ تا ۲۵۰ نویسه باشد.")
    return value


def price_validator(value, field_name="قیمت"):
    try:
        price = float(value)
    except (ValueError, TypeError):
        raise ValueError(field_name + " باید عدد باشد.")
    # قیمت نباید منفی یا بی‌نهایت باشد.
    if not math.isfinite(price) or price < 0:
        raise ValueError(field_name + " باید عدد محدود و نامنفی باشد.")
    return price


def stock_validator(value):
    text = str(value).strip()
    if not text.isdecimal():
        raise ValueError("موجودی باید عدد صحیح نامنفی باشد.")
    return int(text)


def quantity_validator(value):
    return id_validator(value, "تعداد خرید")


def status_validator(value, allowed_statuses=None, field_name="وضعیت"):
    value = value.strip()
    if value == "":
        raise ValueError(field_name + " نباید خالی باشد.")
    if allowed_statuses is not None and value not in allowed_statuses:
        raise ValueError(field_name + " معتبر نیست.")
    return value


def object_validator(obj, expected_class, field_name="شیء"):
    # مثلاً خریدار سفارش باید از کلاس Buyer ساخته شده باشد.
    if not isinstance(obj, expected_class):
        raise ValueError(field_name + " از کلاس مورد انتظار نیست.")
    return obj
