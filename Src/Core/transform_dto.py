from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import operation_exception
from Src.Core.validator import argument_exception

# Базовое dto для всех преобразований, содержит:
# field_name - поле
class transform_dto(abstract_dto):
    __field_name: str = ""

    @property
    def field_name(self) -> str:
        return self.__field_name

    @field_name.setter
    def field_name(self, value: str):
        self.__field_name = value