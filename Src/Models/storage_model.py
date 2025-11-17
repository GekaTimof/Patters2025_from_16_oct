from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Dtos.storage_dto import storage_dto

"""
Модель склада
"""
class storage_model(entity_model):
    __address: str = ""
    __dto_type: storage_dto = storage_dto

    # подходящий тип dto
    @property
    def dto_type(self) -> storage_dto:
        return self.__dto_type


    # Адрес
    @property
    def address(self) -> str:
        return self.__address.strip()

    @address.setter
    def address(self, value: str):
        validator.validate(value, str)
        self.__address = value.strip()


    # Универсальный фабричный метод
    @staticmethod
    def create(name: str, adress: str):
        validator.validate(name, str)
        validator.validate(adress, str)

        item = storage_model()
        item.name = name
        item.address = adress
        return item


    # Фабричный метод из Dto
    @staticmethod
    def from_dto(dto: storage_dto, cache: dict):
        validator.validate(dto, storage_dto)
        validator.validate(cache, dict)

        item = storage_model.create(dto.name, dto.address)
        return item


    # Переобразовать в dto
    def to_dto(self):
        return super().to_dto()

    def __eq__(self, other):
        if not isinstance(other, storage_model):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, storage_model):
            return NotImplemented
        return self.name < other.name

    def __le__(self, other):
        if not isinstance(other, storage_model):
            return NotImplemented
        return self.name <= other.name

    def __gt__(self, other):
        if not isinstance(other, storage_model):
            return NotImplemented
        return self.name > other.name

    def __ge__(self, other):
        if not isinstance(other, storage_model):
            return NotImplemented
        return self.name >= other.name