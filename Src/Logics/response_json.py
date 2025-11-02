from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
import json

class response_json(abstract_response):
    # Сформировать JSON
    def create(self, format: str, data: list):
        result = []

        for row in data:
            obj = {}
            fields = common.get_fields(row)
            for f in fields:
                obj[f] = str(getattr(row, f, ""))
            result.append(obj)

        return json.dumps(result, ensure_ascii=False, indent=2)

