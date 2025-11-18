from Src.Core.common import common
from Src.Core.validator import validator
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.sorting_dto import sorting_dto
from Src.Core.validator import argument_exception
from Src.Logics.factory_transform import factory_transform

# Прототип
class prototype:
    __data = []
    __transforms = {}

    def __init__(self, data:list):
        validator.validate(data, list)
        self.__data = data
        # Задаём все существующийе вид преобразования
        self.__transforms = {
            "sort": prototype.sorting,
            "filter": prototype.filter
        }


    @property
    def data(self) -> list:
        return self.__data

    @property
    def transforms(self) -> dict:
        return self.__transforms

    @property
    def transforms_keys(self) -> list:
        return list(self.__transforms.keys())

    def clone(self, data: list = None) -> "prototype":
        inner_data = None
        if data is None:
            inner_data = self.__data
        else:
            inner_data = data

        instance = prototype(inner_data)
        return instance


    # Универсальный фильтр для прототипов
    @staticmethod
    def filter(data_prototype: "prototype", filter: filter_dto) -> "prototype":
        data =  data_prototype.data
        if not data:
            return prototype([])

        filtered_data = []
        for item in data:
            if hasattr(item, filter.field_name):
                attribute_value = getattr(item, filter.field_name)

                comp_attribute_value = attribute_value
                comp_filter_value = filter.value

                # Выбранный тип фильтрации
                filter_type = filter.filter_type

                # Полное совпадение
                if filter_type == filter_dto.equal_filter():
                    if comp_attribute_value == comp_filter_value:
                        filtered_data.append(item)
                # Обратная операция полного совпадения
                elif filter_type == filter_dto.not_equal_filter():
                    if comp_attribute_value != comp_filter_value:
                        filtered_data.append(item)
                # Вхождение строки
                elif filter_type == filter_dto.like_filter():
                    if comp_filter_value in comp_attribute_value:
                        filtered_data.append(item)
                # Обратная операция вхождения строки
                elif filter_type == filter_dto.not_like_filter():
                    if comp_filter_value not in comp_attribute_value:
                        filtered_data.append(item)
                # >
                elif filter_type == filter_dto.greater_filter():
                    if comp_attribute_value > comp_filter_value:
                        filtered_data.append(item)
                # >=
                elif filter_type == filter_dto.greater_or_equal_filter():
                    if comp_attribute_value >= comp_filter_value:
                        filtered_data.append(item)
                # <
                elif filter_type == filter_dto.less_filter():
                    if comp_attribute_value < comp_filter_value:
                        filtered_data.append(item)
                # <=
                elif filter_type == filter_dto.less_or_equal_filter():
                    if comp_attribute_value <= comp_filter_value:
                        filtered_data.append(item)
                else:
                    raise argument_exception(f"Unknown type of filter {filter_type}")
        return prototype(filtered_data)


    # Универсальная сортировка для прототипов
    @staticmethod
    def sorting(data_prototype: "prototype", sort: sorting_dto) -> "prototype":
        data =  data_prototype.data

        # Проверяем, что у элементов есть нужное поле
        if not all(hasattr(item, sort.field_name) for item in data):
            raise argument_exception(f"Not all objects in data have field {sort.field_name}")

        # Определяем ключ для сортировки (получаем значение нужного поля)
        def sort_key(item):
            attribute = getattr(item, sort.field_name)
            return attribute

        sort_type = sort.sort_type
        reverse = False
        if sort_type == sorting_dto.descending():
            reverse = True
        elif sort_type == sorting_dto.ascending():
            reverse = False
        else:
            raise argument_exception(f"Unknown sorting type {sort_type}")

        sorted_data = sorted(data, key=sort_key, reverse=reverse)

        return prototype(sorted_data)

    # Метод для множественной трансформации
    # Принемает словарь с трансформациями вида:
    """
    {
        "filter": [
            {
                "field_name": "name",
                "value": "а",
                "filter_type": "LIKE"
            },
            {
                "field_name": "name",
                "value": "х",
                "filter_type": "NOT_LIKE"
            }
        ],
        "sort": [
            {
                "field_name": "name",
                "sort_type": "ASCENDING"
            }
        ]
    }
    """

    @staticmethod
    def multi_transforming(data_prototype: "prototype", transforming: dict) -> "prototype":
        transformed_prototype = data_prototype
        # Применяем разные операции трансформации данных
        for key in data_prototype.transforms_keys:
            if key in transforming:
                transform_operation = data_prototype.__transforms[key]
                transform_array = transforming[key]
                for transform in transform_array:
                    # Получаем подходящий dto для преобразования, заполняем его
                    factory = factory_transform()
                    transform_dto = factory.create_and_fill(transform)
                    # Проводим трансформацию
                    transformed_prototype = transform_operation(transformed_prototype, transform_dto)

        return transformed_prototype
