import unittest
from Src.start_service import start_service
from Src.repository import reposity

# Набор тестов для проверки работы статового сервиса
class test_start(unittest.TestCase):

    # Проверить создание start_service и заполнение данными
    def test_notThow_start_service_load(self):
        # Подготовка
        start = start_service()

        # Действие
        start.start()

        # Проверка
        assert len(start.data[ reposity.ranges_key()]) > 0

    # Проверить уникальность элемиентов
    def test_checkUnique_start_service_load(self):
        # Подготовка
        start = start_service()

        # Действие
        start.start()

        # Проверка
        gramm =  list(filter(lambda x: x.name == "Грамм", start.data[ reposity.ranges_key()]))
        kg =  list(filter(lambda x: x.name == "Киллограмм", start.data[ reposity.ranges_key()]))
        assert gramm[0].id == kg[0].base.id


    # Проверить метод keys класса reposity
    def test_any_reposity_keys(self):
        # Подготовка

        # Действие
        result = reposity.keys()
        
        # Проверка
        assert len(result) > 0

    # Проверить метод initalize класса reposity 
    def test_notThrow_reposity_initialize(self):   
        # Подготовка
        repo = reposity()

        # Действие
        repo.initalize() 



        