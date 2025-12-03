from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
import json
from Src.Core.abstract_dto import abstract_dto

class response_json(abstract_response):
    # Сформировать JSON
    def create(self, format: str, data: list | dict):
        def to_serializable(d):
            if isinstance(d, dict):
                return {k: to_serializable(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [to_serializable(x) for x in d]
            elif isinstance(d, abstract_dto):
                return d.to_dict()
            else:
                return str(d)  # или d

        return json.dumps(to_serializable(data), ensure_ascii=False, indent=2)

