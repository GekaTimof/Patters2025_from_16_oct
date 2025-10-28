
"""
Репозиторий данных
"""
class reposity:
    __data = {}

    # все данные компании хранящиеся в репозиории в виде массивов моделей
    @property
    def data(self):
        return self.__data
    
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
    Получить список всех ключей
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(reposity) if
                    callable(getattr(reposity, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(reposity, method)()
            result.append(key)

        return result

    
    """
    Инициализация
    """
    def initalize(self):
        keys = reposity.keys()
        for key in keys:
            self.__data[ key ] = []
    
    
