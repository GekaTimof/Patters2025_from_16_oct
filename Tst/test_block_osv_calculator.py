import unittest
from Src.Logics.osv_calculator import osv_calculator
from Src.start_service import start_service
import json

# Набор тестов для работы с Dto
class test_block_osv_calculator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Запускаем сервис один раз для всех тестов
        cls.service = start_service()
        cls.service.load_file_name = "settings_my.json"
        cls.service.start()

        cls.osv_calculator = osv_calculator(cls.service.repository)

    # Проверяем, что расчёт баланса отрабатывает правильно (с учётом блокировки).
    def test_turnover_balance_basic(self):
        end_date = "2027-01-01"
        storage_id = "5361b6c103144bbd81e6e9cd03ec600a"

        turnover = self.osv_calculator.calculate_osv_with_block(end_date, storage_id)

        # Проверяем, что получили список DTO
        self.assertIsInstance(turnover, list)
        self.assertGreater(len(turnover), 0)

        # Проверяем структуру первого элемента
        item = turnover[0]
        self.assertTrue(hasattr(item, "nomenclature_id"))
        self.assertTrue(hasattr(item, "opening_balance"))
        self.assertIsInstance(item.opening_balance, (int, float))

    # Проверяем, что дынные возвращаются в правильном формате (с учётом блокировки).
    def test_format_report(self):
        turnover = []
        end_date = "2027-01-01"
        storage_id = "5361b6c103144bbd81e6e9cd03ec600a"
        format = "json"

        formatted = self.osv_calculator.format_osv_report(
            end_date=end_date,
            storage_id=storage_id,
            format=format)
        print(formatted)
        self.assertIsInstance(formatted, str)

        # Дополнительная проверка: можно ли распарсить результат в JSON
        try:
            parsed = json.loads(formatted)
            self.assertIsInstance(parsed, (list, dict))
        except json.JSONDecodeError:
            self.fail("Formatted output is not valid JSON")


    # Порверяем, что баланс расчитывается правильно (с учётом блокировки).
    # -есть нужные поля и отношения между ними соответствуют ожиданиям
    def test_turnover_balance_correctness(self):
        end_date = "2027-01-01"
        storage_id = "fc5ab65500f54f7d843684856e836e77"

        turnover = self.osv_calculator.calculate_osv_with_block(end_date, storage_id)

        self.assertIsInstance(turnover, list)
        self.assertGreater(len(turnover), 0)

        for item in turnover:
            self.assertTrue(hasattr(item, "opening_balance"))
            self.assertTrue(hasattr(item, "incoming"))
            self.assertTrue(hasattr(item, "outgoing"))
            self.assertTrue(hasattr(item, "closing_balance"))

            # Проверяем типы значений
            self.assertIsInstance(item.opening_balance, (int, float))
            self.assertIsInstance(item.incoming, (int, float))
            self.assertIsInstance(item.outgoing, (int, float))
            self.assertIsInstance(item.closing_balance, (int, float))

            # Проверяем формулу итогового баланса
            calculated_closing = item.opening_balance + item.incoming - item.outgoing
            self.assertAlmostEqual(item.closing_balance, calculated_closing, places=5)


    # Порверяем, что баланс расчитывается правильно (после смены даты блокировки).
    # -есть нужные поля и отношения между ними соответствуют ожиданиям
    def test_turnover_balance_correctness_after_change_block_period(self):
        # Меняем перод блокировки
        self.service.change_block_period("2024-01-01")

        end_date = "2027-01-01"
        storage_id = "5361b6c103144bbd81e6e9cd03ec600a"

        turnover = self.osv_calculator.calculate_osv_with_block(end_date, storage_id)

        self.assertIsInstance(turnover, list)
        self.assertGreater(len(turnover), 0)

        for item in turnover:
            self.assertTrue(hasattr(item, "opening_balance"))
            self.assertTrue(hasattr(item, "incoming"))
            self.assertTrue(hasattr(item, "outgoing"))
            self.assertTrue(hasattr(item, "closing_balance"))

            # Проверяем типы значений
            self.assertIsInstance(item.opening_balance, (int, float))
            self.assertIsInstance(item.incoming, (int, float))
            self.assertIsInstance(item.outgoing, (int, float))
            self.assertIsInstance(item.closing_balance, (int, float))

            # Проверяем формулу итогового баланса
            calculated_closing = item.opening_balance + item.incoming - item.outgoing
            self.assertAlmostEqual(item.closing_balance, calculated_closing, places=5)

if __name__ == "__main__":
    unittest.main()
