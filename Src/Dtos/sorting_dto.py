from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import operation_exception
from Src.Core.validator import argument_exception
from Src.Core.transform_dto import transform_dto

# Сортировка, содержит:
# field_name - поле
# value - значение
# sort_types - тип сортировки
class sorting_dto(transform_dto):
    __value: str = ""
    __sort_type: str = ""
    __sort_types = {
        "ASCENDING": "ASCENDING",  # сортировка по возрастанию
        "DESCENDING": "DESCENDING",  # сортировка по убыванию
    }

    def __init__(self, field_name="", value="", sort_type="ASCENDING"):
        self.field_name = field_name
        self.value = value
        self.sort_type = sort_type

    @classmethod
    def get_sort_types(cls):
        return cls.__sort_types

    @classmethod
    def get_sort_type(cls, key: str):
        sort_types = cls.__sort_types
        try:
            return sort_types[key]
        except KeyError:
            return argument_exception("Non exist sort type")

    @classmethod
    def ascending(cls):
        return cls.get_sort_type("ASCENDING")

    @classmethod
    def descending(cls):
        return cls.get_sort_type("DESCENDING")

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value

    @property
    def sort_type(self) -> str:
        return self.__sort_type

    @sort_type.setter
    def sort_type(self, sort_type: str):
        if sort_type not in self.__sort_types:
            raise argument_exception(f"Undefined sort type {sort_type}")
        self.__sort_type = sort_type
