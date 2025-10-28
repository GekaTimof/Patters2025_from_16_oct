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


    # Перевод в dto
    def to_dto(self):
        dto = self.dto_type()
        # Избегаем паралельный импорт
        from Src.Core.common import common

        # Проверяем все setters dto
        for arg in common.get_fields(dto):
            # Если нашли нужный параметр
            if arg in common.get_fields(self):
                # берём значение
                data = getattr(self, arg)
                # если список, проходим по каждому элементу
                if type(data) == list:
                    for item in data:
                        # Если объект является модель преобразуем в dto, а потом в dict
                        if "dto_type" in common.get_fields(item):
                            item = item.to_dto().to_dict()
                        getattr(dto, arg).append(item)
                else:
                    item = data
                    if "dto_type" in common.get_fields(item):
                        item = item.to_dto()
                    setattr(dto, arg, item)

            # Если нашит ссылку на нужный объект (вместо сложных оьбъектов dto хранит ссылку на этот объект, name + _id)
            elif len(arg) >= 3 and arg[-3:] == "_id" and arg[:-3] in common.get_fields(self):
                linked_obj = getattr(self, arg[:-3])
                setattr(dto, arg, linked_obj.id if linked_obj is not None else None)
            else:
                # Если не нашли нужное поле, пропускаем (будет пустое значение по умолчанию 0, None, "" и тд.)
                pass
        return dto