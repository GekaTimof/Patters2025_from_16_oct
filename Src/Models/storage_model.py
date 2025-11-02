from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Dtos.storage_dto import storage_dto

"""
Модель склада
"""
class storage_model(entity_model):
    __address: str = ""
    __dto_type = storage_dto

    # Адрес
    @property
    def address(self) -> str:
        return self.__address.strip()

    @address.setter
    def address(self, value: str):
        validator.validate(value, str)
        self.__address = value.strip()

    # Переобразовать в dto
    def to_dto(self):
        return super().to_dto()