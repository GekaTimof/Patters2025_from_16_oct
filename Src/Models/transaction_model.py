from Src.Core.entity_model import abstact_model
from Src.Core.common import common
from Src.Core.validator import validator
from datetime import datetime
from Src.Models.range_model import range_model
from Src.Models.storage_model import storage_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Dtos.transaction_dto import transaction_dto
from Src.repository import reposity

# Модель транзакции
# Пример
#                "name":"-",
#                "id":"0c101a7e-5934-4155-83a6-d2c388fcc11a"
#                "date":"2025-11-02 14:30:45",
#                "storage_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",
#                "nomenclature_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",
#                "amount":10,
#                "range_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",

class transaction_model(abstact_model):
    __date: datetime = None
    __storage: storage_model = None
    __nomenclature: nomenclature_model = None
    __amount: int = 0
    __range: range_model = None
    __dto_type: transaction_dto = transaction_dto

    # подходящий тип dto
    @property
    def dto_type(self) -> transaction_dto:
        return self.__dto_type


    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value: datetime):
        validator.validate(value, datetime)
        self.__date = value


    @property
    def storage(self) -> storage_model:
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model):
        validator.validate(value, storage_model)
        self.__storage = value


    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value


    @property
    def amount(self) -> int:
        return self.__amount

    @amount.setter
    def amount(self, value: int):
        self.__amount = value


    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    """
    Универсальный фабричный метод
    """
    @staticmethod
    def create(_date: datetime):
        validator.validate(_date, datetime)

        item = transaction_model()
        item.date = _date
        return item

    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto: transaction_dto, cache: dict):
        validator.validate(dto, transaction_dto)
        validator.validate(cache, dict)

        item = transaction_model.create(common.convert_to_date(dto.date))

        item.storage = cache[dto.storage_id] if dto.storage_id in cache else None
        item.nomenclature = cache[dto.nomenclature_id] if dto.nomenclature_id in cache else None
        item.range = cache[dto.range_id] if dto.range_id in cache else None
        item.amount = int(dto.amount)

        return item

    # Переобразовать в dto
    def to_dto(self):
        return super().to_dto()