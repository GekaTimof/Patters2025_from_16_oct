import unittest
from Src.start_service import start_service
from Src.repository import reposity

service = start_service()
service.start()

# Набор тестов для проверки работы статового сервиса
class test_to_dto(unittest.TestCase):
    # проверяем, что при конвертации получается dto
    def test_convertion_to_dto(self):
        nomenclature = service.repo_data[reposity.nomenclatures_key()][0]
        # print(nomenclature)
        dto = nomenclature.to_dto()
        print(f"-{dto}-")
        assert dto is not None

    def test_dto_fields_match_object(self):
        from Src.Core.common import common
        nomenclature = service.repo_data[reposity.nomenclatures_key()][0]
        dto = nomenclature.to_dto()

        dto_fields = common.get_fields(dto)
        obj_fields = common.get_fields(nomenclature)

        # Проверка полей и значений
        for field in dto_fields:
            if field in obj_fields:
                print(f"{getattr(dto, field)}, {getattr(nomenclature, field)}")
                assert getattr(dto, field) == getattr(nomenclature, field), f"Значения поля '{field}' не совпадают"
            elif field.endswith('_id') and field[:-3] in obj_fields:
                linked_obj = getattr(nomenclature, field[:-3])
                expected_id = linked_obj.id if linked_obj else None
                assert getattr(dto,
                               field) == expected_id, f"Значение поля '{field}' (id связаного объекта) не совпадают"
            else:
                raise AssertionError(f"В DTO есть поле '{field}', отсутствующее в объекте")


