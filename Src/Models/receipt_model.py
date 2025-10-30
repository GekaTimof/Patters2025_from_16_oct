from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Core.abstract_dto import abstact_dto
from Src.Dtos.receipt_dto import receipt_dto


# Модель рецепта
class receipt_model(entity_model):
    # Количество порций
    __portions: int = 1
    # Шаги приготовления
    __steps: list = []
    # Список ингридиентов
    __receipt_items: list = []
    # Время приготовления
    __cooking_time: str = ""
    # Соответствующий dto
    __dto_type = receipt_dto

    # Подходящий тип dto
    @property
    def dto_type(self) -> receipt_dto:
        return self.__dto_type

    # Количество порций
    @property
    def portions(self) -> int:
        return self.__portions

    @portions.setter
    def portions(self, value: int):
        validator.validate(value, int)
        self.__portions = value

    # Шаги приготовления
    @property
    def steps(self) -> list:
        return self.__steps

    # Состав
    @property
    def receipt_items(self) -> list:
        return self.__receipt_items

    @receipt_items.setter
    def receipt_items(self, value: list):
        validator.validate(self, list)
        self.__receipt_items = value

    # Время приготовления
    @property
    def cooking_time(self) -> str:
        return self.__cooking_time

    @cooking_time.setter
    def cooking_time(self, value: str):
        validator.validate(value, str)
        self.__cooking_time = value.strip()

    # Фабричный метод для создания нового рецепта
    # Состав и шаги уже созданы. Будут пустыми
    @staticmethod
    def create(id: int, name: str, cooking_time: str, portions: int) -> "receipt_model":
        item = receipt_model()
        if id:
            item.id = id
        item.name = name
        item.cooking_time = cooking_time
        item.portions = portions
        return item

    # Переобразовать в dto
    def to_dto(self):
        return super().to_dto()