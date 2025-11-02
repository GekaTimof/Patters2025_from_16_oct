from Src.repository import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator, argument_exception, operation_exception
import os
import json
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.group_dto import group_dto
from Src.Dtos.receipt_item_dto import receipt_item_dto
from Src.Dtos.receipt_dto import receipt_dto
from Src.Logics.convert_factory import convert_factory


class start_service:
    # Репозиторий
    __repo: reposity = reposity()

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    # Наименование файла для загрузки настроек (полный путь)
    __load_file_name: str = "settings.json"
    # Наименование файла для сохранения настроек (полный путь)
    __save_file_name: str = "settings_my.json"

    def __init__(self):
        self.__repo.initalize()

    # Single-tone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    # получить данные репозитория
    @property
    def repo_data(self):
        return self.__repo.data

    # получить рапозиторий целиком
    @property
    def repository(self):
        return self.__repo

    # Текущий файл зпугрузки настроек
    @property
    def load_file_name(self) -> str:
        return self.__load_file_name


    # Полный путь к файлу для загрузки настроек
    @load_file_name.setter
    def load_file_name(self, value: str):
        validator.validate(value, str)
        file_name = os.path.abspath(value)
        if os.path.exists(file_name):
            self.__load_file_name = file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {file_name}')


    # Текущий файл сохранения настроек
    @property
    def save_file_name(self) -> str:
        return self.__save_file_name

    # Полный путь к файлу для сохранения настроек
    @save_file_name.setter
    def save_file_name(self, value: str):
        validator.validate(value, str)
        save_file_name = os.path.abspath(value)

        if not os.path.isfile(save_file_name):
            raise argument_exception(f'Путь не является файлом: {save_file_name}')

        self.__save_file_name = save_file_name.strip()


    # Текущая конфигурация
    def settings(self) -> str:
        factory = convert_factory()
        settings_json = self.create_json_settings(self)
        return settings_json

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__load_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        # try:
        with open(self.__load_file_name, 'r') as file_instance:
            settings = json.load(file_instance)

            # получаем данные о компании
            # ***

            # пролучаем repository - данные о компании
            repository_json = settings["repository"]

            # получаем общие данные
            self.__convert_ranges(repository_json)
            self.__convert_groups(repository_json)
            self.__convert_nomenclatures(repository_json)
            self.__convert_receipts(repository_json)

            return True

            # # получаем рецепты
            # if reposity.receipts_key() in repository.keys():
            #
            #     # получаем список рецептов
            #     receipts = repository[reposity.receipts_key()]
            #     # конвертируем все рецепты
            #     for receipt in receipts:
            #         if not self.__convert_receipt(receipt):
            #             return False
            #     return True
            # else:
            #     return False
        # except Exception as e:
        #     error_message = str(e)
        #     print(error_message)
        #     return False

    # Сохранить элемент в репозитории
    def __save_item(self, key: str, dto, item):
        validator.validate(key, str)
        item.id = dto.id
        self.__cache.setdefault(dto.id, item)
        self.__repo.data[key].append(item)

    # Загрузить единицы измерений
    def __convert_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data[reposity.ranges_key()] if reposity.ranges_key() in data else []
        if len(ranges) == 0:
            return False

        for range in ranges:
            dto = range_dto().create(range)
            item = range_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.ranges_key(), dto, item)

        return True

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        groups = data[reposity.groups_key()] if reposity.groups_key() in data else []
        if len(groups) == 0:
            return False

        for group in groups:
            dto = group_dto().create(group)
            item = group_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.groups_key(), dto, item)

        return True

    # Загрузить номенклатуру
    def __convert_nomenclatures(self, data: dict) -> bool:
        validator.validate(data, dict)
        nomenclatures = data[reposity.nomenclatures_key()] if reposity.nomenclatures_key() in data else []
        if len(nomenclatures) == 0:
            return False

        for nomenclature in nomenclatures:
            dto = nomenclature_dto().create(nomenclature)
            item = nomenclature_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.nomenclatures_key(), dto, item)

        return True

    # Обработать полученный словарь
    def __convert_receipts(self, data: dict) -> bool:
        validator.validate(data, dict)
        receipts = data[reposity.receipts_key()] if reposity.receipts_key() in data else []
        if len(receipts) == 0:
            return False

        for receipt in receipts:
            # Получаем информацию о рецепте
            id = receipt['id'] if 'id' in receipt else None
            name = receipt['name'] if 'name' in receipt else "НЕ ИЗВЕСТНО"
            portions = int(receipt['portions']) if 'portions' in receipt else 0
            cooking_time = receipt['cooking_time'] if 'cooking_time' in receipt else ""

            # Создаём рецепт
            receipt_full = receipt_model().create(id, name, portions, cooking_time)

            # Загружаем ингридиенты
            receipt_items = receipt[reposity.receipt_items_key()] if reposity.receipt_items_key() in receipt else []
            if len(receipt_items) == 0:
                return False

            for receipt_item in receipt_items:
                dto = receipt_item_dto().create(receipt_item)
                item = receipt_item_model.from_dto(dto, self.__cache)
                # Созраняем ингридиент в репозиторий
                self.__save_item(reposity.receipt_items_key(), dto, item)
                receipt_full.receipt_items.append(item)

            # Загрузим шаги приготовления
            steps = receipt['steps'] if 'steps' in receipt else []
            for step in steps:
                if step.strip() != "":
                    receipt_full.steps.append(step)

            # Сохраняем рецепт в репозиторий
            self.__repo.data[reposity.receipts_key()].append(receipt_full)
        return True


    # Метод конвертирующий и возвращающий данные из репозитория в формате json
    def create_json_settings(self, service) -> str:
        factory = convert_factory()

        result_json = {}
        result_json["is_firs_start"] = False
        result_json["company"] = {}
        result_json["repository"] = factory.create_dict_from_dto(service.repository.data)
        return json.dumps(result_json, ensure_ascii=False, indent=2)


    # Возврашщаем данные из репзитория
    @property
    def data(self):
        return self.__repo.data


    # метод сохранения сервиса в файл
    def save_settings_to_file(self):
        settings_json = self.settings()

        # Открываем файл для записи в текстовом режиме с нужной кодировкой
        with open(self.__save_file_name, "w", encoding="utf-8") as f:
            f.write(settings_json)


    # Основной метод для загрузки данных сервиса из файла
    def start(self):
        result = self.load()
        if result == False:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")


    # Основной метод для отключения сервера и сохранения данных из репозитория
    def stop(self):
        self.save_settings_to_file()
