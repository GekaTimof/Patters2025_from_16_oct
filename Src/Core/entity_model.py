from Src.Core.abstract_model import abstact_model
from Src.Core.validator import validator
from Src.Core.validator import convertation_exception

"""
Общий класс для наследования. Содержит стандартное определение: код, наименование
"""
class entity_model(abstact_model):
    __name:str = ""
    __dto_type: "abstact_dto"

    # # подходящий тип dto
    # @abc.abstractmethod
    def dto_type(self) -> "abstact_dto":
        return self.__dto_type

    # Наименование
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str):
        validator.validate(value, str)
        self.__name = value.strip()


    # Фабричный метод
    @staticmethod
    def create(name:str):
        item = entity_model()
        item.name = name
        return item


    # Перевод в dto
    def to_dto(self):
        dto = self.dto_type()
        # избегаем паралельный импорт
        from Src.Core.common import common

        # проверяем все setterы dto
        for arg in common.get_fields(dto):
            # если нашли нужный объект
            if arg in common.get_fields(self):
                setattr(dto, arg, getattr(self, arg))
            # если нашит ссылку на нужный объект (вместо сложных оьбъектов dto хранит ссылку на этот объект, name + _id)
            elif len(arg) >= 3 and arg[-3:] == "_id" and arg[:-3] in common.get_fields(self):
                linked_obj = getattr(self, arg[:-3])
                if linked_obj is not None:
                    setattr(dto, arg, linked_obj.id)
                else:
                    setattr(dto, arg, None)
            else:
                raise convertation_exception(f"не возможно конвертироать в dto аргумент {arg} отсутствует")
        return dto