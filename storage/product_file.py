from pathlib import Path
from models.products.product import Product
from models.products.category import Category
from models.users.seller import Seller


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "products.txt"


def read_products():
    # برای ساده ماندن پروژه، همهٔ کالاها یک فروشنده و دسته‌بندی دارند.
    category = Category(1, "لوازم تحریر")
    seller = Seller(1, "shop@example.com", "Sample123", "فروشگاه کلاس",
                    "09120000000", "support@example.com")
    products = []
    if not DATA_FILE.exists():
        return products
    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            fields = line.rstrip("\n").split("|")
            if len(fields) != 4:
                raise ValueError("هر خط فایل محصولات باید چهار قسمت داشته باشد.")
            product = Product(fields[0], fields[1], fields[2], fields[3], category, seller)
            for old_product in products:
                if old_product.id == product.id:
                    raise ValueError("شناسهٔ تکراری در فایل محصولات وجود دارد.")
            products.append(product)
            category.products.append(product)
    return products


def save_products(products):
    lines = []
    for product in products:
        if "|" in product.name or "\n" in product.name or "\r" in product.name:
            raise ValueError("نام محصول نباید علامت | یا خط جدید داشته باشد.")
        fields = [str(product.id), product.name, str(product.price), str(product.stock)]
        lines.append("|".join(fields) + "\n")
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = DATA_FILE.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        for line in lines:
            file.write(line)
    temporary.replace(DATA_FILE)
