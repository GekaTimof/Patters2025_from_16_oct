from Src.Core.common import common

"""
Репозиторий данных
"""
class reposity:
    __data = {}
    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    # все данные компании хранящиеся в репозиории в виде массивов моделей
    @property
    def data(self):
        return self.__data

    # кэш хранить id и соответствующий ему элемент
    @property
    def cache(self):
        return self.__cache

    # добавление элемента в data, с добавлением этого же элемнта в cache
    def add_item(self, key: str, item):
        if key not in self.__data:
            self.__data[key] = []
        self.__data[key].append(item)

        # Добавляем в кэш по id
        item_id = getattr(item, "id", None)
        if item_id is not None and item_id not in self.__cache:
            self.__cache[item_id] = item


    # добавление элемента в cache
    def add_cache_item(self, key: str, item):
        self.__cache[key] = item

    """
    Ключ (настройки) для периода блокировки блокировки
    """
    @staticmethod
    def block_period_setting_key():
        return "block_period"



    """
    Ключ (настройки) для указания был ли произведён запуск
    """
    @staticmethod
    def is_firs_start_setting_key():
        return "is_firs_start"

    """
    Ключ (настройки) для хранения
    """
    @staticmethod
    def cache_period_osv_key():
        return "period_osv"


    """
    Ключ для единц измерений
    """
    @staticmethod
    def ranges_key():
        return "ranges"


    """
    Ключ для категорий
    """
    @staticmethod
    def groups_key():
        return "groups"


    """
    Ключ для номенклатуры
    """
    @staticmethod
    def nomenclatures_key():
        return "nomenclatures"


    """
    Ключ для рецептов
    """
    @staticmethod
    def receipts_key():
        return "receipts"


    """
    Ключ для компонент рецептов
    """
    @staticmethod
    def receipt_items_key():
        return "receipt_items"


    """
    Ключ для складов
    """
    @staticmethod
    def storages_key():
        return "storages"


    """
    Ключ для тразакций
    """
    @staticmethod
    def transactions_key():
        return "transactions"


    """
    Получить список всех ключей
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(reposity) if
            callable(getattr(reposity, method)) and
                   not method.startswith("cache_") and
                   not method.endswith('_setting_key') and
                   method.endswith('_key')]
        for method in methods:
            key = getattr(reposity, method)()
            result.append(key)
        return result

    """
    Получить список всех ключей нестроек сервиса
    """
    @staticmethod
    def setting_keys() -> list:
        result = []
        methods = [method for method in dir(reposity) if
            callable(getattr(reposity, method)) and method.endswith('_setting_key')]
        for method in methods:
            key = getattr(reposity, method)()
            result.append(key)
        return result


    # Инициализация
    def initialize(self):
        keys = reposity.keys()
        for key in keys:
            self.__data[key] = []

        keys = reposity.setting_keys()
        for key in keys:
            self.__data[key] = None


    # Получение элемента по его id
    def get_by_id(self, _id: str):
        for key in self.keys():
            for elem in self.__data[key]:
                if "id" == common.get_fields(elem) and elem.id == _id:
                    return elem
        return None