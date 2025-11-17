from Src.Core.entity_model import entity_model
from Src.Core.abstract_dto import abstract_dto
from Src.Dtos.group_dto import group_dto

"""
Модель группы номенклатуры
"""
class group_model(entity_model):
    __dto_type = group_dto

    # Подходящий тип dto
    @property
    def dto_type(self) -> abstract_dto:
        return self.__dto_type

    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto: abstract_dto, cache: dict):
        item = group_model()
        item.name = dto.name
        item.id = dto.id
        return item

    # Переобразовать в dto
    def to_dto(self):
        return super().to_dto()
