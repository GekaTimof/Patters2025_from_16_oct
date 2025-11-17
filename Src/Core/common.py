from Src.Core.entity_model import entity_model
from Src.Core.validator import argument_exception
from datetime import datetime
from Src.Core.validator import convertation_exception


# Набор статических общих методов
class common:
    """
    Получить список наименований всех моделей
    """
    @staticmethod
    def get_models() -> list:
        result = []
        for  inheritor in entity_model.__subclasses__():
            result.append(inheritor.__name__)

        return result


    """
    Получить полный список полей любой модели
        - is_common = True - исключить из списка словари и списки
    """
    @staticmethod
    def get_fields(source, is_common: bool = False) -> list:
        if source is None:
            raise argument_exception("Некорректно переданы аргументы!")

        items = list(filter(lambda x: not x.startswith("_") , dir(source)))
        result = []

        for item in items:
            attribute = getattr(source.__class__, item)
            if isinstance(attribute, property):
                value = getattr(source, item)

                # Флаг. Только простые типы и модели включать
                if is_common == True and (isinstance(value, dict) or isinstance(value, list) ):
                    continue

                result.append(item)
        return result


    """
    Получить полный список полей любой модели
        - is_common = True - исключить из списка словари и списки
    """
    @staticmethod
    def get_setters(source, is_common: bool = False) -> list:
        if source is None:
            raise argument_exception("Некорректно переданы аргументы!")

        # Определяем класс, если передан экземпляр
        cls = source if isinstance(source, type) else source.__class__

        items = list(filter(lambda x: not x.startswith("_"), dir(cls)))
        result = []

        for item in items:
            attribute = getattr(cls, item, None)
            # Проверяем, что это property и у него есть сеттер (fset)
            if isinstance(attribute, property) and attribute.fset is not None:
                value = None
                # Если передан экземпляр, пробуем получить значение свойства
                if not isinstance(source, type):
                    try:
                        value = getattr(source, item)
                    except Exception:
                        value = None

                # Исключаем dict и list если указан флаг is_common
                if is_common and (isinstance(value, dict) or isinstance(value, list)):
                    continue

                result.append(item)

        return result


    """
    Получить полный список наследников класса
    {name: obj}
    """
    @staticmethod
    def get_all_subclasses_dict(cls):
        subclasses = {}
        work = [cls]
        while work:
            parent = work.pop()
            for subclass in parent.__subclasses__():
                if subclass.__name__ not in subclasses:
                    subclasses[subclass.__name__] = subclass
                    work.append(subclass)
        return subclasses

    """
    Проверяем - можнор ли объект преобразовать в dto
    имеет ли он параметр dto_type
    """
    @staticmethod
    def can_convert_to_dto(obj):
        if "dto_type" in common.get_fields(obj):
            return True
        else:
            return False

    """
    Переводим строку в datetime
    если не подходит формат возвращаем None 
    """
    @staticmethod
    def convert_to_date(date_str: str):
        date_str = date_str.strip()
        try:
            # Первая попытка: формат с датой и временем
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                # Вторая попытка: только дата
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                # Ни один формат не подошёл
                raise convertation_exception(f"Не подходящий формат для конвертации в datetime - {date_str}. Попробуйте - '2025-11-02' | '2025-11-02 14:30:45'")