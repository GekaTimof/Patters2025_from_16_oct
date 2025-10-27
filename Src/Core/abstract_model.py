from abc import ABC
import uuid
from Src.Core.validator import validator

"""
Абстрактный класс для наследования моделей
Содержит в себе только генерацию уникального кода
"""
class abstact_model(ABC):
    __id: str

    def __init__(self) -> None:
        super().__init__()
        self.__id = uuid.uuid4().hex

    """
    Уникальный код
    """
    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, value: str):
        validator.validate(value, str)
        self.__id = value.strip()

    """
    Перегрузка штатного варианта сравнения
    """
    def __eq__(self, value) -> bool:
        if value is  None: return False
        if not isinstance(value, abstact_model): return False

        return self.id == value.id

