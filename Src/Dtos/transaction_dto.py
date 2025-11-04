from Src.Core.abstract_dto import abstact_dto
from Src.Core.common import common
from datetime import datetime

# Модель транзакции (dto)
# Пример
#                "name":"-",
#                "id":"0c101a7e-5934-4155-83a6-d2c388fcc11a"
#                "date":"2025-11-02" | "2025-11-02 14:30:45",
#                "storage_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",
#                "nomenclature_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",
#                "amount":10,
#                "range_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",

class transaction_dto(abstact_dto):
    __date: str = ""
    __storage_id: str = ""
    __nomenclature_id: str = ""
    __amount: str = 0
    __range_id: str = ""

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value: datetime|str):
        self.__date = str(value)


    @property
    def storage_id(self) -> str:
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value: str):
        self.__storage_id = value


    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value: str):
        self.__nomenclature_id = value


    @property
    def amount(self) -> str:
        return self.__amount

    @amount.setter
    def amount(self, value: int|str):
        self.__amount = str(value)


    @property
    def range_id(self) -> str:
        return self.__range_id

    @range_id.setter
    def range_id(self, value: str):
        self.__range_id = value
