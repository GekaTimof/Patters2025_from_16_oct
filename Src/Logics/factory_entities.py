from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_csv
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.Logics.response_json import response_json
from Src.Core.response_format import response_formats
from Src.Core.validator import operation_exception
from Src.Core.validator import validator

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

    @property
    def format(self) -> str:
        return self.__format

    @format.setter
    def format(self, value: str):
        validator.validate(value, str)
        self.__format = value


    # Получить нужный тип
    def create(self, format:str) -> abstract_response:
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")
        
        return self.__match[ format ]


    # создать response заданного типа
    def create_default(self, data: list):
        # Создаем нужный класс в зависимости от сохраненного формата
        response_cls = self.create(self.format)
        response_instance = response_cls()
        return response_instance.create(self.format, data)