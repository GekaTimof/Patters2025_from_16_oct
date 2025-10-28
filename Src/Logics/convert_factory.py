import json

from Src.Core.common import common
from Src.Core.abstract_dto import abstact_dto

class convert_factory:
    def __init__(self):
        # Словарь {имя_класса: класс-наследник abstact_dto}
        self.dto_classes = common.get_all_subclasses_dict(abstact_dto)

    # Возвращает dto соответствующее объекту
    def create(self, obj) -> abstact_dto:
        if common.can_convert_to_dto(obj):
            class_name = obj.dto_type.__name__
            # проверяем, что класс наследован от abstact_dto
            if class_name not in self.dto_classes.keys():
                raise ValueError(f"Неизвестный тип DTO: {class_name}")
            # создаём dto
            return obj.to_dto()
        else:
            raise ValueError(f"Объект {obj} не имеет метода конвертации в dto")

    # Возвращает response в формате dict описание всего сервиса
    def create_dict_repository(self, repository) -> dict:
        result_dict = {}
        repository_keys = repository.keys()

        for key in repository_keys:
            # конвертирует только те объекты, у которых есть dto_type (их можно преобразовать в dto)
            objects_list = repository.data.get(key, [])
            filtered_list = []
            for obj in objects_list:
                # преобразовываем объекты, которые можно преобразовать в dto
                if "dto_type" in common.get_fields(obj):
                    dto = self.create(obj)
                    filtered_list.append(dto.to_dict())
            result_dict[key] = filtered_list
        return result_dict

    def create_json_settings(self, service) -> str:
        result_json = {}
        result_json["is_firs_start"] = False
        result_json["company"] = {}
        result_json["repository"] = self.create_dict_repository(service.repository)
        return json.dumps(result_json, ensure_ascii=False, indent=2)
