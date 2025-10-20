from Src.Core.abstract_dto import abstact_dto
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model

# Модель единицы измерения (dto)
# Пример
#                "name":"Грамм",
#                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "nomenclature":null,
#                "range_id":"a33dd457-36a8-4de6-b5f1-40afa6193346",
#                "value":1

class receipt_item_dto(abstact_dto):
    __nomenclature: nomenclature_model
    __range: range_model
    __value: int

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value):
        self.__nomenclature = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value):
        self.__range = value

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value