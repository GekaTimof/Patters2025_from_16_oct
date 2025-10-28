from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from enum import Enum
from Src.start_service import start_service
from Src.Core.response_format import response_formats  # перечисление форматов
from Src.Logics.factory_entities import factory_entities  # фабрика форматов
from Src.Logics.convert_factory import convert_factory

# иницилизация api
app = FastAPI()

# смписок всех доступных форматов
response_formats_arr = response_formats.all_formats()

factory = convert_factory()

# создаём и запускаем сервис
service = start_service()
service.file_name = "settings.json"
try:
    service.start()
except Exception as e:
    print(f"Ошибка при запуске startservice: {e}")

# список всех объектов, которые можно предоставить (их ключи храняться в репозитории)
repo_keys = service.repository.keys()
# ограничения для repo_key - только аргумент входящий в RepoKeyEnum (ключ репозитория)
RepoKeyEnum = Enum('RepoKeyEnum', [(key, key) for key in repo_keys], type=str)

# Запрос для получения данных из репозитория по ключу
@app.get("/data/{repo_key}")
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

@app.get("/catalogs")
def get_catalogs():
    # Возвращает весь справочник в json с использованием фабрики
    settings_json = service.settings()
    return JSONResponse(content=settings_json)

@app.get("/receipts")
def get_receipts():
    receipts_list = service.repository.data.get("receipts", [])
    # Перевести в dto, получить только нужные поля
    result_json = [
        {
            "id": r.id,
            "name": r.name
        }
        for r in receipts_list if hasattr(r, "id") and hasattr(r, "name")
    ]
    return JSONResponse(content=result_json)


@app.get("/receipt/{receipt_id}")
def get_receipt(receipt_id: str):
    # Ищем рецепт по id среди рецептов
    for r in service.repository.data.get("receipts", []):
        if getattr(r, "id", None) == receipt_id:
            result_json = factory.create(r.to_dto())
            return JSONResponse(content=result_json)
    raise HTTPException(status_code=404, detail="Receipt not found")


@app.get("/")
def root():
    return {"message": "API запущено, данные загружены из startservice"}