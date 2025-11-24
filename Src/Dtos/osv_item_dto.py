from Src.Core.abstract_dto import abstract_dto

"""
DTO для элемента оборотно-сальдовой ведомости (ОСВ).

Поля:
- nomenclature_id: Идентификатор номенклатуры
- nomenclature_name: Наименование номенклатуры
- range_id: Идентификатор единицы измерения
- range_name: Наименование единицы измерения
- storage_id: Идентификатор единицы измерения
- storage_name: Наименование единицы измерения
- opening_balance: Начальный остаток на дату начала
- incoming: Приход за период
- outgoing: Расход за период
- closing_balance: Конечный остаток на дату окончания
"""
class osv_item_dto(abstract_dto):
    def __init__(self):
        self.__nomenclature_id = ""
        self.__nomenclature_name = ""
        self.__range_id = ""
        self.__range_name = ""
        self.__storage_id = ""
        self.__storage_name = ""
        self.__opening_balance = 0.0
        self.__incoming = 0.0
        self.__outgoing = 0.0
        self.__closing_balance = 0.0

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id
    @nomenclature_id.setter
    def nomenclature_id(self, value: str):
        self.__nomenclature_id = value
    @property
    def nomenclature_name(self) -> str:
        return self.__nomenclature_name
    @nomenclature_name.setter
    def nomenclature_name(self, value: str):
        self.__nomenclature_name = value

    @property
    def range_id(self) -> str:
        return self.__range_id
    @range_id.setter
    def range_id(self, value: str):
        self.__range_id = value
    @property
    def range_name(self) -> str:
        return self.__range_name
    @range_name.setter
    def range_name(self, value: str):
        self.__range_name = value

    @property
    def storage_id(self) -> str:
        return self.__storage_id
    @storage_id.setter
    def storage_id(self, value: str):
        self.__storage_id = value
    @property
    def storage_name(self) -> str:
        return self.__storage_name
    @storage_name.setter
    def storage_name(self, value: str):
        self.__storage_name = value

    @property
    def opening_balance(self) -> float:
        return self.__opening_balance
    @opening_balance.setter
    def opening_balance(self, value: float):
        self.__opening_balance = value
    @property
    def incoming(self) -> float:
        return self.__incoming
    @incoming.setter
    def incoming(self, value: float):
        self.__incoming = value

    @property
    def outgoing(self) -> float:
        return self.__outgoing
    @outgoing.setter
    def outgoing(self, value: float):
        self.__outgoing = value
    @property
    def closing_balance(self) -> float:
        return self.__closing_balance
    @closing_balance.setter
    def closing_balance(self, value: float):
        self.__closing_balance = value
