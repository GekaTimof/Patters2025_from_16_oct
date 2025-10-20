import os
import unittest
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_format import response_formats
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Models.storage_model import storage_model
from Src.Models.company_model import company_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Models.receipt_model import receipt_model
from Src.Models.settings_model import settings_model
from Src.Models.nomenclature_model import nomenclature_model

class TestDataFileGeneration(unittest.TestCase):
    # Создание папки для сохранения, создания фабрики
    def setUp(self):
        self.output_dir = "Responses"
        os.makedirs(self.output_dir, exist_ok=True)
        self.factory = factory_entities()

    # Сохранение в файл
    def save_response_to_file(self, filename, content):
        with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)

    # Функция создания разных моделей
    def create_group(self):
        return group_model.create("test")

    def create_range(self):
        base_range = range_model.create("test_base_range", 5)
        return range_model.create("test_range", 10, base_range)

    def create_storage(self):
        return storage_model.create("test_storage")

    def create_company(self):
        return company_model.create("test_company")

    def create_receipt_item(self):
        # Нужно соответствие параметров метода create
        return receipt_item_model.create("test_item", 10, 5)

    def create_receipt(self):
        return receipt_model.create("test_receipt", "some time", 10)

    def create_nomenclature(self):
        test_range = range_model.create("test_base_range", 5)
        test_group = group_model.create("test")
        return nomenclature_model.create("test_nomenclature", test_group, test_range)


    # Создаём ответы и сохраняем их в файлы
    def generate_and_save(self, model_name, create_func):
        data = [create_func()]

        for fmt in [response_formats.csv(), response_formats.json(), response_formats.md(), response_formats.xml()]:
            self.factory.format = fmt
            content = self.factory.create_default(data)
            ext = fmt
            file_name = f"{model_name}.{ext}"
            self.save_response_to_file(file_name, content)
            print(f"Saved {file_name}")


    # Проверка создания фалов каждой модели
    def test_generate_all_files(self):
        model_creators = {
            "groups": self.create_group,
            "ranges": self.create_range,
            "storages": self.create_storage,
            "companies": self.create_company,
            "receipt_items": self.create_receipt_item,
            "receipts": self.create_receipt,
            "nomenclatures": self.create_nomenclature,
        }

        for model_name, create_func in model_creators.items():
            self.generate_and_save(model_name, create_func)


if __name__ == "__main__":
    unittest.main()
