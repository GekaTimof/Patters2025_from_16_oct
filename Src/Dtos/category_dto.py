from Src.Core.abstract_dto import abstact_dto
from Src.Core.common import common
import json

# Модель категории (dto)
# Пример
#               "name":"Ингредиенты",
#               "id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918"
class category_dto(abstact_dto):
   pass

   # # конвертация dto в dict
   # def to_dict(self) -> dict:
   #    result_dict = {}
   #    fields = common.get_fields(self)
   #    for field in fields:
   #       value = getattr(self, field, None)
   #       # Если значение — объект DTO, рекурсивно преобразуем
   #       if hasattr(value, 'to_json') and callable(value.to_json):
   #          result_dict[field] = value.to_json()
   #       else:
   #          result_dict[field] = value
   #    return result_dict
   #
   # # Перевод в строку json
   # def to_json_string(self) -> str:
   #   return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
