from Src.Core.common import common
from Src.Core.validator import validator
from Src.Dtos.osv_item_dto import osv_item_dto
from Src.Logics.factory_entities import factory_entities


"""
Сервис для расчёта оборота по конкретному складу в выбранный период
Требуется repository из которого буджут полученны данные 
"""
class turnover_calculator:
    def __init__(self, repository):
        self.__repository = repository


    @property
    def repository(self):
        return self.__repository
    @repository.setter
    def repository(self, value: list):
        self.__repository = value

    # Возвращает агрегированные данные с начальным остатком, приходом, расходом и конечным остатком.
    def calculate_turnover(
        self,
        start_date: str,
        end_date: str,
        storage_id: str
    ) -> list:
        repository = self.repository

        # Конвертируем входные даты из строк в объекты datetime
        start_date = common.convert_to_date(start_date)
        end_date = common.convert_to_date(end_date)

        # Получаем название склада
        storage_name = ""
        storage_obj = next(
            (storage for storage in repository.data.get(repository.storages_key(), []) if
             storage.id == storage_id),
            None
        )
        if storage_obj:
            storage_name = storage_obj.name

        # Получаем все транзакции по заданному складу
        transactions = [
            transaction for transaction in repository.data.get(repository.transactions_key(), [])
            if transaction.storage and transaction.storage.id == storage_id
        ]

        # Рассчитываем начальный остаток на start_date_dt по каждой паре (номенклатура, единица измерения)
        opening_balances = {}
        for transaction in transactions:
            if transaction.date < start_date:
                # Получаем коэффициент (value)
                coefficient = transaction.range.value

                # Проверяем есть ли у range базовая единица
                actual_range = transaction.range.base.id if getattr(transaction.range, 'base',
                                                                    None) else transaction.range.id

                key = (transaction.nomenclature.id, actual_range)
                opening_balances[key] = opening_balances.get(key, 0.0) + transaction.amount * coefficient

        # Считаем приход и расход по периоду
        incoming = {}
        outgoing = {}
        for transaction in transactions:
            if start_date <= transaction.date <= end_date:
                # Получаем коэффициент (value)
                coefficient = transaction.range.value

                # Проверяем есть ли у range базовая единица
                actual_range = transaction.range.base.id if getattr(transaction.range, 'base',
                                                                    None) else transaction.range.id

                key = (transaction.nomenclature.id, actual_range)
                amount_scaled = transaction.amount * coefficient

                if amount_scaled >= 0:
                    incoming[key] = incoming.get(key, 0.0) + amount_scaled
                else:
                    outgoing[key] = outgoing.get(key, 0.0) + abs(amount_scaled)

        # Формируем итоговые ключи
        all_keys = set(opening_balances.keys()) | set(incoming.keys()) | set(outgoing.keys())
        result = []

        # Формируем итоговый список DTO для отчёта
        for key in all_keys:
            nomenclature_id, range_id = key
            nomenclature = next(
                (nomenclature for nomenclature in repository.data.get(repository.nomenclatures_key(), []) if
                 nomenclature.id == nomenclature_id),
                None
            )
            range = next(
                (range for range in repository.data.get(repository.ranges_key(), []) if range.id == range_id),
                None
            )

            opening = opening_balances.get(key, 0.0)
            inc = incoming.get(key, 0.0)
            out = outgoing.get(key, 0.0)
            closing = opening + inc - out

            dto = osv_item_dto()
            dto.storage_id = storage_id
            dto.storage_name = storage_name
            dto.nomenclature_id = nomenclature_id
            dto.nomenclature_name = nomenclature.name if nomenclature else ""
            dto.range_id = range_id
            dto.range_name = range.name if range else ""
            dto.opening_balance = opening
            dto.incoming = inc
            dto.outgoing = out
            dto.closing_balance = closing

            result.append(dto)
        return result

    # Получить оборотно-сальдовую ведомость в заданном формате (json, csv, markdown и т.д.).
    def format_turnover_report(
            self,
            start_date: str,
            end_date: str,
            storage_id: str,
            format: str,
    ) -> str:
        validator.validate(format, str)

        # считаем оборот
        turnover = self.calculate_turnover(
            start_date=start_date,
            end_date=end_date,
            storage_id=storage_id
        )
        factory = factory_entities()
        return factory.create_default(format, turnover)