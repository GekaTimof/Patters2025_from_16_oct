from Src.Models.settings_model import settings_model
from Src.Core.validator import argument_exception
from Src.Core.validator import operation_exception
from Src.Core.validator import validator
from Src.Models.company_model import company_model
from Src.Core.common import common
from Src.Core.response_format import response_formats
import xmltodict
import os
import json

####################################################
# Менеджер настроек. 
# Предназначен для управления настройками и хранения параметров приложения
class settings_manager:
    # Какому расширеню какой формат соответствует
    __match_formats = {
        "xml": response_formats.xml(),
        "json": response_formats.json(),
    }

    # Наименование файла (полный путь)
    __full_file_name: str = ""

    # Настройки
    __settings: settings_model = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.set_default()

    # Текущие настройки
    @property
    def settings(self) -> settings_model:
        return self.__settings

    # Текущий файл
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # Загрузить настройки из файла (.json .xml)
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        # Определяем расширение файла
        _, ext = os.path.splitext(self.__full_file_name)
        ext = ext.lower().replace('.', '')

        # Проверяем, что формат поддерживается
        if ext not in self.__match_formats.keys():
            raise argument_exception(f"Формат файла '.{ext}' не поддерживается!")

        try:
            # Читаем файл
            with open(self.__full_file_name, 'r', encoding='utf-8') as file_instance:
                if ext == "json":
                    settings = json.load(file_instance)
                elif ext == "xml":
                    # Преобразуем XML → dict
                    xml_dict = xmltodict.parse(file_instance.read())
                    # Конвертируем OrderedDict → обычный dict
                    settings = json.loads(json.dumps(xml_dict))

                # достаем company из xml {'settings': {'company': {...}, 'default_receipt': {...}}}
                if "settings" in settings:
                    settings = settings["settings"]

                if "company" in settings:
                    data = settings["company"]
                    return self.convert(data)

            return False
        except:
            return False

    # Обработать полученный словарь
    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        fields = common.get_fields(self.__settings.company)
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                value = data[key]
                # Если значение - строка числа, конвертируем
                if isinstance(value, str) and value.isdigit():
                    value = int(value)
                setattr(self.__settings.company, key, value)
        except:
            return False

        return True

    # Параметры настроек по умолчанию
    def set_default(self):
        company = company_model()
        company.name = "Рога и копыта"
        company.inn = -1

        self.__settings = settings_model()
        self.__settings.company = company