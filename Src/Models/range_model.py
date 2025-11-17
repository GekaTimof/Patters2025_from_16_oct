from Src.Core.entity_model import entity_model
from Src.Core.validator import validator, argument_exception
from Src.Dtos.range_dto import range_dto
from Src.Core.abstract_dto import abstract_dto

"""
Модель единицы измерения
"""
class range_model(entity_model):
    __value: int = 1
    __base: 'range_model' = None
    __dto_type = range_dto

    # подходящий тип dto
    @property
    def dto_type(self) -> abstract_dto:
        return self.__dto_type

    """
    Значение коэффициента пересчета
    """
    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: int):
        validator.validate(value, int)
        if value <= 0:
            raise argument_exception("Некорректный аргумент!")
        self.__value = value

    """
    Базовая единица измерения
    """
    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self, value):
        self.__base = value


    """
    Универсальный метод - фабричный
    """
    @staticmethod
    def create(name: str, value: int, base: 'range_model' = None):
        validator.validate(name, str)
        validator.validate(value, int)

        inner_base = None
        if not base is None:
            validator.validate(base, range_model)
            inner_base = base
        item = range_model()
        item.name = name
        item.base = inner_base
        item.value = value
        return item

    """
    Фабричный метод из Dto
    """
    def from_dto(dto: range_dto, cache: dict):
        validator.validate(dto, range_dto)
        validator.validate(cache, dict)
        base = cache[dto.base_id] if dto.base_id in cache else None
        item = range_model.create(dto.name, int(dto.value), base)
        return item

    # Переобразовать в dto
    def to_dto(self):
        return super().to_dto()

    def get_effective_value(self) -> int:
        # Вычисляет итоговое значение с умножением на базовые коэффициенты рекурсивно.
        if self.base is None:
            return self.value
        else:
            return self.value * self.base.get_effective_value()

    def __eq__(self, other):
        if not isinstance(other, range_model):
            return NotImplemented
        return self.get_effective_value() == other.get_effective_value()

    def __lt__(self, other):
        if not isinstance(other, range_model):
            return NotImplemented
        return self.get_effective_value() < other.get_effective_value()

    def __le__(self, other):
        if not isinstance(other, range_model):
            return NotImplemented
        return self.get_effective_value() <= other.get_effective_value()

    def __gt__(self, other):
        if not isinstance(other, range_model):
            return NotImplemented
        return self.get_effective_value() > other.get_effective_value()

    def __ge__(self, other):
        if not isinstance(other, range_model):
            return NotImplemented
        return self.get_effective_value() >= other.get_effective_value()