import json
from Src.Core.common import common
from Src.Core.transform_dto import transform_dto
from Src.Core.validator import operation_exception

class factory_transform:
    def __init__(self):
        # Словарь {имя_класса: класс-наследник transform_dto}
        self.dto_classes = common.get_all_subclasses_dict(transform_dto)

    # Возвращает dto подходящий под поля списка
    def create(self, data: dict) -> transform_dto:
        for class_name, dto_class in self.dto_classes.items():
            # Получаем поля класса dtо
            dto_fields = common.get_setters(dto_class)

            # Проверяем, что все поля data есть в dto
            if dto_fields and set(data.keys()).issubset(set(dto_fields)):
                instance = dto_class()
                return instance
        raise operation_exception("Can't create dto from this dict - fields no matching")


    def create_and_fill(self, data: dict) -> transform_dto:
        dto_instance = self.create(data)

        # Заполняем поля из data в экземпляр dto
        for key, value in data.items():
            if hasattr(dto_instance, key):
                setattr(dto_instance, key, value)
            else:
                raise operation_exception("Can't fill dto from this dict - fields no matching")
        return dto_instance


