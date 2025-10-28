import abc
from Src.Core.common import common
from Src.Core.validator import validator, operation_exception
import json

"""
Абстрактный класс для наследования только dto структур
"""
class abstact_dto(metaclass=abc.ABCMeta):
    __name:str = ""
    __id:str = ""

    @property
    def name(self) ->str:
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value   

    # Универсальный фабричный метод для загрузщки dto из словаря
    def create(self, data) -> "abstact_dto":
        validator.validate(data, dict)
        fields = common.get_fields(self)
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self, key, data[ key ])
        except:
            raise   operation_exception("Невозможно загрузить данные!")    

        return self

    # конвертация dto в dict (можно переопределить для конкретного dto)
    def to_dict(self) -> dict:
        result_dict = {}
        fields = common.get_fields(self)
        for field in fields:
            value = getattr(self, field, None)
            # Если значение — объект DTO, рекурсивно преобразуем
            if hasattr(value, 'to_dict') and callable(value.to_dict):
                result_dict[field] = value.to_dict()
            else:
                result_dict[field] = value
        return result_dict

    # Перевод в строку json
    def to_json_string(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)