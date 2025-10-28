from Src.Core.abstract_dto import abstact_dto
from Src.Core.common import common

# Модель группы номенклатук (dto)
# Пример
#                "name":"Ингредиенты",
#                "id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918"

class group_dto(abstact_dto):
    pass

    # # конвертация dto в dict
    # def to_dict(self) -> dict:
    #   _dict = {}
    #   fields = common.get_fields(self)
    #   for field in fields:
    #      value = getattr(self, field, None)
    #      _dict[field] = value
    #   return _dict
