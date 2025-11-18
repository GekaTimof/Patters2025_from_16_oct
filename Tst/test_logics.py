import unittest
from Src.Core.common import common
from Src.Logics.response_csv import response_csv
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.Models.group_model import group_model
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_format import response_formats
from Src.Core.validator import validator
from Src.Core.abstract_response import abstract_response

# Тесты для проверки логики 
class test_logics(unittest.TestCase):

    # Проверим формирование CSV
    def test_notNone_response_csv_buld(self):
        # Подготовка
        response = response_csv()
        data = []
        entity = group_model.create( "test" )
        data.append( entity )

        # Дейстие
        result = response.create( "csv", data)

        # Проверка
        assert result is not None


    # Проверим формирование JSON
    def test_notNone_response_json_build(self):
        # Подготовка
        response = response_json()
        data = []
        entity = group_model.create( "test" )
        data.append( entity )

        # Дейстие
        result = response.create( "json", data)

        # Проверка
        assert result is not None


    # Проверим формирование Markdown
    def test_notNone_response_md_build(self):
        # Подготовка
        response = response_md()
        data = []
        entity = group_model.create( "test" )
        data.append( entity )

        # Дейстие
        result = response.create( "md", data)

        # Проверка
        assert result is not None


    # Проверим формирование XML
    def test_notNone_response_xml_build(self):
        # Подготовка
        response = response_xml()
        data = []
        entity = group_model.create( "test" )
        data.append( entity )

        # Дейстие
        result = response.create( "xml", data)

        # Проверка
        assert result is not None


    # Проверка, что фабрика создаёт объект response
    def test_notNone_factory_create(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = group_model.create( "test" )
        data.append( entity )

        # Действие
        logic = factory.create(response_formats.csv())

        # Проверка
        assert logic is not None
        instance = logic
        validator.validate( instance,  abstract_response)
        text = instance.create(  response_formats.csv(), data )
        assert len(text) > 0


    # Метод для проверки полей
    def check_fields_in_output(self, output, data, delimiter=None):
        fields = common.get_fields(data)
        # Проверяем, что все имена полей есть в выводе (заголовки)
        for field in fields:
            self.assertIn(field, output)

        # Проверяем, что значения всех полей первого объекта есть в выводе
        for field in fields:
            value = str(getattr(data, field, ""))
            if delimiter:
                # Для csv и md проверяем с учетом разделителей
                self.assertIn(value, output)
            else:
                self.assertIn(value, output)


    # Проверяет, что CSV вывод содержит все поля и соответствующие значения
    def test_csv_output_contains_all_fields_and_values(self):
        response = response_csv()
        data = [group_model.create("test")]
        output = response.create("csv", data)
        print("CSV")
        print(output)
        self.check_fields_in_output(output, data, delimiter=";")


    # Проверяет, что JSON вывод содержит все поля и соответствующие значения
    def test_json_output_contains_all_fields_and_values(self):
        response = response_json()
        data = [group_model.create("test")]
        output = response.create("json", data)
        print("JSON")
        print(output)
        self.check_fields_in_output(output, data)


    # Проверяет, что Markdown вывод содержит все поля и соответствующие значения
    def test_markdown_output_contains_all_fields_and_values(self):
        response = response_md()
        data = [group_model.create("test")]
        output = response.create("md", data)
        print("MD")
        print(output)
        self.check_fields_in_output(output, data)


    # Проверяет, что XML вывод содержит все поля и соответствующие значения
    def test_xml_output_contains_all_fields_and_values(self):
        response = response_xml()
        data = [group_model.create("test")]
        output = response.create("xml", data)
        print("XML")
        print(output)
        self.check_fields_in_output(output, data)


if __name__ == '__main__':
    unittest.main()   
