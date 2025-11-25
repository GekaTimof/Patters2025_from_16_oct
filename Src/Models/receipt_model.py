from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Core.validator import argument_exception
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

    @steps.setter
    def steps(self, value: list):
        validator.validate(self, list)
        self.__steps = value

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
    def create(id: str,
               name: str,
               portions: int = 0,
               cooking_time: str = "",
               receipt_items: list =[],
               steps: list = []) -> "receipt_model":
        item = receipt_model()
        # пересзаписываем id, если есть
        if id:
            item.id = id
        item.name = name
        item.portions = portions
        if cooking_time:
            item.cooking_time = cooking_time
        if steps:
            item.steps = steps
        if receipt_items:
            item.receipt_items = receipt_items
        return item

    """
     Фабричный метод из Dto
     """
    @staticmethod
    def from_dto(dto: receipt_dto, cache: dict):
        validator.validate(dto, receipt_dto)
        validator.validate(cache, dict)
        receipt_items = cache[dto.receipt_items] if dto.receipt_items in cache else None
        item = receipt_model.create(
            id=dto.id,
            name=dto.name,
            portions=dto.portions,
            cooking_time=dto.cooking_time,
            steps=dto.steps,
            receipt_items=receipt_items
        )
        return item

    # Переобразовать в dto
    def to_dto(self):
        return super().to_dto()