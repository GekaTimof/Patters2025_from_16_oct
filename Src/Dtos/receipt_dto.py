from Src.Core.abstract_dto import abstact_dto
from Src.Core.common import common
from Src.Core.validator import validator

# Модель рецепта (dto)
# Пример
#                "name":"Грамм",
#                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "portions": 1,
#                "receipt_items": []
#                "steps":" []
#                "cooking_time": "15 минут"

class receipt_dto(abstact_dto):
    __portion: int = 0
    __steps: list = []
    __receipt_items: list = []
    __cooking_time: str = ""


    @property
    def portion(self) -> int:
        return self.__portion

    @portion.setter
    def portion(self, value: int):
        self.__portion = value


    @property
    def steps(self) -> list:
        return self.__steps

    @steps.setter
    def steps(self, value: list):
        self.__steps = value


    @property
    def receipt_items(self) -> list:
        return self.__receipt_items

    @receipt_items.setter
    def receipt_items(self, value: list):
        self.__receipt_items = value


    @property
    def cooking_time(self) -> str:
        return self.__cooking_time

    @cooking_time.setter
    def cooking_time(self, value: str):
        self.__cooking_time = value