from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from enum import Enum
from Src.start_service import start_service
from Src.Core.response_format import response_formats  # перечисление форматов
from Src.Logics.factory_entities import factory_entities  # фабрика форматов

# иницилизация api
app = FastAPI()

# смписок всех доступных форматов
response_formats_arr = response_formats.all_formats()

# создаём и запускаем сервис
service = start_service()
service.filename = "settings.json"
try:
    service.start()
except Exception as e:
    print(f"Ошибка при запуске startservice: {e}")

# список всех объектов, уоторые можно представить (храняться в репозитории)
repo_keys = service.repository.keys()
RepoKeyEnum = Enum('RepoKeyEnum', [(key, key) for key in repo_keys], type=str)

@app.get("/data/{repo_key}")
def get_data(
    repo_key: RepoKeyEnum,
    format: str = Query("json", enum=response_formats_arr)
    ):
    try:
        if repo_key not in repo_keys:
            raise HTTPException(status_code=404, detail=f"Набор данных {repo_key} не найден")

        data = service.repo_data[repo_key]
        factory = factory_entities()
        formatted_content = factory.create_default(format, data)

        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# @app.get("/groups")
# def get_groups(format: str = Query("json", enum=response_formats_arr)):
#     try:
#         data = service.get_groups()
#         factory = factory_entities()
#         formatted_content = factory.create_default(format, data)
#
#         return PlainTextResponse(content=formatted_content)
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
#
#
# @app.get("/ranges")
# def get_ranges(format: str = Query("json", enum=response_formats_arr)):
#     try:
#         data = service.get_ranges()
#         factory = factory_entities()
#         formatted_content = factory.create_default(format, data)
#
#         return PlainTextResponse(content=formatted_content)
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
#
#
# @app.get("/receipts")
# def get_companies(format: str = Query("json", enum=response_formats_arr)):
#     try:
#         data = service.get_receipts()
#         factory = factory_entities()
#         formatted_content = factory.create_default(format, data)
#
#         return PlainTextResponse(content=formatted_content)
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
#
# @app.get("/nomenclatures")
# def get_companies(format: str = Query("json", enum=response_formats_arr)):
#     try:
#         data = service.get_nomenclatures()
#         factory = factory_entities()
#         formatted_content = factory.create_default(format, data)
#
#         return PlainTextResponse(content=formatted_content)
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
def root():
    return {"message": "API запущено, данные загружены из startservice"}