from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import PlainTextResponse, JSONResponse
from enum import Enum
from Src.Core.common import common
from Src.Models.storage_model import storage_model
import uuid
import json
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
from Src.Dtos.service_dto import service_dto
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.group_dto import group_dto
from functools import wraps
import inspect


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
    print(f"Ошибка при запуске start_service: {e}")

# Список всех объектов, которые можно предоставить (их ключи храняться в репозитории)
repo_keys = service.repository.keys()
# Ограничения для repo_key - только аргумент входящий в RepoKeyEnum (ключ репозитория)
RepoKeyEnum = Enum('RepoKeyEnum', [(key, key) for key in repo_keys], type=str)

# Список всех настроек, которые можно предоставить (их ключи храняться в репозитории)
settings_keys = service.repository.setting_keys()
# Ограничения для repo_key - только аргумент входящий в RepoKeyEnum (ключ репозитория)
SettingsKeyEnum = Enum('SettingsKeyEnum', [(key, key) for key in settings_keys], type=str)

# Словарь соответствия model_key → DTO класс
DTO_MAPPING = {
    "nomenclature": nomenclature_dto,
    "range": range_dto,
    "group": group_dto,
    "storage": storage_dto
}

# Список моделей которые можнор обработать через events
EventsModelKeyEnum = Enum('EventsModelKeyEnum', [(key, key) for key in [
    "nomenclature",
    "range",
    "group",
    "storage",
]], type=str)

# Enum для настроек логгера
LoggerSettingEnum = Enum('LoggerSettingEnum', [
    ('log_type', 'log_type'),
    ('show_info_logs', 'show_info_logs'),
    ('show_warning_logs', 'show_warning_logs'),
    ('show_errors_logs', 'show_errors_logs'),
    ('log_path', 'log_path')
], type=str)


# Декоратор для логирования вызова/успеха/ошибки API
def api_log(title: str = ""):
    def decorator(func):
        # Обёртка для async функций
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    service.log(f"{title} started", "INFO")
                except Exception:
                    pass
                try:
                    result = await func(*args, **kwargs)
                    try:
                        service.log(f"{title} success", "INFO")
                    except Exception:
                        pass
                    return result
                except Exception as e:
                    try:
                        service.log(f"{title} error: {e}", "ERROR")
                    except Exception:
                        pass
                    raise
            return async_wrapper

        # Обёртка для sync функций
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                service.log(f"{title} started", "INFO")
            except Exception:
                pass
            try:
                result = func(*args, **kwargs)
                try:
                    service.log(f"{title} success", "INFO")
                except Exception:
                    pass
                return result
            except Exception as e:
                try:
                    service.log(f"{title} error: {e}", "ERROR")
                except Exception:
                    pass
                raise
        return sync_wrapper

    return decorator


# Обработчик моих ошибок — возвращает подробное сообщение с кодом 400
@app.exception_handler(convertation_exception)
async def conversion_exception_handler(request: Request, exc: convertation_exception|operation_exception|argument_exception):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


# Запрос для получения списка данных определённого типа из репозитория по ключу (в определённом формате)
@app.get("/data/get/items/{repo_key}")
@api_log("GET /data/get/items")
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
@api_log("POST /data/get/items")
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


# Запрос для получения списка настроек c фильтрацией и сортировкой в формате json
@app.post("/data/get/settings/{repo_key}")
@api_log("POST /data/get/settings")
def post_settings(
    setting_key: SettingsKeyEnum,
    format: str = Query("json", enum=response_formats_arr),
    transform_dict: dict = Body({})
):
    try:
        if setting_key not in settings_keys:
            raise HTTPException(status_code=404, detail=f"Настройки {setting_key} не найдены")

        data = service.repo_data[setting_key]

        # Если это список, который можно преобразовать - преобразовываем
        if type(data) == list:
            prototype_data = prototype(data)
            prototype_filtered_data = prototype.multi_transforming(prototype_data, transform_dict)
            data = prototype_filtered_data.data
            conv_factory = convert_factory()
            data = conv_factory.create_dict_from_dto(data)

        factory = factory_entities()
        formatted_content = factory.create_default(format, data)
        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# Получить json со всеми данными фабрики
@app.get("/data/get/settings")
@api_log("GET /data/get/settings")
def get_settings():
    settings_json = service.settings()
    return PlainTextResponse(content=settings_json)


# GET через наблюдатель, для получения модели по id
@app.get("/data/event/get/{model_key}/{item_id}")
@api_log("GET /data/event/get")
async def get_with_observer(model_key: EventsModelKeyEnum, item_id: str):
    try:
        dto = service_dto({
            "target_id": item_id,
            "target_model": model_key
        })
        response = service.event("get", dto)
        conv_factory = convert_factory()
        convert_data = conv_factory.create_dict_from_dto(response)
        factory = factory_entities()
        formatted_content = factory.create_default("json", convert_data)
        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Put через наблюдатель, для добавления модели
@app.put("/data/event/put/{model_key}")
@api_log("PUT /data/event/put")
async def put_with_observer(model_key: EventsModelKeyEnum, data: dict = Body(...)):
    """
    Пример запроса:
    "target_nomenclature_dto": {
        "group_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
        "range_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
        "name": "Новый товар"
    }
    """
    try:
        # Динамически создаём DTO для model_key
        target_dto_data = data.get(f"target_{model_key}_dto")
        if not target_dto_data:
            raise HTTPException(status_code=400, detail=f"Missing target_{model_key}_dto")

        dto_class = DTO_MAPPING.get(model_key)
        if not dto_class:
            raise HTTPException(status_code=400, detail=f"Unknown model: {model_key}")

        # Заполняем setters динамически
        target_dto = dto_class()
        setters = common.get_setters(target_dto)
        for setter in setters:
            if setter in target_dto_data:
                setattr(target_dto, setter, target_dto_data[setter])

        # Создаём service_dto
        service_dto_obj = service_dto({
            "target_model": model_key,
            f"target_{model_key}_dto": target_dto
        })

        response = service.event("put", service_dto_obj)
        json_response = json.dumps(response)
        return PlainTextResponse(content=json_response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Patch через наблюдатель, для обновления модели
@app.patch("/data/event/patch/{model_key}")
@api_log("PATCH /data/event/patch")
async def patch_with_observer(model_key: EventsModelKeyEnum, id: str = "", data: dict = Body(...)):
    """
    Пример запроса:
    "id": "78d5db5d3f93429a9e9aa748658047d3"
    "target_nomenclature_dto": {
        "group_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
        "range_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
        "name": "Новый товар изменённый"
    }
    """
    try:
        # Динамически создаём DTO для model_key
        target_dto_data = data.get(f"target_{model_key}_dto")
        if not target_dto_data:
            raise HTTPException(status_code=400, detail=f"Missing target_{model_key}_dto")

        dto_class = DTO_MAPPING.get(model_key)
        if not dto_class:
            raise HTTPException(status_code=400, detail=f"Unknown model: {model_key}")

        # Заполняем setters динамически
        target_dto = dto_class()
        setters = common.get_setters(target_dto)
        for setter in setters:
            if setter in target_dto_data:
                setattr(target_dto, setter, target_dto_data[setter])

        # Создаём service_dto
        service_dto_obj = service_dto({
            "target_model": model_key,
            "target_id": id,
            f"target_{model_key}_dto": target_dto
        })

        response = service.event("patch", service_dto_obj)
        json_response = json.dumps(response)
        return PlainTextResponse(content=json_response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete через наблюдатель, для удаления модели
@app.delete("/data/event/delete/{model_key}/{item_id}")
@api_log("DELETE /data/event/delete")
async def delete_with_observer(model_key: EventsModelKeyEnum, item_id: str):
    try:
        dto = service_dto({
            "target_id": item_id,
            "target_model": model_key
        })
        response = service.event("delete", dto)
        json_response = json.dumps(response)
        return PlainTextResponse(content=json_response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Получение всех настроек логгера
@app.get("/logger/setting")
def get_logger_settings():
    try:
        settings = service.get_logger_settings()
        return JSONResponse(content=settings)
    except Exception as e:
        raise HTTPException(status_code=500, content={"error": str(e)})


# Получение конкретной настройки логгера
@app.get("/logger/{setting_key}")
def get_logger_setting(setting_key: LoggerSettingEnum):
    try:
        method_name = f"get_{setting_key.value.replace('_', '_')}"
        if hasattr(service, method_name):
            result = getattr(service, method_name)()
            return JSONResponse(content={setting_key.value: result})
        else:
            raise HTTPException(status_code=400, detail=f"Unknown logger setting: {setting_key.value}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Изменение параметров логгера напрямую через service
@app.patch("/logger/{setting_key}")
async def patch_logger_setting(setting_key: LoggerSettingEnum, value: str = Query(...)):
    try:
        # Конвертируем value в нужный тип
        if value.lower() in ['true', 'false']:
            converted_value = value.lower() == 'true'
        else:
            converted_value = value

        # Вызываем соответствующий метод service
        method_name = f"set_{setting_key.value.replace('_', '_')}"
        if hasattr(service, method_name):
            result = getattr(service, method_name)(converted_value)
            if result:
                return PlainTextResponse(content=f"Logger setting '{setting_key.value}' updated to '{value}'")
            else:
                raise HTTPException(status_code=500, detail="Failed to update logger setting")
        else:
            raise HTTPException(status_code=400, detail=f"Unknown logger setting: {setting_key.value}")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Базовый ответ API
@app.get("/")
@api_log("GET /")
def root():
    return {"message": "API запущено, данные загружены из start_service"}