import time
import random
from datetime import datetime, timedelta
from Src.start_service import start_service
from Src.Models.transaction_model import transaction_model
from Src.Dtos.transaction_dto import transaction_dto
from Src.Logics.osv_calculator import osv_calculator


class LoadTestRunner:
    def __init__(self, settings_path):
        self.service = start_service()
        self.service.load_file_name = settings_path
        self.service.start()

    def generate_random_date(self, start_year=2020, end_year=2026):
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime('%Y-%m-%d')

    def add_transactions(self, count=10000):
        storages = self.service.repo_data['storages']
        nomenclatures = self.service.repo_data['nomenclatures']

        # Формируем пары номенклатура-единица измерения
        nomenclature_range_pairs = [
            (nom.id, nom.to_dto().range_id) for nom in nomenclatures
        ]

        for _ in range(count):
            nomenclature_id, range_id = random.choice(nomenclature_range_pairs)
            storage_id = random.choice(storages).id

            dto = transaction_dto()
            dto.date = self.generate_random_date()
            dto.storage_id = storage_id
            dto.nomenclature_id = nomenclature_id
            dto.amount = 1
            dto.range_id = range_id

            item = transaction_model.from_dto(dto, self.service.repository.cache)
            self.service.add_item_to_repository('transactions', item)

    def osv_with_block_test(self, n=5):
        results = []
        calculator = osv_calculator(self.service.repository)
        storage_id = self.service.repo_data['storages'][0].id
        date_list = ['2021-01-01', '2022-01-01', '2023-01-01', '2024-01-01', '2025-01-01']

        for date in date_list[:n]:
            self.service.change_block_period(date)
            t0 = time.perf_counter()
            res = calculator.calculate_osv_with_block(end_date=date, storage_id=storage_id, transform_dict={})
            t1 = time.perf_counter()
            balances = ', '.join([str(int(i.closing_balance)) for i in res])
            results.append((date, t1 - t0, balances))

        return results

    def osv_test(self, n=5):
        results = []
        calculator = osv_calculator(self.service.repository)
        storage_id = self.service.repo_data['storages'][0].id
        start_date = '1990-01-01'
        end_dates = ['2021-01-01', '2022-01-01', '2023-01-01', '2024-01-01', '2025-01-01']

        for end_date in end_dates[:n]:
            t0 = time.perf_counter()
            res = calculator.calculate_osv(
                start_date=start_date,
                end_date=end_date,
                storage_id=storage_id
            )
            t1 = time.perf_counter()
            balances = ', '.join([str(int(i.closing_balance)) for i in res])
            results.append((end_date, t1 - t0, balances))

        return results

    def run_all(self):
        self.add_transactions()
        print(f"---{len(self.service.repo_data[self.service.repository.transactions_key()])}---")
        osv_with_block_results = self.osv_with_block_test()
        osv_results = self.osv_test()
        self.save_results("performance_results.md", osv_with_block_results, osv_results)

    def save_results(self, filename, osv_with_block_results, osv_results):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Результаты нагрузочного теста\n\n")

            f.write("## calculate_osv_with_block\n\n")
            for date, t, balances in osv_with_block_results:
                f.write(f"{date} ({t:.6f} сек): {balances}\n\n")

            f.write("## calculate_osv\n\n")
            for end_date, t, balances in osv_results:
                f.write(f"{end_date} ({t:.6f} сек): {balances}\n\n")


if __name__ == "__main__":
    runner = LoadTestRunner("settings_my.json")
    runner.run_all()
