from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator

# Модель склада (dto)
# Пример
#                "name":"Склад 1",
#                "id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918"
#                "address":"какой-то адресс"

class storage_dto(abstract_dto):
    __address: str = ""

    # Адрес
    @property
    def address(self) -> str:
        return self.__address.strip()

    @address.setter
    def address(self, value: str):
        validator.validate(value, str)
        self.__address = value.strip()