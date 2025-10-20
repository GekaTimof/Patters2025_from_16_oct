import traceback

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from Src.Core.response_format import response_formats
from Src.Logics.factory_entities import factory_entities

from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.storage_model import storage_model
from Src.Models.company_model import company_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Models.receipt_model import receipt_model
from Src.Models.settings_model import settings_model

app = FastAPI()

# Функция создания разных моделей
def create_group():
    return group_model.create("test")

def create_range():
    base_range = range_model.create("test_base_range", 5)
    return range_model.create("test_range", 10, base_range)

def create_storage():
    return storage_model.create("test_storage")

def create_company():
    return company_model.create("test_company")

def create_receipt_item():
    # Нужно соответствие параметров метода create
    return receipt_item_model.create("test_item", 10, 5)

def create_receipt():
    return receipt_model.create("test_receipt", "some time", 10)

def create_nomenclature():
    test_range = range_model.create("test_base_range", 5)
    test_group = group_model.create("test")
    return nomenclature_model.create("test_nomenclature", test_group, test_range)

CREATE_FUNCS = {
    "groups": create_group,
    "nomenclature": create_nomenclature,
    "ranges": create_range,
    "storages": create_storage,
    "companies": create_company,
    "receipt_items": create_receipt_item,
    "receipts": create_receipt,
}

@app.get("/api/data")
async def get_data(
    format: str = Query("json", enum=["csv", "json", "md", "xml"]),
    model: str = Query(..., enum=list(CREATE_FUNCS.keys()))
):
    create_func = CREATE_FUNCS.get(model)
    if not create_func:
        raise HTTPException(status_code=400, detail="No create function for model")

    try:
        data = [create_func()]
        factory = factory_entities()
        factory.format = format
        content = factory.create_default(data)
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{tb}")

    return PlainTextResponse(content=content)

