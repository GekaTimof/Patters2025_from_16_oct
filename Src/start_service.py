from datetime import datetime
from Src.Core.abstract_dto import abstract_dto
from Src.Core.common import common
from Src.Dtos.storage_dto import storage_dto
from Src.Dtos.transaction_dto import transaction_dto
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
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
from Src.Logics.factory_convert import convert_factory
from Src.Core.abstract_model import abstact_model
from Src.Logics.osv_calculator import osv_calculator
from Src.Dtos.osv_item_dto import osv_item_dto


class start_service:
    # Репозиторий
    __repo: reposity = reposity()

    # Массив пар для загрузки шаблонных данных в __convert_generic
    __generic_convert_pairs = [
        (reposity.ranges_key(), range_dto, range_model),
        (reposity.groups_key(), group_dto, group_model),
        (reposity.nomenclatures_key(), nomenclature_dto, nomenclature_model),
        (reposity.storages_key(), storage_dto, storage_model),
        (reposity.transactions_key(), transaction_dto, transaction_model)
    ]

    # Наименование файла для загрузки настроек (полный путь)
    __load_file_name: str = "settings.json"
    # Наименование файла для сохранения настроек (полный путь)
    __save_file_name: str = "settings_my.json"

    def __init__(self):
        self.__repo.initialize()

    # Single-tone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    # Возврашщаем данные репозитория
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
        settings_json = self.__create_json_settings()
        return settings_json


    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__load_file_name == "":
            raise operation_exception("Не найден файл настроек!")
        # try:
        with open(self.__load_file_name, 'r') as file_instance:
            settings = json.load(file_instance)

            # Получаем данные о компании
            settings_json= settings["settings"]
            for setting_key in reposity.setting_keys():
                if setting_key in settings_json.keys():
                    setting = settings_json[setting_key]
                    self.repository.data[setting_key] = setting

            # Пролучаем repository - данные о компании
            repository_json = settings["repository"]

            # Загружаем общие данные (через шаблонную конвертацию)
            for (key, dto, model) in self.__generic_convert_pairs:
                self.__convert_generic(data=repository_json,
                                       key=key,
                                       dto_class=dto,
                                       model_class=model)

            # Загружаем данные по сложным шаблонам
            self.__convert_receipts(repository_json)

            return True

    # Сохранить элемент в репозитории
    def __save_item(self, key: str, dto, item):
        validator.validate(key, str)
        item.id = dto.id
        self.repository.cache.setdefault(dto.id, item)
        self.repository.add_item(key, item)

    # общий метод конвертации
    def __convert_generic(self, data: dict, key: str, dto_class: abstract_dto, model_class: abstact_model) -> bool:
        validator.validate(data, dict)
        items = data[key] if key in data else []
        if len(items) == 0:
            return False

        for item in items:
            dto = dto_class().create(item)
            model_item = model_class.from_dto(dto, self.repository.cache)
            self.__save_item(key, dto, model_item)
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
                item = receipt_item_model.from_dto(dto, self.repository.cache)
                # Созраняем ингридиент в репозиторий
                self.__save_item(reposity.receipt_items_key(), dto, item)
                receipt_full.receipt_items.append(item)

            # Загрузим шаги приготовления
            steps = receipt['steps'] if 'steps' in receipt else []
            for step in steps:
                if step.strip() != "":
                    receipt_full.steps.append(step)

            # Сохраняем рецепт в репозиторий
            self.repository.add_item(reposity.receipts_key(), receipt_full)
        return True


    def add_item_to_repository(self, key: str, item: abstact_model):
        validator.validate(key, str)
        validator.validate(item, abstact_model)

        if key in self.repository.keys():
            self.repository.add_item(key, item)
        else:
            raise argument_exception(f"в репозитории нет ключа {key}")


    # Метод конвертирующий и возвращающий данные из репозитория в формате json
    def __create_json_settings(self) -> str:
        factory = convert_factory()
        result_json = {}

        # Загружаем данные о настроек
        settings_data = {}
        for setting_key in self.repository.setting_keys():
            setting = self.repository.data[setting_key]
            settings_data[setting_key] = setting
        result_json["settings"] = settings_data

        # Загружаем данные из репозитория (без настроек)
        non_settings_data = self.repository.data.copy()
        setting_keys = reposity.setting_keys()
        for setting_key in setting_keys:
            non_settings_data.pop(setting_key, None)

        result_json["repository"] = factory.create_dict_from_dto(non_settings_data)
        return json.dumps(result_json, ensure_ascii=False, indent=2)


    # Расчёт результата транзакций за период и сохранение в кэш
    def calculate_block_period(self) -> bool:
        period = self.repository.data[self.repository.block_period_setting_key()]
        storages = self.repository.data[reposity.storages_key()]
        calculator = osv_calculator(self.repository)

        # Для каждого склада считаем остатки по каждой номенклатуре
        period_osv_dict = {}
        for storage in storages:
            storage_id = storage.id
            period_osv = calculator.calculate_osv(
                storage_id=storage_id,
                start_date="1990-01-01",
                end_date=period
            )
            period_osv_dict[storage_id] = period_osv

        print("period_osv_dict", period_osv_dict)
        self.repository.add_cache_item(reposity.cache_period_osv_key(), period_osv_dict)
        return True


    # Смена периода блокировки и перерасчёт результата транзакций
    def change_block_period(self, new_period: str):
        # Проверяем, что конвертация в дату не вызывает ошибки
        common.convert_to_date(new_period)

        self.repository.data[reposity.block_period_setting_key()] = new_period
        self.calculate_block_period()


    # метод сохранения сервиса в файл
    def save_settings_to_file(self):
        settings_json = self.settings()

        # Открываем файл для записи в текстовом режиме с нужной кодировкой
        with open(self.__save_file_name, "w", encoding="utf-8") as f:
            f.write(settings_json)


    # Основной метод для загрузки данных сервиса из файла
    def start(self):
        # Загрузка данных
        result = self.load()
        if result == False:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")

        # Расчёт результата транзакций за период
        if not self.calculate_block_period():
            raise operation_exception("Невозможно расчитать транзакции до периода блокировки!")


    # Основной метод для отключения сервера и сохранения данных из репозитория
    def stop(self):
        self.save_settings_to_file()
