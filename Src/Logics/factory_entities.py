from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_csv
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.Logics.response_json import response_json
from Src.Core.response_format import response_formats

class factory_entities:
    # текущий формат
    __format: str
    # список форматов
    __match = {
        # csv
        response_formats.csv():  response_csv,
        # json
        response_formats.json(): response_json,
        # md
        response_formats.md(): response_md,
        # xml
        response_formats.xml(): response_xml
    }

    # Возвращаем нужный инстанс класса
    def create(self, format: str) -> abstract_response:
        cls = self.__match.get(format)
        if cls is None:
            raise ValueError(f"Format {format} is not supported")
        return cls()

    # Вызываем create у подходящего инстанса
    def create_default(self, format: str, data: list):
        response_instance = self.create(format)
        return response_instance.create(format, data)
