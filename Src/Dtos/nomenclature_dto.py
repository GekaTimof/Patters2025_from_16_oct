from Src.Core.abstract_dto import abstract_dto
from Src.Core.common import common

# Модель номенклатуры (dto)
# Пример
#                "name":"Пшеничная мука",
#                "id":"0c101a7e-5934-4155-83a6-d2c388fcc11a"
#                "range_id":"a33dd457-36a8-4de6-b5f1-40afa6193346",
#                "category_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",

class nomenclature_dto(abstract_dto):
    __range_id: str = ""
    __group_id: str = ""

    @property
    def range_id(self) -> str:
        return self.__range_id

    @range_id.setter
    def range_id(self, value):
        self.__range_id = value

    @property
    def group_id(self) -> str:
        return self.__group_id

    @group_id.setter
    def group_id(self, value):
        self.__group_id = value
