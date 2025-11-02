from Src.Core.abstract_model import abstact_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator
from Src.Dtos.receipt_item_dto import receipt_item_dto
from Src.Core.validator import argument_exception

# Модель элемента рецепта
class receipt_item_model(abstact_model):
    __nomenclature: nomenclature_model
    __range: range_model
    __value: int
    __dto_type = receipt_item_dto

    # подходящий тип dto
    @property
    def dto_type(self) -> receipt_item_dto:
        return self.__dto_type

    # Номенклатура
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    # Единица измерения
    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    # Количество
    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, val: int):
        validator.validate(val, int, min_lim=0)
        self.__value = val

    # Фабричный метод
    @staticmethod
    def create(nomenclature: nomenclature_model, range: range_model, value: int):
        item = receipt_item_model()
        item.__nomenclature = nomenclature
        item.__range = range
        item.__value = value
        return item

    # Фабричный метод из Dto
    @staticmethod
    def from_dto(dto:receipt_item_dto, cache:dict):
        validator.validate(dto, receipt_item_dto)
        validator.validate(cache, dict)
        nomenclature = cache[dto.nomenclature_id] if dto.nomenclature_id in cache else None
        range = cache[dto.range_id] if dto.range_id in cache else None
        item = receipt_item_model.create(nomenclature, range, dto.value)
        return item

    # Переобразовать в dto
    def to_dto(self):
        return super().to_dto()