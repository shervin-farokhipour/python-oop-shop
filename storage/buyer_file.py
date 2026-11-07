from pathlib import Path
from models.users.buyer import Buyer
from validation.validation import id_validator


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "buyers.txt"


def buyer_id(buyer):
    return buyer.id


def read_buyers():
    if not DATA_FILE.exists():
        return []
    buyers = []
    ids = []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            # هر خط اطلاعات یک خریدار است؛ علامت | فیلدها را جدا می‌کند.
            fields = line.rstrip("\n").split("|")
            if len(fields) != 7:
                raise ValueError(f"خط {line_number} فایل خریداران باید ۷ قسمت داشته باشد.")
            try:
                buyer = Buyer(fields[0], fields[1], fields[2], fields[3],
                              fields[4], fields[5], fields[6])
                if buyer.id in ids:
                    raise ValueError("شناسه تکراری است.")
            except ValueError as error:
                raise ValueError(f"خط {line_number} فایل خریداران: {error}")
            ids.append(buyer.id)
            buyers.append(buyer)
    return sorted(buyers, key=buyer_id)


def save_buyers(buyers):
    lines = []
    for buyer in buyers:
        fields = [str(buyer.id), buyer.email, buyer.password, buyer.first_name,
                  buyer.last_name, buyer.phone, buyer.address]
        for value in fields:
            if "|" in value or "\n" in value or "\r" in value:
                raise ValueError("در اطلاعات خریدار از علامت | یا خط جدید استفاده نکنید.")
        lines.append("|".join(fields) + "\n")
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    # ابتدا فایل موقت نوشته می‌شود تا هنگام خطا اطلاعات قبلی حفظ شود.
    temporary = DATA_FILE.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        for line in lines:
            file.write(line)
    temporary.replace(DATA_FILE)


def insert_buyer(buyer):
    buyers = read_buyers()
    for old_buyer in buyers:
        if old_buyer.id == buyer.id:
            raise ValueError("این شناسه قبلاً ثبت شده است.")
    buyers.append(buyer)
    save_buyers(buyers)


def find_buyer(user_id):
    # اطلاعات تازه از فایل خوانده می‌شود؛ فهرست داخل فرم ممکن است قدیمی باشد.
    user_id = id_validator(user_id)
    for buyer in read_buyers():
        if buyer.id == user_id:
            return buyer
    raise ValueError("این خریدار دیگر وجود ندارد؛ فهرست خریداران را به‌روز کنید.")


def search_buyers(text):
    text = text.strip().lower()
    result = []
    for buyer in read_buyers():
        values = [str(buyer.id), buyer.first_name, buyer.last_name, buyer.email]
        for value in values:
            if text in value.lower():
                result.append(buyer)
                break
    return result


def update_buyer(buyer):
    buyers = read_buyers()
    for index in range(len(buyers)):
        if buyers[index].id == buyer.id:
            buyers[index] = buyer
            save_buyers(buyers)
            return
    raise ValueError("خریداری با این شناسه پیدا نشد.")


def delete_buyer(user_id):
    user_id = id_validator(user_id)
    buyers = read_buyers()
    for buyer in buyers:
        if buyer.id == user_id:
            buyers.remove(buyer)
            save_buyers(buyers)
            return
    raise ValueError("خریداری با این شناسه پیدا نشد.")
