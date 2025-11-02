from Src.Core.abstract_response import abstract_response
from Src.Core.common import common


class response_md(abstract_response):
    # Сформировать MD
    def create(self, format:str, data: list):
        text = ""

        item = data[0] if data else None
        if not item:
            return text
        fields = common.get_fields(item)

        header = "| " + " | ".join(fields) + " |\n"
        separator = "| " + " | ".join(["---"] * len(fields)) + " |\n"

        text += header + separator

        for row in data:
            values = [str(getattr(row, f, "")) for f in fields]
            text += "| " + " | ".join(values) + " |\n"

        return text

