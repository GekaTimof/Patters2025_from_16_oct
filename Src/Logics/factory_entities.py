from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_csv
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.Logics.response_json import response_json
from Src.Core.response_format import response_formats
from Src.Core.validator import operation_exception

class factory_entities:
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


    # Получить нужный тип
    def create(self, format:str) -> abstract_response:
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")
        
        return self.__match[ format ]


    # создать response заданного типа
    def create_default(self, format:str, data: list):
        # Создаем нужный класс в зависимости от сохраненного формата
        response_cls = self.create(format)
        response_instance = response_cls()
        return response_instance.create(format, data)