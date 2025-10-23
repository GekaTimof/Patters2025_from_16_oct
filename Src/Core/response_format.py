
# Форматы ответов
class response_formats:

    @staticmethod
    def csv() -> str:
        return "csv"
    
    @staticmethod
    def json() -> str:
        return "json"

    @staticmethod
    def md() -> str:
        return "md"

    @staticmethod
    def xml() -> str:
        return "xml"

    @staticmethod
    # список всех форматов
    def all_formats():
        func = response_formats.__dict__.keys()
        # получаем список ключей - методов без __ и не all_formats
        formats = list(filter(lambda x: "__" not in x and x != "all_formats", func))
        return formats
