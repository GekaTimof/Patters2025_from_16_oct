import datetime

from Src.Core.common import common
from Src.Core.validator import validator
from Src.Dtos.osv_item_dto import osv_item_dto
from Src.Logics.factory_entities import factory_entities
from Src.repository import reposity
from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Core.common import argument_exception

"""
Сервис для расчёта оборота по конкретному складу в выбранный период
Требуется repository из которого буджут полученны данные 
"""
class osv_calculator:
    def __init__(self, repository):
        self.__repository: reposity = repository


    @property
    def repository(self):
        return self.__repository
    @repository.setter
    def repository(self, value: list):
        self.__repository = value

    # Возвращает агрегированные данные с начальным остатком, приходом, расходом и конечным остатком.
    def calculate_osv(
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


    # Возвращает агрегированные данные с начальным остатком, приходом, расходом и конечным остатком. (работает через прототип)
    def calculate_osv_by_prototype(
        self,
        start_date: str,
        end_date: str,
        storage_id: str,
        transform_dict: dict = {}
    ) -> list:
        repository = self.__repository

        # Конвертируем входные даты из строк в объекты datetime
        start_date = common.convert_to_date(start_date)
        end_date = common.convert_to_date(end_date)

        # Стартовый прототип хранящий все транзакции
        start_prototype = prototype(repository.data[repository.transactions_key()])

        # Получаем название склада
        storage_name = ""
        storage = next(
            (storage for storage in repository.data.get(repository.storages_key(), []) if
             storage.id == storage_id),
            None
        )
        if storage:
            storage_name = storage.name

        # Фильтр по складу
        storage_filter = filter_dto("storage", storage, filter_dto.equal_filter())
        filtered_by_storage = start_prototype.filter(start_prototype, storage_filter)

        # Фильтр по дате < start_date
        start_date_filter = filter_dto("date", start_date, filter_dto.less_filter())
        filtered_before_start = start_prototype.filter(filtered_by_storage, start_date_filter)

        # Вычисляем начальный баланс
        opening_balances = {}
        for transaction in filtered_before_start.data:
            coefficient = transaction.range.value
            actual_range = transaction.range.base.id if getattr(transaction.range, 'base',
                                                                None) else transaction.range.id
            key = (transaction.nomenclature.id, actual_range)
            opening_balances[key] = opening_balances.get(key, 0.0) + transaction.amount * coefficient

        # Фильтр по дате > start_date
        start_date_filter = filter_dto("date", start_date, filter_dto.greater_or_equal_filter())
        filtered_after_start = start_prototype.filter(filtered_by_storage, start_date_filter)

        # Фильтр по дате < end_date
        end_date_filter = filter_dto("date", end_date, filter_dto.less_or_equal_filter())
        filtered_before_end = start_prototype.filter(filtered_after_start, end_date_filter)

        # Подсчёт прихода и расхода в периоде
        incoming = {}
        outgoing = {}

        for transaction in filtered_before_end.data:
            coefficient = transaction.range.value
            actual_range = transaction.range.base.id if getattr(transaction.range, 'base',
                                                                None) else transaction.range.id
            key = (transaction.nomenclature.id, actual_range)
            amount_scaled = transaction.amount * coefficient

            if amount_scaled >= 0:
                incoming[key] = incoming.get(key, 0.0) + amount_scaled
            else:
                outgoing[key] = outgoing.get(key, 0.0) + abs(amount_scaled)

        # Итоговые ключи
        all_keys = set(opening_balances.keys()) | set(incoming.keys()) | set(outgoing.keys())

        result = []
        for key in all_keys:
            nomenclature_id, range_id = key
            # Получаем нужную номенклатуру
            nomenclature = next(
                (nomenclature for nomenclature in repository.data.get(repository.nomenclatures_key(), []) if
                 nomenclature.id == nomenclature_id),
                None
            )
            # Получаем нужную единицу измерения
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

        # Дополнительная обработка
        prototype_result = prototype(result)
        filtered_result = prototype.multi_transforming(prototype_result, transform_dict)

        return filtered_result.data


    # Возвращает агрегированные данные с начальным остатком, приходом, расходом и конечным остатком. (применяет блокировку)
    def calculate_osv_with_block(
        self,
        end_date: str,
        storage_id: str,
        transform_dict: dict = {}
    ) -> list:

        repository = self.__repository
        block_date = repository.data[repository.block_period_setting_key()]

        if end_date <= block_date:
            # Получаем данные до блокировки по нужному складу
            period_osv_dict: dict = repository.cache[repository.cache_period_osv_key()]
            period_osv: list = period_osv_dict.get(storage_id, False)
            if not period_osv:
                raise argument_exception(f"Non exist storage - {storage_id}")

            # Добавляем преобразования
            osv_prototype = prototype(period_osv)
            filtered_result = osv_prototype.multi_transforming(osv_prototype, transform_dict)
            return filtered_result.data
        else:
            # Получаем данные до блокировки по нужному складу
            period_osv_dict: dict = repository.cache[repository.cache_period_osv_key()]
            period_osv: list = period_osv_dict.get(storage_id, False)
            if not period_osv:
                return []

            after_block_date = str(common.convert_to_date(block_date) + datetime.timedelta(days=1))

            after_period_osv = self.calculate_osv_by_prototype(
                start_date=after_block_date,
                end_date=end_date,
                storage_id=storage_id
            )

            result_osv = []
            index_by_nomenclature = {}
            # Объединяем osv
            for item in period_osv + after_period_osv:
                key = item.nomenclature_id
                # Если уже есть такая номенклатура объединяем osv по числовым полям
                if key in index_by_nomenclature:
                    existing = index_by_nomenclature[key]
                    for setter in common.get_setters(item):
                        v1 = getattr(existing, setter)
                        v2 = getattr(item, setter)
                        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                            setattr(existing, setter, v1 + v2)
                # Добавляем копию osv под номенклатуру
                else:
                    item_copy = item.copy()
                    result_osv.append(item_copy)
                    index_by_nomenclature[key] = item_copy

            # Добавляем преобразования
            osv_prototype = prototype(result_osv)
            filtered_result = osv_prototype.multi_transforming(osv_prototype, transform_dict)
            return filtered_result.data


    # Получить оборотно-сальдовую ведомость в заданном формате (json, csv, markdown и т.д.).
    # Пример входных данных
    """
    start_date = 2025-10-02
    end_date = 2027-10-02
    storage_id = "5361b6c103144bbd81e6e9cd03ec600a"
    format = "json"
    transform_dict = {
        "filter": [
        ],
        "sort": [
            {
                "field_name": "closing_balance",
                "sort_type": "ASCENDING"
            }
        ]
    }
    """
    def format_osv_report(
            self,
            end_date: str,
            storage_id: str,
            format: str,
            start_date: str = "",
            transform_dict: dict = {}
    ) -> str:
        validator.validate(format, str)

        # считаем оборот
        osv = None
        if start_date:
            osv = self.calculate_osv_by_prototype(
                start_date=start_date,
                end_date=end_date,
                storage_id=storage_id,
                transform_dict=transform_dict
            )
        else:
            osv = self.calculate_osv_with_block(
                end_date=end_date,
                storage_id=storage_id,
                transform_dict=transform_dict
            )
        factory = factory_entities()
        return factory.create_default(format, osv)