import unittest
from Src.start_service import start_service
from Src.Logics.factory_convert import convert_factory
import json

service = start_service()
service.start()

class TestCreateReceiptDict(unittest.TestCase):
    def test_create_dict_repository(self):
        repository = service.repository

        # создание фабрики
        factory = convert_factory()
        receipt_dict = factory.create_dict_from_dto(repository.data)

        # Проверяем, что ключи совпадают с ключами репозитория
        self.assertSetEqual(set(receipt_dict.keys()), set(repository.keys()))

        # Проверяем, что для каждого ключа значение - список словарей (json-serializable)
        for key, items in receipt_dict.items():
            # Проверяем это множественный илои еденичный параметр
            self.assertIsInstance(items, list)
            for item in items:
                self.assertIsInstance(item, dict)


if __name__ == "__main__":
    unittest.main()