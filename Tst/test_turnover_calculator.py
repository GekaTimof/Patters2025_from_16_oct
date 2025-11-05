import unittest
from Src.Logics.turnover_calculator import turnover_calculator
from Src.start_service import start_service
import json

# Набор тестов для работы с Dto
class test_turnover_calculator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Запускаем сервис один раз для всех тестов
        cls.service = start_service()
        cls.service.load_file_name = "settings_my.json"
        cls.service.start()

        cls.turnover_calculator = turnover_calculator(cls.service.repository)

    # Проверяем, что расчёт баланса отрабатывает правильно
    def test_turnover_balance_basic(self):
        start_date = "2025-01-01"
        end_date = "2027-01-01"
        storage_id = "5361b6c103144bbd81e6e9cd03ec600a"

        turnover = self.turnover_calculator.calculate_turnover(start_date, end_date, storage_id)

        # Проверяем, что получили список DTO
        self.assertIsInstance(turnover, list)
        self.assertGreater(len(turnover), 0)

        # Проверяем структуру первого элемента
        item = turnover[0]
        self.assertTrue(hasattr(item, "nomenclature_id"))
        self.assertTrue(hasattr(item, "opening_balance"))
        self.assertIsInstance(item.opening_balance, (int, float))

    # Проверяем, что дынные возвращаются в правильном формате
    def test_format_report(self):
        turnover = []
        start_date = "2025-01-01"
        end_date = "2027-01-01"
        storage_id = "5361b6c103144bbd81e6e9cd03ec600a"
        format = "json"

        formatted = self.turnover_calculator.format_turnover_report(
            start_date=start_date,
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


    # Порверяем, что баланс расчитывается правильно
    # -есть нужные поля и отношения между ними соответствуют ожиданиям
    def test_turnover_balance_correctness(self):
        start_date = "2025-01-01"
        end_date = "2027-01-01"
        storage_id = "5361b6c103144bbd81e6e9cd03ec600a"

        turnover = self.turnover_calculator.calculate_turnover(start_date, end_date, storage_id)

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
