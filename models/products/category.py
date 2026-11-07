from validation.validation import id_validator, name_validator, address_validator


class Category:
    """کلاس دسته‌بندی کالاها"""

    def __init__(self, category_id, title, description="بدون توضیحات"):
        self.id = category_id
        self.title = title
        self.description = description
        self.products = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = id_validator(value, field_name="شناسه دسته‌بندی")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = name_validator(value, field_name="عنوان دسته‌بندی")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = address_validator(value, field_name="توضیحات دسته‌بندی")
