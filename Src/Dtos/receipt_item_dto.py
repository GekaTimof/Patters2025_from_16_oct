from Src.Core.abstract_dto import abstact_dto
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Core.common import common

# Модель единицы измерения (dto)
# Пример
#                "name":"Грамм",
#                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "nomenclature_id":"a33dd457-36a8-4de6-b5f1-40afa6193346",
#                "range_id":"a33dd457-36a8-4de6-b5f1-40afa6193346",
#                "value":1

class receipt_item_dto(abstact_dto):
    __nomenclature_id: str = None
    __range_id: str = None
    __value: int = 0

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value: str):
        self.__nomenclature_id = value

    @property
    def range_id(self) -> str:
        return self.__range_id

    @range_id.setter
    def range_id(self, value):
        self.__range_id = value

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    # # конвертация dto в dict
    # def to_dict(self) -> dict:
    #     _dict = {}
    #     fields = common.get_fields(self)
    #     for field in fields:
    #         value = getattr(self, field, None)
    #         _dict[field] = value
    #     return _dict
