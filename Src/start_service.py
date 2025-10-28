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
from Src.Dtos.category_dto import category_dto
from Src.Dtos.receipt_item_dto import receipt_item_dto
from Src.Logics.convert_factory import convert_factory

class start_service:
    # Репозиторий
    __repo: reposity = reposity()

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    # Наименование файла (полный путь)
    __full_file_name:str = ""

    def __init__(self):
        self.__repo.initalize()

    # Singletone
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

    # Текущий файл
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)        
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        # try:
        with open( self.__full_file_name, 'r') as file_instance:
            settings = json.load(file_instance)

            # получаем данные о компании
            # ***

            # получаем рецепты
            if reposity.receipts_key() in settings.keys():
                # получаем список рецептов
                receipts = settings[reposity.receipts_key()]
                # конвертируем все рецепты
                for receipt in receipts:
                    if not self.convert(receipt):
                        return False
            return True
        # except Exception as e:
        #     error_message = str(e)
        #     print(error_message)
        #     return False

    # Сохранить элемент в репозитории
    def __save_item(self, key:str, dto, item):
        validator.validate(key, str)
        item.id = dto.id
        self.__cache.setdefault(dto.id, item)
        self.__repo.data[ key ].append(item)

    # Загрузить единицы измерений   
    def __convert_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data[reposity.ranges_key()] if reposity.ranges_key() in data else []
        if len(ranges) == 0:
            return False
         
        for range in ranges:
            dto = range_dto().create(range)
            item = range_model.from_dto(dto, self.__cache)
            self.__save_item( reposity.ranges_key(), dto, item )

        return True

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        categories =  data[reposity.groups_key()] if reposity.groups_key() in data else []
        if len(categories) == 0:
            return False

        for category in categories:
            dto = category_dto().create(category)    
            item = group_model.from_dto(dto, self.__cache )
            self.__save_item( reposity.groups_key(), dto, item )

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
            self.__save_item( reposity.nomenclatures_key(), dto, item )

        return True        


    # Обработать полученный словарь    
    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        # 1 Созданим рецепт
        cooking_time = data['cooking_time'] if 'cooking_time' in data else ""
        portions = int(data['portions']) if 'portions' in data else 0
        name = data['name'] if 'name' in data else "НЕ ИЗВЕСТНО"
        # self.__default_receipt = receipt_model.create(name, cooking_time, portions)
        receipt: receipt_model = receipt_model.create(name, cooking_time, portions)

        # Загрузим шаги приготовления
        steps =  data['steps'] if 'steps' in data else []
        for step in steps:
            if step.strip() != "":
                receipt.steps.append( step )

        # Загрузим ингридиенты
        receipt_items = data['receipt_items'] if 'receipt_items' in data else []
        for receipt_item in receipt_items:
            dto = receipt_item_dto().create(receipt_item)
            item = receipt_item_model.from_dto(dto, self.__cache)
            receipt.receipt_items.append(item)

        self.__convert_ranges(data)
        self.__convert_groups(data)
        self.__convert_nomenclatures(data)


        # Собираем рецепт
        receipt_items =  data['receipt_items'] if 'receipt_items' in data else []
        if len(receipt_items) == 0:
            return False

        for receipt_item in receipt_items:
            namnomenclature_id = receipt_item['nomenclature_id'] if 'nomenclature_id' in receipt_item else ""
            range_id = receipt_item['range_id'] if 'range_id' in receipt_item else ""
            value  = receipt_item['value'] if 'value' in receipt_item else ""
            nomenclature = self.__cache[namnomenclature_id] if namnomenclature_id in self.__cache else None
            range = self.__cache[range_id] if range_id in self.__cache else None
            item = receipt_item_model.create(  nomenclature, range, value)
            receipt.receipt_items.append(item)

        # Сохраняем рецепт
        self.__repo.data[ reposity.receipts_key() ].append(receipt)
        return True

    """
    Стартовый набор данных
    """
    @property
    def data(self):
        return self.__repo.data   

    # метод сохранения сервиса в файл
    def save_settings_to_file(self):
        factory = convert_factory()
        settings_json = factory.create_json_settings(self)

        # Открываем файл для записи в текстовом режиме с нужной кодировкой
        with open("settings_my.json", "w", encoding="utf-8") as f:
            f.write(settings_json)


    """
    Основной метод для генерации эталонных данных
    """
    def start(self):
        self.file_name = "settings.json"
        result = self.load()
        if result == False:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")

    """
    Основной метод для отключения сервера и сохранения данных из репозитория
    """
    def stop(self):
        self.save_settings_to_file()


service = start_service()
service.start()
service.stop()