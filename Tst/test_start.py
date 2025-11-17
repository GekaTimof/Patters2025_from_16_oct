import os
import unittest
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_format import response_formats
from Src.start_service import start_service


class TestDataFileGeneration(unittest.TestCase):

    def setUp(self):
        self.output_dir = "Responses"
        os.makedirs(self.output_dir, exist_ok=True)
        self.factory = factory_entities()
        self.service = start_service()
        self.service.load_file_name = "settings_my.json"
        self.service.start()

    def save_response_to_file(self, filename, content):
        with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)

    # Универсальный метод для получения данных по ключу из репозитория
    def get_data_by_key(self, key):
        data_list = self.service.repo_data.get(key, [])
        return data_list[0] if data_list else None

    def generate_and_save(self, model_name, data_func):
        data = [data_func()]
        if not data[0]:
            print(f"No data found for model '{model_name}', skipping...")
            return

        for format in [response_formats.csv(), response_formats.json(), response_formats.md(), response_formats.xml()]:
            content = self.factory.create_default(format, data)
            extension = format
            file_name = f"{model_name}.{extension}"
            self.save_response_to_file(file_name, content)
            print(f"Saved {file_name}")

    def test_generate_all_files(self):
        # Ключи в репозитории соответствуют данным моделям
        repo_keys = self.service.repository.keys()

        # Словарь из ключа к функции получения данных (через get_data_by_key)
        model_creators = {
            key: lambda k=key: self.get_data_by_key(k) for key in repo_keys
        }

        for model_name, data_func in model_creators.items():
            self.generate_and_save(model_name, data_func)


if __name__ == "__main__":
    unittest.main()