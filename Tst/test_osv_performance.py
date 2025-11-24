import time
import random
from Src.start_service import start_service
from Src.Models.transaction_model import transaction_model
from Src.Dtos.transaction_dto import transaction_dto
from Src.Logics.osv_calculator import osv_calculator


class LoadTestRunner:
    def __init__(self, settings_path):
        self.service = start_service()
        self.service.load_file_name = settings_path
        self.service.start()

    def add_transactions(self, count=1000):
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
            dto.date = '2025-11-24'
            dto.storage_id = storage_id
            dto.nomenclature_id = nomenclature_id
            dto.amount=random.randint(1, 500)
            dto.range_id=range_id

            item = transaction_model.from_dto(dto, self.service.repository.cache)
            self.service.add_item_to_repository('transactions', item)

    def osv_with_block_test(self, n=5):
        results = []
        calculator = osv_calculator(self.service.repository)
        storage_id = self.service.repo_data['storages'][0].id
        date_list = ['2025-10-01', '2025-10-10', '2025-10-15', '2025-11-01', '2025-11-10']

        for date in date_list[:n]:
            self.service.change_block_period(date)
            t0 = time.time()
            res = calculator.calculate_osv_with_block(end_date=date, storage_id=storage_id, transform_dict={})
            t1 = time.time()
            results.append((date, t1 - t0, len(res)))

        return results

    def osv_test(self, n=5):
        results = []
        calculator = osv_calculator(self.service.repository)
        storage_id = self.service.repo_data['storages'][0].id
        start_date = '2025-10-01'
        end_dates = ['2025-10-10', '2025-10-15', '2025-11-01', '2025-11-10', '2025-11-20']

        for end_date in end_dates[:n]:
            t0 = time.time()
            res = calculator.calculate_osv(
                start_date=start_date,
                end_date=end_date,
                storage_id=storage_id
            )
            t1 = time.time()
            results.append((start_date, end_date, t1 - t0, len(res)))

        return results

    def run_all(self):
        self.add_transactions()
        osv_with_block_results = self.osv_with_block_test()
        osv_results = self.osv_test()
        self.save_results("performance_results.md", osv_with_block_results, osv_results)

    def save_results(self, filename, osv_with_block_results, osv_results):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Результаты нагрузочного теста\n\n")
            f.write("## calculate_osv_with_block\n")
            f.write("| Дата блокировки | Время (сек) | Количество результатов |\n")
            f.write("|---|---|---|\n")
            for date, t, count in osv_with_block_results:
                f.write(f"| {date} | {t:.6f} | {count} |\n")
            f.write("\n## calculate_osv\n")
            f.write("| Дата начала | Дата конца | Время (сек) | Количество результатов |\n")
            f.write("|---|---|---|---|\n")
            for start, end, t, count in osv_results:
                f.write(f"| {start} | {end} | {t:.6f} | {count} |\n")


if __name__ == "__main__":
    runner = LoadTestRunner("settings_my.json")
    runner.run_all()
