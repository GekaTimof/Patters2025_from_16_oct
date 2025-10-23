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
from Src.Models.nomenclature_model import nomenclature_model
from Src.start_service import start_service

service = start_service()
service.start()

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

    # Функция получения разных моделей
    def get_group(self):
        groups = service.get_groups()
        # Возьмем первый или нужный элемент, если нужно именно один
        return groups[0] if groups else None

    def get_range(self):
        ranges = service.get_ranges()
        return ranges[0] if ranges else None

    def get_receipt(self):
        receipts = service.get_receipts()
        return receipts[0] if receipts else None

    def get_nomenclature(self):
        nomenclatures = service.get_nomenclatures()
        return nomenclatures[0] if nomenclatures else None


    # Создаём ответы и сохраняем их в файлы
    def generate_and_save(self, model_name, create_func):
        data = [create_func()]

        for format in [response_formats.csv(), response_formats.json(), response_formats.md(), response_formats.xml()]:
            content = self.factory.create_default(format, data)
            extension = format
            file_name = f"{model_name}.{extension}"
            self.save_response_to_file(file_name, content)
            print(f"Saved {file_name}")


    # Проверка создания фалов каждой модели
    def test_generate_all_files(self):
        model_creators = {
            "groups": self.get_group,
            "ranges": self.get_range,
            "receipts": self.get_receipt,
            "nomenclatures": self.get_nomenclature,
        }

        for model_name, create_func in model_creators.items():
            self.generate_and_save(model_name, create_func)


if __name__ == "__main__":
    unittest.main()
