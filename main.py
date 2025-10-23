from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from Src.start_service import start_service
from Src.Core.response_format import response_formats  # перечисление форматов
from Src.Logics.factory_entities import factory_entities  # фабрика форматов

app = FastAPI()
service = start_service()
service.filename = "settings.json"
response_formats_arr = [response_formats.csv(),
                        response_formats.json(),
                        response_formats.md(),
                        response_formats.xml()]

try:
    service.start()
except Exception as e:
    print(f"Ошибка при запуске startservice: {e}")

@app.get("/groups")
def get_groups(format: str = Query("json", enum=response_formats_arr)):
    try:
        data = service.get_groups()
        factory = factory_entities()
        formatted_content = factory.create_default(format, data)

        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/ranges")
def get_ranges(format: str = Query("json", enum=response_formats_arr)):
    try:
        data = service.get_ranges()
        factory = factory_entities()
        formatted_content = factory.create_default(format, data)

        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/receipts")
def get_companies(format: str = Query("json", enum=response_formats_arr)):
    try:
        data = service.get_receipts()
        factory = factory_entities()
        formatted_content = factory.create_default(format, data)

        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/nomenclatures")
def get_companies(format: str = Query("json", enum=response_formats_arr)):
    try:
        data = service.get_nomenclatures()
        factory = factory_entities()
        formatted_content = factory.create_default(format, data)

        return PlainTextResponse(content=formatted_content)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
def root():
    return {"message": "API запущено, данные загружены из startservice"}