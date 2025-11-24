from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import PlainTextResponse, JSONResponse
from enum import Enum
from Src.Core.common import common
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Dtos.storage_dto import storage_dto
from Src.Models.transaction_model import transaction_model
from Src.Dtos.transaction_dto import transaction_dto
from Src.start_service import start_service
from Src.Core.response_format import response_formats  # перечисление форматов
from Src.Logics.factory_entities import factory_entities  # фабрика форматов
from Src.Logics.factory_convert import convert_factory
from Src.Dtos.osv_item_dto import osv_item_dto
from Src.Core.validator import convertation_exception, operation_exception, argument_exception
from fastapi import Request
from Src.Logics.osv_calculator import osv_calculator
from Src.Core.prototype import prototype

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


# Обработчик моих ошибок — возвращает подробное сообщение с кодом 400
@app.exception_handler(convertation_exception)
async def conversion_exception_handler(request: Request, exc: convertation_exception|operation_exception|argument_exception):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


# Запрос для получения списка данных определённого типа из репозитория по ключу (в определённом формате)
@app.get("/data/get/items/{repo_key}")
def get_data(repo_key: RepoKeyEnum, format: str = Query("json", enum=response_formats_arr)):
    try:
        if repo_key not in repo_keys:
            raise HTTPException(status_code=404, detail=f"Набор данных {repo_key} не найден")

        data = service.repo_data[repo_key]
        conv_factory = convert_factory()
        convert_data = conv_factory.create_dict_from_dto(data)

        factory = factory_entities()
        formatted_content = factory.create_default(format, convert_data)


        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# Запрос для получения списка данных c фильтрацией и сортировкой в формате json
@app.post("/data/get/items/{repo_key}")
def post_data(
    repo_key: RepoKeyEnum,
    format: str = Query("json", enum=response_formats_arr),
    transform_dict: dict = Body({})
):
    try:
        if repo_key not in repo_keys:
            raise HTTPException(status_code=404, detail=f"Набор данных {repo_key} не найден")

        prototype_data = prototype(service.repo_data[repo_key])
        prototype_filtered_data = prototype.multi_transforming(prototype_data, transform_dict)
        data = prototype_filtered_data.data

        conv_factory = convert_factory()
        convert_data = conv_factory.create_dict_from_dto(data)

        factory = factory_entities()
        formatted_content = factory.create_default(format, convert_data)

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


# Получить оборотно-сальдовую ведомость за период по выбранному складу.
# Возвращает агрегированные данные с начальным остатком, приходом, расходом и конечным остатком.
# Поддержка различных форматов вывода (json, csv, markdown и т.д.).
@app.post("/report/get/osv")
def report_osv(
    start_date: str = Query(..., description="Дата начала, формат YYYY-MM-DD"),
    end_date: str = Query(..., description="Дата окончания, формат YYYY-MM-DD"),
    storage_id: str = Query(..., description="ID склада"),
    format: str = Query("json", enum=response_formats_arr),
    transform_dict: dict = Body({})
):
    balance_calculator = osv_calculator(service.repository)
    formatted_result = balance_calculator.format_osv_report(
        start_date=start_date,
        end_date=end_date,
        storage_id=storage_id,
        format=format,
        transform_dict=transform_dict
    )
    return PlainTextResponse(content=formatted_result)


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

    # Конвертируем дату в текст
    try:
        date_obj = common.convert_to_date(date)
    except ValueError as e:
        return PlainTextResponse(content=str(e))

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
@app.post("/data/save/settings")
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