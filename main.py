from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from enum import Enum
from Src.Core.common import common
from Src.Models.storage_model import storage_model
from Src.Dtos.storage_dto import storage_dto
from Src.Models.transaction_model import transaction_model
from Src.Dtos.transaction_dto import transaction_dto
from Src.start_service import start_service
from Src.Core.response_format import response_formats  # перечисление форматов
from Src.Logics.factory_entities import factory_entities  # фабрика форматов
from Src.Logics.convert_factory import convert_factory


# иницилизация api
app = FastAPI()

# смписок всех доступных форматов
response_formats_arr = response_formats.all_formats()
# фабрика перевода объектов в dict
dict_factory = convert_factory()

# создаём и запускаем сервис
service = start_service()
service.load_file_name = "settings_my.json"
try:
    service.start()
except Exception as e:
    print(f"Ошибка при запуске startservice: {e}")

# список всех объектов, которые можно предоставить (их ключи храняться в репозитории)
repo_keys = service.repository.keys()
# ограничения для repo_key - только аргумент входящий в RepoKeyEnum (ключ репозитория)
RepoKeyEnum = Enum('RepoKeyEnum', [(key, key) for key in repo_keys], type=str)


# Запрос для получения списка данных определённого типа из репозитория по ключу (в определённом формате)
@app.get("/data/get/items/{repo_key}")
def get_data(repo_key: RepoKeyEnum, format: str = Query("json", enum=response_formats_arr)):
    try:
        if repo_key not in repo_keys:
            raise HTTPException(status_code=404, detail=f"Набор данных {repo_key} не найден")

        data = service.repo_data[repo_key]
        factory = factory_entities()
        formatted_content = factory.create_default(format, data)

        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# Получить json со всеми данными фабрики
@app.get("/data/get/settings")
def get_settings():
    settings_json = service.settings()
    return PlainTextResponse(content=settings_json)


# Получить список всех рецептов и их id
@app.get("/data/get/receipts_list")
def get_receipts_list():
    receipts_list = service.repository.data.get(service.repository.receipts_key(), [])
    # Перевести в dto, получить только нужные поля
    result_json = [
        {
            "id": receipt.id,
            "name": receipt.name
        }
        for receipt in receipts_list if hasattr(receipt, "id") and hasattr(receipt, "name")
    ]
    return JSONResponse(content=result_json)


# Получить информацию о конкретном рецепте по его id
@app.get("/data/get/receipt/{receipt_id}")
def get_receipt(receipt_id: str):
    # Ищем рецепт по id среди рецептов
    for receipt in service.repository.data.get(service.repository.receipts_key(), []):
        if getattr(receipt, "id", None) == receipt_id:
            result_json = dict_factory.create(receipt).to_dict()
            return JSONResponse(content=result_json)
    raise HTTPException(status_code=404, detail="Рецепт не найден")


# Получить таблицу транзакций в данный период, на выбранном складе
@app.get("/data/get/transactions_filtered", response_class=HTMLResponse)
def get_transactions_filtered(
    start_date: str = Query(..., description="Дата начала 'YYYY-MM-DD' | 'YYYY-MM-DD HH:MM:SS'"),
    end_date: str = Query(..., description="Дата окончания 'YYYY-MM-DD' | 'YYYY-MM-DD HH:MM:SS'"),
    storage_id: str = Query(..., description="ID склада")
):
    # Преобразование строк в datetime
    start_dt = common.convert_to_date(start_date)
    end_dt = common.convert_to_date(end_date)
    if not start_dt or not end_dt:
        raise HTTPException(status_code=400, detail="Неправильный формат даты")

    # Фильтрация транзакций
    transactions = service.repo_data.get(service.repository.transactions_key(), [])
    filtered = [
        t for t in transactions
        if t.storage and t.storage.id == storage_id
        and start_dt <= t.date <= end_dt
    ]

    # Формируем HTML таблицу
    html_content = """
    <table border="1">
        <tr>
            <th>ID</th><th>Дата</th><th>Склад</th><th>Номенклатура</th><th>Количество</th><th>Ед. измерения</th>
        </tr>
    """
    for t in filtered:
        html_content += f"""
        <tr>
            <td>{t.id}</td>
            <td>{t.date}</td>
            <td>{t.storage.name if t.storage else ''}</td>
            <td>{t.nomenclature.name if t.nomenclature else ''}</td>
            <td>{t.amount}</td>
            <td>{t.range.name if t.range else ''}</td>
        </tr>
        """
    html_content += "</table>"
    return HTMLResponse(content=html_content)

# Запрос на добавление нового склада
@app.put("/data/put/storage")
def put_storage(name: str, address: str):
    # приводим строки к стандартному виду
    name.strip().lower()
    address.strip().lower()

    # Проверяем, нет ли уже такого склада в репозитории
    for storage in service.repo_data[service.repository.storages_key()]:
        if storage.name == name and storage.address == address:
            return PlainTextResponse(content=f"Склад уже существует, id: {storage.id}")

    dto = storage_dto()
    dto.name = name
    dto.address = address
    item = storage_model.from_dto(dto, service.repo_data)

    service.add_item_to_repository(service.repository.storages_key(), item)
    return PlainTextResponse(content=f"Склад добавлен, id: {item.id}")


# Запрос на добавление новой транзакции
@app.put("/data/put/transaction")
def put_transaction(date: str, storage_id: str, nomenclature_id: str, amount: int, range_id: str):
    # Проверяем что нужные данные есть в репозитории
    repo_data = service.repo_data
    if not storage_id in [i.id for i in repo_data[service.repository.storages_key()]]:
        raise HTTPException(status_code=404, detail="Склад не найден")
    if not nomenclature_id in [i.id for i in repo_data[service.repository.nomenclatures_key()]]:
        raise HTTPException(status_code=404, detail="Номенклатура не найден")
    if not range_id in [i.id for i in repo_data[service.repository.ranges_key()]]:
        raise HTTPException(status_code=404, detail="Единица измерения не найден")

    # Проверяем формат даты
    if common.convert_to_date(date) is None:
        raise HTTPException(status_code=404, detail="Неверный формат даты.\n Попробуйте - '2025-11-02' | '2025-11-02 14:30:45'")

    dto = transaction_dto()
    dto.date = date
    dto.storage_id = storage_id
    dto.nomenclature_id = nomenclature_id
    dto.amount = amount
    dto.range_id = range_id

    item = transaction_model.from_dto(dto, service.repository.cache)
    service.add_item_to_repository(service.repository.transactions_key(), item)
    return PlainTextResponse(content=f"Транзакция добавлена, id: {item.id}")


# Получить json со всеми данными фабрики
@app.get("/data/save/settings")
def get_settings(file_path: str = None):
    # Задаём путь сохранения
    if file_path:
        service.save_file_name = file_path
    service.save_settings_to_file()
    return PlainTextResponse(content="Настройки сохранены в файл")


# Базовый ответ API
@app.get("/")
def root():
    return {"message": "API запущено, данные загружены из startservice"}