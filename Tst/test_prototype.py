import unittest

from Src.Core.common import common
from Src.start_service import start_service
from Src.Core.prototype import prototype
from Src.repository import reposity
from Src.Core.validator import operation_exception
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.sorting_dto import sorting_dto

class test_prototype(unittest.TestCase):

    def test_any_prototype(self):
        # Запускаем сервис один раз для всех тестов
        service = start_service()
        service.load_file_name = "settings_my.json"
        service.start()

        # Базовый прототип
        start_prototype = prototype(service.repo_data[reposity.transactions_key()])
        nomenclatures = service.repo_data[reposity.nomenclatures_key()]
        if len(nomenclatures) == 0:
            raise operation_exception("nomenclatures is empty")
        first_nomenclature = nomenclatures[-1]
        filter_nomenclature = filter_dto("nomenclature", first_nomenclature, filter_dto.equal_filter())

        # Новый прототип с фильтром
        new_prototype = start_prototype.filter(start_prototype, filter_nomenclature)

        # Проверки
        assert len(start_prototype.data) > 0
        assert len(new_prototype.data) > 0
        assert len(start_prototype.data) >= len(new_prototype.data)


    def test_sorting_prototype(self):
        service = start_service()
        service.load_file_name = "settings_my.json"
        service.start()

        start_prototype = prototype(service.repo_data[reposity.transactions_key()])
        sorting_by_date = sorting_dto("date", None, sorting_dto.ascending())

        sorted_prototype = prototype.sorting(start_prototype, sorting_by_date)

        dates = [item.date for item in sorted_prototype.data]
        assert dates == sorted(dates)


    def test_multy_transforming_prototype(self):
        service = start_service()
        service.load_file_name = "settings_my.json"
        service.start()

        start_prototype = prototype(service.repo_data[reposity.nomenclatures_key()])
        transforming =   {
            "filter" : [
                {
                    "field_name": "name",
                    "value": "а",
                    "filter_type": "LIKE"
                },
                {
                    "field_name": "name",
                    "value": "х",
                    "filter_type": "NOT_LIKE"
                },
            ],
            "sort" : [
                {
                    "field_name": "name",
                    "sort_type": "ASCENDING"
                },
            ]
        }

        transformed_prototype = prototype.multi_transforming(start_prototype, transforming)
        for i, elem in enumerate(transformed_prototype.data):
            print(f"elem - {i}")
            for field in common.get_fields(elem):
                print(field, getattr(elem, field))
            print()

        assert len(transformed_prototype.data) > 0


if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
