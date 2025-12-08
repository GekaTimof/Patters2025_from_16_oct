from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.group_dto import group_dto
from Src.Dtos.storage_dto import storage_dto

# Dto для передачи параметров сервиса
# id - нужного объекта
class service_dto(abstract_dto):
    __target_id: str = ""
    __target_model: str = ""
    __target_nomenclature_dto: nomenclature_dto
    __target_range_dto: range_dto
    __target_group_dto: group_dto
    __target_storage_dto: storage_dto

    """
    Инициализация из словаря
    data: {'target_id': '123', 'target_nomenclature_dto': {...}}
    """
    def __init__(self, data: dict = None):
        if data:
            self.from_dict(data)

    # Заполнение полей из словаря
    def from_dict(self, data: dict):
        if "target_id" in data:
            self.target_id = data["target_id"]

        if "target_model" in data:
            self.target_model = data["target_model"]

        if "target_nomenclature_dto" in data:
            self.target_nomenclature_dto = data["target_nomenclature_dto"]

        if "target_range_dto" in data:
            self.target_range_dto = data["target_range_dto"]

        if "target_group_dto" in data:
            self.target_group_dto = data["target_group_dto"]

        if "target_storage_dto" in data:
            self.target_storage_dto = data["target_storage_dto"]

    @property
    def target_id(self):
        return self.__target_id
    @target_id.setter
    def target_id(self, value: str):
        validator.validate(value, str)
        self.__target_id = value

    @property
    def target_model(self):
        return self.__target_model
    @target_model.setter
    def target_model(self, value: str):
        validator.validate(value, str)
        self.__target_model = value

    @property
    def target_nomenclature_dto(self):
        return self.__target_nomenclature_dto
    @target_nomenclature_dto.setter
    def target_nomenclature_dto(self, value: nomenclature_dto):
        validator.validate(value, nomenclature_dto)
        self.__target_nomenclature_dto = value

    @property
    def target_range_dto(self):
        return self.__target_range_dto
    @target_range_dto.setter
    def target_range_dto(self, value: range_dto):
        validator.validate(value, range_dto)
        self.__target_range_dto = value

    @property
    def target_group_dto(self):
        return self.__target_group_dto
    @target_group_dto.setter
    def target_group_dto(self, value: group_dto):
        validator.validate(value, group_dto)
        self.__target_group_dto = value

    @property
    def target_storage_dto(self):
        return self.__target_storage_dto
    @target_storage_dto.setter
    def target_storage_dto(self, value: storage_dto):
        validator.validate(value, storage_dto)
        self.__target_storage_dto = value