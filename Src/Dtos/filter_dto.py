from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import operation_exception
from Src.Core.validator import argument_exception
from Src.Core.transform_dto import transform_dto

# Фильтрация, содержит:
# field_name - поле
# value - значение
# filter_types - тип фильтрации
class filter_dto(transform_dto):
    __value: str = ""
    __filter_type = ""
    __filter_types = {
        "EQUAL": "EQUAL",  # Полное совпадение
        "NOT_EQUAL": "NOT_EQUAL",  # Обратная операция, полное совпадение
        "LIKE": "LIKE",  # Вхождение строки
        "NOT_LIKE": "NOT_LIKE",  # Обратная операция, вхождение строки
        "GREATER": "GREATER",  # >
        "GREATER_OR_EQUAL": "GREATER_OR_EQUAL",  # >=
        "LESS": "LESS",  # <
        "LESS_OR_EQUAL": "LESS_OR_EQUAL"  # <=
    }

    def __init__(self, field_name="", value="", filter_type="EQUAL"):
        self.field_name = field_name
        self.value = value
        self.filter_type = filter_type

    @classmethod
    def get_filter_types(cls):
        return cls.__filter_types

    @classmethod
    def get_filter(cls, key: str):
        filter_types = cls.__filter_types
        try:
            return filter_types[key]
        except ValueError:
            return argument_exception("Non exist filter type")

    # Методы для получения позиции по ключам:
    @classmethod
    def equal_filter(cls):
        return cls.get_filter("EQUAL")

    @classmethod
    def not_equal_filter(cls):
        return cls.get_filter("NOT_EQUAL")

    @classmethod
    def like_filter(cls):
        return cls.get_filter("LIKE")

    @classmethod
    def not_like_filter(cls):
        return cls.get_filter("NOT_LIKE")

    @classmethod
    def greater_filter(cls):
        return cls.get_filter("GREATER")

    @classmethod
    def greater_or_equal_filter(cls):
        return cls.get_filter("GREATER_OR_EQUAL")

    @classmethod
    def less_filter(cls):
        return cls.get_filter("LESS")

    @classmethod
    def less_or_equal_filter(cls):
        return cls.get_filter("LESS_OR_EQUAL")

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value

    @property
    def filter_type(self) -> str:
        return self.__filter_type

    @filter_type.setter
    def filter_type(self, filter_type: str):
        if filter_type not in self.__filter_types:
            raise operation_exception(f"Undefined filter type {filter_type}")
        self.__filter_type = filter_type