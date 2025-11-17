import json

from Src.Core.common import common
from Src.Core.abstract_dto import abstract_dto

class convert_factory:
    def __init__(self):
        # Словарь {имя_класса: класс-наследник abstract_dto}
        self.dto_classes = common.get_all_subclasses_dict(abstract_dto)

    # Возвращает dto соответствующее объекту
    def create(self, obj) -> abstract_dto:
        if common.can_convert_to_dto(obj):
            class_name = obj.dto_type.__name__
            # проверяем, что класс наследован от abstract_dto
            if class_name not in self.dto_classes.keys():
                raise ValueError(f"Неизвестный тип DTO: {class_name}")
            # создаём dto
            return obj.to_dto()
        else:
            raise ValueError(f"Объект {obj} не имеет метода конвертации в dto")

    # Возвращает dict|list преобразованный в словарь
    def create_dict_from_dto(self, data) -> dict|list:
        # если получен словарь (вернём словарь)
        if type(data) == dict:
            result = {}
            for key in data.keys():
                # конвертирует только те объекты, у которых есть dto_type (их можно преобразовать в dto)
                objects_list = data.get(key, [])
                filtered_list = []
                for obj in objects_list:
                    # преобразовываем объекты, которые можно преобразовать в dto
                    if common.can_convert_to_dto(obj):
                        dto = self.create(obj)
                        filtered_list.append(dto.to_dict())
                result[key] = filtered_list
        # если получен массив или 1 объект (вернём массив)
        else:
            result = []
            for obj in data:
                # преобразовываем объекты, которые можно преобразовать в dto
                if common.can_convert_to_dto(obj):
                    dto = self.create(obj)
                    result.append(dto.to_dict())

        return result